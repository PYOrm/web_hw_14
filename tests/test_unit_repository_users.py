import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.repository.users import create_user, get_user_by_email, update_avatar, confirmed_email, update_token
from src.schemas import UserModel


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.user = User("str", "str@mail.com", "str")
        self.user_model = UserModel(name="str", email="str@mail.com", password='str')
        self.session = MagicMock(spec=Session)

    def tearDown(self):
        del self.user_model
        del self.session
        del self.user

    async def test_create_user(self):
        result = await create_user(self.session, self.user_model)
        assert self.user_model.name == result.name
        self.assertTrue(hasattr(result, "id"))

    async def test_get_user_by_email(self):
        user = MagicMock(User)
        self.session.query().filter_by().first.return_value = user
        result = await get_user_by_email(self.session, "str@mail.com")
        self.assertEqual(result, user)

    async def test_update_avatar(self):
        user = MagicMock(User)
        self.session.query().filter_by().first.return_value = user
        result = await update_avatar("str@mail.com", "str", self.session)
        self.assertEqual(result.avatar, user.avatar)

    async def test_confirmed_email(self):
        user = self.user
        self.session.query().filter_by().first.return_value = user
        await confirmed_email("str@mail.com", self.session)
        self.assertEqual(user.email_confirmed, True)

    async def test_update_token(self):
        user = self.user
        self.session.query().filter_by().first.return_value = user
        await update_token(self.session, user, "str",)
        self.assertEqual(user.update_token, "str")


if __name__ == "__main__":
    unittest.main()
