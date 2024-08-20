import datetime
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.repository.contacts import get_all_contacts, get_contact_by_id, get_contact_, delete_contact, \
    update_contact_by_id, create_contact, get_upcoming_birthdays
from src.schemas import ContactModel


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=9, name="I", email="I@gmail.com", password="123", update_token=None, email_confirmed=True)
        self.contacts = [Contact(id=1, name="John", soname="Wick", email="John.Wick@gmail.com", phone="123456789",
                                 birthday=datetime.date(1980, 8, 22), info=None, user_id=9),
                         Contact(id=2, name="Ozzy", soname="Osborn", email="Ozzy.Osborn@gmail.com", phone="6666666666",
                                 birthday=datetime.date(1968, 9, 1), info=None, user_id=9)
                         ]
        self.contact_model = ContactModel(name="John", soname="Wick", email="John.Wick@gmail.com", phone="123456789",
                                          birthday=datetime.date(1980, 8, 22), info="")

    def tearDown(self):
        del self.contacts
        del self.user
        del self.session

    async def test_get_all_contacts(self):
        self.session.query().filter_by().offset().limit().all.return_value = self.contacts
        result = await get_all_contacts(self.session, self.user)
        self.assertListEqual(result, self.contacts)

    async def test_get_all_contacts_none(self):
        self.session.query().filter_by().offset().limit().all.return_value = []
        result = await get_all_contacts(self.session, self.user)
        self.assertEqual(result, [])

    async def test_get_contact_by_id(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_id(self.session, 1, self.user)
        self.assertEqual(result, contact)

    async def test_get_contact_name(self):
        contact = Contact()
        self.session.query().filter_by().all.return_value = contact
        self.session.query().filter_by().filter_by().all.return_value = contact
        result1 = await get_contact_(self.session, "str", None, None, user=self.user)
        self.assertEqual(result1, contact)

    async def test_get_contact_name_soname(self):
        contact = Contact()
        self.session.query().filter_by().all.return_value = contact
        self.session.query().filter_by().filter_by().all.return_value = contact
        self.session.query().filter_by().filter_by().filter_by().all.return_value = contact
        result2 = await get_contact_(self.session, "str", "str", None, user=self.user)
        self.assertEqual(result2, contact)

    async def test_get_contact_email(self):
        contact = Contact()
        self.session.query().filter_by().all.return_value = contact
        self.session.query().filter_by().filter_by().all.return_value = contact
        result3 = await get_contact_(self.session, None, None, "str", user=self.user)
        self.assertEqual(result3, contact)

    async def test_get_contact_none(self):
        contact = Contact()
        self.session.query().filter_by().all.return_value = contact
        result4 = await get_contact_(self.session, None, None, None, user=self.user)
        self.assertEqual(result4, contact)

    async def test_get_contact_name_soname_email(self):
        contact = Contact()
        self.session.query().filter_by().all.return_value = contact
        self.session.query().filter_by().filter_by().filter_by().filter_by().all.return_value = contact
        result3 = await get_contact_(self.session, "str", "str", "str", user=self.user)
        self.assertEqual(result3, contact)

    async def test_delete_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result3 = await delete_contact(self.session, 1, user=self.user)
        self.assertEqual(result3, contact)

    async def test_update_contact_by_id(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result3 = await update_contact_by_id(self.session, 1, self.contact_model, user=self.user)
        self.assertEqual(result3, contact)

    async def test_create_contact(self):
        result3 = await create_contact(self.session, self.contact_model, user=self.user)
        assert self.contact_model.name == result3.name
        self.assertTrue(hasattr(result3, "id"))

    async def test_get_upcoming_birthdays(self):
        self.session.query().filter().all.return_value = self.contacts
        result3 = await get_upcoming_birthdays(self.session, user=self.user)
        self.assertEqual(result3, [self.contacts[0]])


if __name__ == "__main__":
    unittest.main()
