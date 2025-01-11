import uuid
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import select


from . import database
from . import models
from . import oauth2
from . import schemas
from . import utils
from . database import SessionDep


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Creating database and tables...")
    database.create_db_and_tables()
    yield


users_app = FastAPI(lifespan=lifespan)


@users_app.post(
    "/register/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserRegister, database: SessionDep):
    hashed_password = utils.hash_password(user.password)

    # new_user = models.User(user.email, hashed_password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        created_at=datetime.now(),
    )

    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    return new_user


@users_app.get("/user/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: uuid.UUID, database_session: SessionDep):
    user = database_session.get(models.User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No User Found"
        )

    return user


@users_app.post("/login")
def login(
    database_session: SessionDep,
    user_oauth2_form: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    user = database_session.exec(
        select(models.User).where(models.User.email == user_oauth2_form.username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify_password(user_oauth2_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id.hex})

    return schemas.Token(access_token=access_token, token_type="bearer")


# @users_app.post("/login/refresh")
# def login_refresh():
#     raise NotImplementedError



@users_app.get("/health")
def health_check(
    _database_session: SessionDep,
):
    return Response(status_code=200)


