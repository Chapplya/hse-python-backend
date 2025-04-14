from fastapi import FastAPI
from hw.shop_api.api.routers.rout_cart import router_cart
from hw.shop_api.api.routers.rout_item import router_item
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="Shop API")

app.include_router(router_cart)
app.include_router(router_item)


Instrumentator().instrument(app).expose(app)
