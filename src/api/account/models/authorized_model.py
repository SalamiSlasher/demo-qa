from pydantic import BaseModel


class AuthorizedModel(BaseModel):
    userName: str
    password: str
