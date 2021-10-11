from fastapi import APIRouter

from app.api.routers.endpoints import authors
from app.api.routers.endpoints import books
from app.api.routers.endpoints import checkout
from app.api.routers.endpoints import dev
from app.api.routers.endpoints import login
from app.api.routers.endpoints import orders
from app.api.routers.endpoints import reviews
from app.api.routers.endpoints import users

api_router = APIRouter()
api_router.include_router(dev.router, tags=["dev"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(books.router, tags=["books"])
api_router.include_router(reviews.router, tags=["reviews"])
api_router.include_router(authors.router, tags=["authors"])
api_router.include_router(checkout.router, tags=["checkout"])
api_router.include_router(orders.router, tags=["orders"])
