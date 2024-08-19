from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel

""" Access for users"""


async def create_user(db: Session, body: UserModel) -> User:
    """
    Create new user

    :param db: connection to DB
    :param body: information about new user
    :return: new user object
    :rtype: User
    """
    user = User(**body.__dict__)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Get user by email

    :param db: connection to DB
    :param email: user email
    :return: user
    :rtype: User
    """
    return db.query(User).filter_by(email=email).first()


async def update_token(db: Session, user: User, token: str | None) -> None:
    """

    :param db: connection to DB
    :param user: application user
    :param token: JWT update token
    :return: Nothing return
    :rtype: None
    """
    user.update_token = token
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update user avatar using user email for user identification

    :param email: user email for user identification
    :param url: URL of avatar
    :param db: connection to DB
    :return: updated user
    :rtype: User
    """
    user = await get_user_by_email(db, email)
    user.avatar = url
    db.commit()
    return user


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirm user email

    :param email: ser email for user identification
    :param db: connection to DB
    :return: return nothing
    :rtype: None
    """

    user = await get_user_by_email(db, email)
    user.email_confirmed = True
    db.commit()
