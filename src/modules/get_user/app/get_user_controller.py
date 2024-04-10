from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_user_usecase import GetUserUsecase
from .get_user_viewmodel import GetUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from aws_lambda_powertools import Logger



class GetUserController:

    def __init__(self, usecase: GetUserUsecase, observability: ObservabilityAWS):
        self.GetUserUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            if request.data.get('id') is None:
                raise MissingParameters('id')

            if type(request.data.get('id')) != str:
                raise WrongTypeParameter(
                    fieldName="id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('id').__class__.__name__
                )

            if not request.data.get('id').isdecimal():
                raise EntityError("id")


            user = self.GetUserUsecase(
                id=int(request.data.get('id'))
            )

            viewmodel = GetUserViewmodel(user)
            
            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=user.id)
            return response

        except NoItemsFound as err:
            self.observability.log_exception(message=err.message)
            return NotFound(body=err.message)

        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])
