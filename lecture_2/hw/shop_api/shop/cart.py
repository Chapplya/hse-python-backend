from pydantic import BaseModel
from lecture_2.hw.shop_api.shop.Items_in_cart import ItemsInCart


class Cart(BaseModel):
    id: str
    items: list[ItemsInCart]
    price: float
