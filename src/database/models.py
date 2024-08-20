from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

"""
Models of Objects in DB
"""

Base = declarative_base()


class Contact(Base):
    """
    Class Contact represent information about contacts of users

    :param id: contact Primary key
    :param name: contact name
    :param soname: contact soname
    :param email: contact email address
    :param phone: contact phone number
    :param birthday: contact birthday date
    :param info: contact additional information
    :param user_id: user id of contact owner (related to user table)
    """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    soname = Column(String(50), nullable=False)
    email = Column(String(100))
    phone = Column("phone_number", String(30))
    birthday = Column("birth_day", Date)
    info = Column("Info", String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    users = relationship("User", back_populates="contacts")


class User(Base):
    """
    Class User represent information about application user

    :param id: contact Primary key
    :param name: contact name
    :param email: contact email address
    :param password: password for user account
    :param update_token: JWT token for update security token
    :param avatar: URL for avatar image location
    :param email_confirmed: identification that user confirm his email
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    update_token = Column(String)
    contacts = relationship("Contact", back_populates="users")
    avatar = Column(String, default=None)
    email_confirmed = Column(Boolean, default=False)

    def __init__(self, name, email, password, update_token=None, id=0, avatar=None, email_confirmed=False):
        self.name = name
        self.email = email
        self.password = password
        self.update_token = update_token
        self.id = id
        self.avatar = avatar
        self.email_confirmed = email_confirmed

    def __str__(self):
        return f"{self.name}_{self.email}_{self.password}_{self.update_token}_{self.id}"
