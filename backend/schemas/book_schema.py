from pydantic import BaseModel


class CreateBookResp(BaseModel):
    title: str
    author: str
    isbn: str
    category: str | None = None
    total_copies: int
    available_copies: int

    model_config = {
        "from_attributes": True
    }


class CreateBookReq(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    total_copies: int


class GetBookResp(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    category: str
    total_copies: int
    available_copies: int

    model_config = {
        "from_attributes": True
    }


class DeleteBookResp(BaseModel):
    title: str
    response: str

    model_config = {
        "from_attributes": True
    }