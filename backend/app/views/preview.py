from pydantic import BaseModel


class PreviewView(BaseModel):
    image: str


class AdminSessionView(BaseModel):
    authenticated: bool
    username: str
