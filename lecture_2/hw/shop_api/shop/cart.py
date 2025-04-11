from pydantic import BaseModel
from hw.shop_api.shop.Items_in_cart import ItemsInCart


class Cart(BaseModel):
    id: str
    items: list[ItemsInCart]
    price: float
