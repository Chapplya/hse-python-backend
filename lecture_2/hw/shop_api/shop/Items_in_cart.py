from pydantic import BaseModel


class Items_In_Cart(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool
