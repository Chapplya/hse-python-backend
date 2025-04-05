from fastapi import APIRouter, HTTPException, Response, status
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from lecture_2.hw.shop_api.shop.cart import Cart
from lecture_2.hw.shop_api.shop.response_mod import CartResponse
from lecture_2.hw.shop_api.api.routers.rout_item import items
from lecture_2.hw.shop_api.shop.Items_in_cart import ItemsInCart
import uuid

router_cart = APIRouter(prefix="/cart", tags=["Carts"])

carts = {}


def generate_id_carts():
    return str(uuid.uuid4())


@router_cart.post("")
async def create_cart(response: Response):
    id_cart = generate_id_carts()
    carts[id_cart] = Cart(id=id_cart, items=[], price=0)
    response.headers["location"] = f"/cart/{id_cart}"
    response.status_code = status.HTTP_201_CREATED

    return {"id1": id_cart}


@router_cart.get("/{id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart(id: str):
    if id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    return CartResponse(**carts[id].dict())


@router_cart.get("", response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_cart_param(
    offset: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    min_price: NonNegativeFloat = None,
    max_price: NonNegativeFloat = None,
    min_quantity: NonNegativeInt = None,
    max_quantity: NonNegativeInt = None,
):
    carts_val = list(carts.values())

    if min_price is not None:
        carts_val = [obj for obj in carts_val if obj.price >= min_price]
    if max_price is not None:
        carts_val = [obj for obj in carts_val if obj.price <= max_price]
    if min_quantity is not None:
        carts_val = [
            obj
            for obj in carts_val
            if sum(item.quantity for item in obj.items) >= min_quantity
        ]
    if max_quantity is not None:
        carts_val = [
            obj
            for obj in carts_val
            if sum(item.quantity for item in obj.items) <= max_quantity
        ]
    carts_val = carts_val[offset : offset + limit]

    response = [
        {
            "id": obj.id,
            "quantity": sum(item.quantity for item in obj.items),
            "price": obj.price,
        }
        for obj in carts_val
    ]

    return response


@router_cart.post(
    "/{cart_id}/add/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_item_in_cart(cart_id: str, item_id: str):
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="cart id not found")
    if item_id not in items:
        raise HTTPException(status_code=404, detail="item id not found")
    if item_id in items and items[item_id].deleted:
        raise HTTPException(status_code=404, detail="item has been deleted")

    cart = carts[cart_id]
    item = items[item_id]

    for it in cart.items:
        if it.id == item.id:
            it.quantity += 1
            cart.price += item.price

            return CartResponse(
                id=cart_id,
                items=[ItemsInCart(**elem.dict()) for elem in cart.items],
                price=cart.price,
            )

    cart.items.append(
        ItemsInCart(id=item.id, name=item.name, quantity=1, available=not item.deleted)
    )
    cart.price += item.price

    return CartResponse(
        id=cart_id,
        items=[ItemsInCart(**elem.dict()) for elem in cart.items],
        price=cart.price,
    )
