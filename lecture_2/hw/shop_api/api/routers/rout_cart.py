from fastapi import APIRouter, HTTPException, Response
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from lecture_2.hw.shop_api.shop.cart import Cart
from lecture_2.hw.shop_api.api.routers.rout_item import items
from lecture_2.hw.shop_api.shop.Items_in_cart import Items_In_Cart
from http import HTTPStatus

router_cart = APIRouter(prefix="/cart")

carts = {}

def generate_id_carts(carts: dict):
    return max(carts.keys(), default=0) + 1


@router_cart.post("")
async def create_cart(response: Response):
    id_cart = generate_id_carts(carts)
    carts[id_cart] = Cart(id=id_cart, items=[], price=0)
    response.headers["location"] = f"/cart/{id_cart}"
    response.status_code = HTTPStatus.CREATED

    return {"id": id_cart}


@router_cart.get("/{id}", status_code=HTTPStatus.OK)
async def get_cart(id: int):
    if id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    return {"cart": carts[id]}


@router_cart.get("", status_code=HTTPStatus.OK)
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


@router_cart.post("/{cart_id}/add/{item_id}", status_code=HTTPStatus.OK)
async def add_item_in_cart(cart_id: int, item_id: int):
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="cart id not found")
    if item_id not in items:
        raise HTTPException(status_code=404, detail="item id not found")

    cart = carts[cart_id]
    item = items[item_id]

    for it in cart.items:
        if it.id == item.id:
            it.quantity += 1
            cart.price += item.price

            return {"message": "quantity increased", "cart": cart}

    cart.items.append(
        Items_In_Cart(
            id=item.id, name=item.name, quantity=1, available=not item.deleted
        )
    )
    cart.price += item.price

    return {"message": "Item added to cart", "cart": cart}