from fastapi import APIRouter, status
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from hw.shop_api.shop.Items import ItemCreate
from hw.shop_api.shop.response_mod import ItemsResponse, ItemListResponse
from hw.shop_api.api.repositories.item_repositoriy import ItemRepositoriy

router_item = APIRouter(prefix="/item", tags=["Items"])


@router_item.post("", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    return ItemRepositoriy().create_item(item)


@router_item.get("/{id}", response_model=ItemsResponse, status_code=status.HTTP_200_OK)
async def get_item(id: int):
    return ItemRepositoriy().get_item(id)


@router_item.get("", response_model=ItemListResponse, status_code=status.HTTP_200_OK)
async def get_list_items(
    offset: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    min_price: NonNegativeFloat = None,
    max_price: NonNegativeFloat = None,
    show_deleted: bool = False,
):
    return ItemRepositoriy().get_list_items(
        offset, limit, min_price, max_price, show_deleted
    )


@router_item.put("/{id}", response_model=ItemsResponse, status_code=status.HTTP_200_OK)
async def put_items(id: int, item: dict):
    return ItemRepositoriy().put_items(id, item)


@router_item.patch(
    "/{id}", response_model=ItemsResponse, status_code=status.HTTP_200_OK
)
async def put_items(id: int, item: dict):
    return ItemRepositoriy().put_items(id, item)


@router_item.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_it(id: int):

    return ItemRepositoriy().delete_it(id)
