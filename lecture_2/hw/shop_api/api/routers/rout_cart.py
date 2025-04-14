from fastapi import APIRouter, Response, status
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from hw.shop_api.shop.response_mod import CartResponse
from hw.shop_api.api.repositories.cart_repositoriy import CartRepositoriy
from hw.shop_api.api.repositories.cart_item_repositoriy import (
    CartItemRepositoriy,
)

router_cart = APIRouter(prefix="/cart", tags=["Carts"])


@router_cart.post("")
async def create_cart(response: Response):
    return CartRepositoriy().create_cart(response)


@router_cart.get("/{id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart(id: str):
    return CartRepositoriy().get_cart(id)


@router_cart.get("", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart_param(
    offset: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    min_price: NonNegativeFloat = None,
    max_price: NonNegativeFloat = None,
    min_quantity: NonNegativeInt = None,
    max_quantity: NonNegativeInt = None,
):
    return CartRepositoriy().get_cart_param(
        offset,
        limit,
        min_price,
        max_price,
        min_quantity,
        max_quantity,
    )


@router_cart.post(
    "/{cart_id}/add/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_item_in_cart(cart_id: str, item_id: str):
    return CartItemRepositoriy().add_item_in_cart(cart_id=cart_id, item_id=item_id)
