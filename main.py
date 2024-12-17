from contextlib import asynccontextmanager
from datetime import datetime
import uuid
import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
import schemas
import models
import utils
import database
import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import SessionDep
from sqlmodel import select

# TODO test with local database
# TODO async?


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@users_app.get("/user/{uuid}", response_model=schemas.UserResponse)
def get_user(id: uuid.UUID, database: SessionDep):
    user = database.get(models.User, id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No User Found"
        )

    return user


@users_app.post("/login")
def login(
    database: SessionDep,
    user_cerd: OAuth2PasswordRequestForm = Depends(),
):
    user = database.exec(
        select(models.User).where(models.User.email == user_cerd.username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify_password(user_cerd.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id.hex})

    return {"access_token": access_token, "token_type": "bearer"}


@users_app.post("/login/refresh")
def login_refresh():
    raise NotImplementedError


if __name__ == "__main__":
    uvicorn.run(users_app, host="0.0.0.0", port=8000)
