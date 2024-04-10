from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.state_enum import STATE


class Test_GetAllUsersViewmodel:
    all_users_list = [
        User(id=1,
             name="Lucas Duez",
             state=STATE.APPROVED),

        User(id=2,
             name="Laura Blablachan",
             state=STATE.APPROVED),
    ]

    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "all_users": [
                {
                    'id': 1,
                    'name': "Lucas Duez",
                    'state': 'APPROVED',
                },
                {
                    'id': 2,
                    'name': "Laura Blablachan",
                    'state': 'APPROVED',
                }
            ],
            "message": "all users has been retrieved"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            User(id=2,
                 name="Laura Blablachan",
                 state=STATE.APPROVED),
)

        response = viewmodel.to_dict()

        expected = {
                    'id': 2,
                    'name': "Laura Blablachan",
                    'state': 'APPROVED',
        }

        assert response == expected


    
