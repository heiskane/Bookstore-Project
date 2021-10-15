from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import async_crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.get("/async_books/", response_model=List[schemas.Book])
async def read_books(session: AsyncSession = Depends(deps.get_async_db)) -> Any:
    return await async_crud.get_all_books(session=session)
