from pydantic import BaseModel
from Items_in_cart import Items_In_Cart


class Cart(BaseModel):
    id: int
    items: list[Items_In_Cart]
    price: float
