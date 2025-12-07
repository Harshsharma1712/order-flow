from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.shop_router import router as shop_router
from app.routers.item_router import router as item_router
from app.routers.order_router import router as order_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(shop_router)
app.include_router(item_router)
app.include_router(order_router)

@app.get("/")
def home():
    return {"message": "This is home"}

