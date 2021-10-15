from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app import models


async def get_all_books(session: Session) -> List[models.Book]:
    stmt = (
        select(models.Book)
        .options(joinedload(models.Book.authors))
        .options(joinedload(models.Book.genres))
    )
    result = await session.execute(stmt)
    return [book for book in result.unique().scalars()]
