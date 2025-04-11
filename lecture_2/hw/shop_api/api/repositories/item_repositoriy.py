from fastapi import HTTPException
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from hw.shop_api.shop.Items import Items, ItemCreate
from hw.shop_api.shop.response_mod import ItemsResponse, ItemListResponse
import uuid

items = {}


class ItemRepositoriy:

    @staticmethod
    def generate_id_item():
        return str(uuid.uuid4())

    def create_item(self, item: ItemCreate):
        id_item = self.generate_id_item()
        items[id_item] = Items(id=id_item, name=item.name, price=item.price)

        return {"item": items[id_item]}

    def get_item(self, id: int):
        if id not in items:
            raise HTTPException(status_code=404, detail="Not found id")
        if items[id].deleted:
            raise HTTPException(status_code=404, detail="Items has been deleted")
        return {"item": items[id]}

    def get_list_items(
        self,
        offset: NonNegativeInt = 0,
        limit: PositiveInt = 10,
        min_price: NonNegativeFloat = None,
        max_price: NonNegativeFloat = None,
        show_deleted: bool = False,
    ):
        if not items:
            raise HTTPException(status_code=404, detail="Items is empty")

        items_val = list(items.values())

        if show_deleted:
            items_val = [elem for elem in items_val if not elem.deleted]
        if min_price is not None:
            items_val = [elem for elem in items_val if elem.price >= min_price]
        if max_price is not None:
            items_val = [elem for elem in items_val if elem.price <= max_price]

        items_val = items_val[offset : offset + limit + 1]

        items_response = [ItemsResponse(**item.dict()) for item in items_val]

        return ItemListResponse(items=items_response)

    def put_items(self, id: int, item: dict):
        if id not in items:
            raise HTTPException(status_code=404, detail="id not in items")
        items[id] = Items(id=id, name=item["name"], price=item["price"])
        return {"item": items[id]}

    def put_items(self, id: int, item: dict):
        if id not in items:
            raise HTTPException(status_code=404, detail="id not in items")

        old_item = items[id]

        if old_item.status_delete:
            raise HTTPException(status_code=304, detail="Item not modified")

        invalid_keys = set(item.keys()) - set(old_item.model_dump().keys())

        if invalid_keys:
            raise HTTPException(status_code=422, detail="Wrong field")

        # pattern for update data
        items[id].name = item.get("name", old_item.name)
        items[id].price = item.get("price", old_item.price)
        items[id].deleted = item.get("deleted", old_item.delete)

        if old_item.deleted != items[id].deleted:
            raise HTTPException(status_code=422, detail="status connot be changed")

        return {"items": items[id]}

    def delete_it(self, id: int):
        if id not in items:
            raise HTTPException(status_code=404, detail="id not in items")

        items[id].deleted = True

        return {"item": items[id]}
