from fastapi import APIRouter

from app.api.routers.endpoints import (
    dev,
    checkout,
    books,
    authors,
    reviews,
    users,
    orders,
    login,
)

api_router = APIRouter()
api_router.include_router(dev.router, tags=["dev"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(books.router, tags=["books"])
api_router.include_router(reviews.router, tags=["reviews"])
api_router.include_router(authors.router, tags=["authors"])
api_router.include_router(checkout.router, tags=["checkout"])
api_router.include_router(orders.router, tags=["orders"])
