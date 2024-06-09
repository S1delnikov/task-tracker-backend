from pydantic import BaseModel

class Token(BaseModel):
    """Представление JWT-токена\n
    access_token: str
    token_type: str
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Представление данных, хранящихся в токене\n
    username: str | None = None
    """
    username: str | None = None