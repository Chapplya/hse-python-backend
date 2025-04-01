from pydantic import BaseModel


class Items(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False
