from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        primary_key=True, index=True, default_factory=uuid.uuid4
    )

    username: str = Field(unique=True)

    email: str = Field(unique=True)

    password: str

    created_at: datetime
