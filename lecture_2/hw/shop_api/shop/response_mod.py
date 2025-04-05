from pydantic import BaseModel
from lecture_2.hw.shop_api.shop.Items_in_cart import ItemsInCart


class CartResponse(BaseModel):
    id: str
    items: list[ItemsInCart]
    price: float


class ItemsResponse(BaseModel):
    id: str
    name: str
    price: float
    deleted: bool = False
    
class ItemListResponse(BaseModel):
    items: list[ItemsResponse]
