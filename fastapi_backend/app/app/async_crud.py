from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from app import models


async def get_all_books(session: Session) -> List[models.Book]:
    stmt = select(models.Book).options(
        joinedload(models.Book.authors)).options(
        joinedload(models.Book.genres))
    result = await session.execute(stmt)
    #print([book for book in result.unique()])
    print(type(result))
    return [book for book in result.unique().scalars()]
