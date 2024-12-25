from pydantic import BaseModel, Field, EmailStr, ConfigDict, SecretStr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MonitorModel(Base):
    __tablename__ = "monitors"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    model: Mapped[str]
    description: Mapped[str]


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str] = Field(max_length=15)
    password: Mapped[str]


class MonitorAddSchema(BaseModel):
    title: str = Field(max_length=30)
    model: str
    description: str = Field(max_length=100)


class MonitorSchema(MonitorAddSchema):
    id: int


class UserAddSchema(BaseModel):
    email: str
    username: str = Field(max_length=15)
    password: str

    model_config = ConfigDict(extra='forbid')


class UserSchema(UserAddSchema):
    id: int


class UserLoginSchema(BaseModel):
    username:str = Field(max_length=15)
    password:str