from fastapi import APIRouter

from app.api.routers.endpoints import dev

api_router = APIRouter()
api_router.include_router(dev.router, tags=["dev"])