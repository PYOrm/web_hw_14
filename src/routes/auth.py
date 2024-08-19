
from fastapi import APIRouter, status, Depends, HTTPException, Security, BackgroundTasks, Request
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserResponse, UserModel, TokenModel
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    API route for create new user

    :param body: user information
    :param request: request from client
    :param background_tasks: Background task for schedule send confirmation later for new user
    :param db: Session for DB Connection
    :return: dictionary with new user information and confirm text
    """
    exist_user = await repository_users.get_user_by_email(db, body.email)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(db, body)
    background_tasks.add_task(send_email, new_user.email, new_user.name, request.base_url.__str__())
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    API route for login

    :param body: information about user
    :param db: Session for DB Connection
    :return: Access JWT token and Update JWT token for login user
    """
    user = await repository_users.get_user_by_email(db, body.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.email_confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(db, user, refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    API rote to update access token using refresh token

    :param credentials: JWT refresh token
    :param db: Session for DB Connection
    :return: Access JWT token and Update JWT token for login user
    """

    token = credentials.credentials
    # print(token)
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(db, email)
    if user.update_token != token:
        await repository_users.update_token(db, user, None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(db, user, refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    API rote for confirm user email address
    :param token: Unique JWT token for user confirmation email
    :param db: Session for DB Connection
    :return: Message of confirmation
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.email_confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}
