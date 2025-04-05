from fastapi import APIRouter, HTTPException
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from lecture_2.hw.shop_api.shop.Items import Items, ItemCreate
from http import HTTPStatus

router_item = APIRouter(prefix="/item")
items = {
    1: Items(id=1, name="Молоко", price=121.99),
    2: Items(id=2, name="Кокс", price=1211.228),
}


def generate_id_item(items: dict):
    return max(items.keys(), default=0) + 1

@router_item.post("", status_code=HTTPStatus.CREATED)
async def create_item(item: ItemCreate):
    id_item = generate_id_item(items)
    items[id_item] = Items(id=id_item, name=item.name, price=item.price)

    return {"item": items[id_item]}


@router_item.get("/{id}", status_code=HTTPStatus.OK)
async def get_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Not found id")
    if items[id].deleted == True:
        raise HTTPException(status_code=404, detail="Items has been deleted")
    return items[id]


@router_item.get("", status_code=HTTPStatus.OK)
async def get_list_items(
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

    items_val = items_val[offset : offset + limit]

    return items_val


@router_item.put("/{id}", status_code=HTTPStatus.OK)
async def put_items(id: int, item: dict):
    if id not in items:
        raise HTTPException(status_code=404, detail="id not in items")
    items[id] = Items(id=id, name=item["name"], price=item["price"])
    return items[id]


@router_item.patch("/{id}", status_code=HTTPStatus.OK)
async def put_items(id: int, item: dict):
    if id not in items:
        raise HTTPException(status_code=404, detail="id not in items")

    old_item = items[id]

    if old_item.status_delete == True:
        raise HTTPException(status_code=304, detail="Item not modified")

    invalid_keys = set(item.keys()) - set(old_item.model_dump().keys())

    if invalid_keys:
        raise HTTPException(status_code=422, detail="Wrong field")

    # pattern for update data
    name = item.get("name", old_item.name)
    price = item.get("price", old_item.price)
    deleted = item.get("deleted", old_item.delete)

    items[id] = Items(id=id, name=name, price=price, deleted=deleted)

    if old_item.deleted != items[id].deleted:
        raise HTTPException(status_code=422, detail="status connot be changed")

    return items[id]


@router_item.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_it(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="id not in items")

    items[id].deleted = True

    return items[id]