from fastapi import APIRouter, HTTPException, status
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from lecture_2.hw.shop_api.shop.Items import Items, ItemCreate
from lecture_2.hw.shop_api.shop.response_mod import ItemsResponse, ItemListResponse
import uuid

router_item = APIRouter(prefix="/item", tags=["Items"])
items = {}


def generate_id_item():
    return str(uuid.uuid4())


@router_item.post("", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    id_item = generate_id_item()
    items[id_item] = Items(id=id_item, name=item.name, price=item.price)

    return {"item": items[id_item]}


@router_item.get("/{id}", response_model=ItemsResponse, status_code=status.HTTP_200_OK)
async def get_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Not found id")
    if items[id].deleted:
        raise HTTPException(status_code=404, detail="Items has been deleted")
    return items[id]


@router_item.get("", response_model=ItemListResponse, status_code=status.HTTP_200_OK)
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

    items_val = items_val[offset : offset + limit + 1]

    items_response = [ItemsResponse(**item.dict()) for item in items_val]

    return ItemListResponse(items=items_response)


@router_item.put("/{id}", response_model=ItemsResponse, status_code=status.HTTP_200_OK)
async def put_items(id: int, item: dict):
    if id not in items:
        raise HTTPException(status_code=404, detail="id not in items")
    items[id] = Items(id=id, name=item["name"], price=item["price"])
    return items[id]


@router_item.patch(
    "/{id}", response_model=ItemsResponse, status_code=status.HTTP_200_OK
)
async def put_items(id: int, item: dict):
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

    return items[id]


@router_item.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_it(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="id not in items")

    items[id].deleted = True

    return items[id]
