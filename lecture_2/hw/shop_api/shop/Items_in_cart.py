from pydantic import BaseModel


class ItemsInCart(BaseModel):
    id: str
    name: str
    quantity: int
    available: bool
