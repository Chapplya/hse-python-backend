from fastapi import HTTPException
from lecture_2.hw.shop_api.shop.response_mod import CartResponse
from lecture_2.hw.shop_api.api.repositories.item_repositoriy import items
from lecture_2.hw.shop_api.api.repositories.cart_repositoriy import carts
from lecture_2.hw.shop_api.shop.Items_in_cart import ItemsInCart


class CartItemRepositoriy:
    def add_item_in_cart(self, cart_id: str, item_id: str):
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
            ItemsInCart(
                id=item.id, name=item.name, quantity=1, available=not item.deleted
            )
        )
        cart.price += item.price

        return CartResponse(
            id=cart_id,
            items=[ItemsInCart(**elem.dict()) for elem in cart.items],
            price=cart.price,
        )
