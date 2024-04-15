from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBaseDTO(BaseModel):
    email: EmailStr


class UserInDTO(UserBaseDTO):
    password: str = Field(max_length=35)


class UserOutDTO(UserBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
