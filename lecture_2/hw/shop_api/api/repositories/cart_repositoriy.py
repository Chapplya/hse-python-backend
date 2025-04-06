from fastapi import HTTPException, Response, status
from pydantic import NonNegativeFloat, NonNegativeInt, PositiveInt
from lecture_2.hw.shop_api.shop.cart import Cart
from lecture_2.hw.shop_api.shop.response_mod import CartResponse
import uuid

carts = {}


class CartRepositoriy:

    @staticmethod
    def generate_id_carts():
        return str(uuid.uuid4())

    def create_cart(self, response: Response):
        id_cart = self.generate_id_carts()
        carts[id_cart] = Cart(id=id_cart, items=[], price=0)
        response.headers["location"] = f"/cart/{id_cart}"
        response.status_code = status.HTTP_201_CREATED

        return {"id1": id_cart}

    def get_cart(self, id: str):
        if id not in carts:
            raise HTTPException(status_code=404, detail="Cart not found")

        return CartResponse(**carts[id].dict())

    def get_cart_param(
        self,
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
