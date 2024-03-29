from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.api import deps

router = APIRouter()


@router.post("/books/", response_model=schemas.Book)
def create_book(
    authors: List[str],
    genres: List[schemas.GenreCreate],
    book: schemas.BookCreate,
    db: Session = Depends(deps.get_db),
    curr_user: schemas.User = Depends(deps.require_admin),
) -> Any:
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400, detail="Book with this tile already exists"
        )

    uniq = list(set(authors))

    if len(uniq) != len(authors):
        raise HTTPException(
            status_code=400,
            detail=f"Duplicate authors not allowed. authors: {authors}, uniq: {uniq}",
        )

    return crud.create_book(db=db, book=book, genres=genres, authors=authors)


@router.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)
) -> Any:
    return crud.get_books(db=db, skip=skip, limit=limit)


@router.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(deps.get_db)) -> Any:
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


# https://stackoverflow.com/questions/63143731/update-sqlalchemy-orm-existing-model-from-posted-pydantic-model-in-fastapi
@router.patch("/books/{book_id}/", response_model=schemas.Book)
def update_book(
    book_id: int,
    updated_book: schemas.BookUpdate,
    db: Session = Depends(deps.get_db),
    curr_user: schemas.User = Depends(deps.require_admin),
) -> Any:
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Books not found")

    return crud.update_book(db=db, book=db_book, updated_book=updated_book)


@router.delete("/books/{book_id}/")
def delete_book(
    book_id: int,
    db: Session = Depends(deps.get_db),
    curr_user: schemas.User = Depends(deps.require_admin),
) -> Any:
    book = crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.delete_book(db=db, book=book)


@router.get("/books/{book_id}/download/")
def download_book(
    book_id: int,
    curr_user: models.User = Depends(deps.get_current_user_or_none),
    ordered_books: List = Depends(deps.get_ordered_books_token),
    db: Session = Depends(deps.get_db),
) -> Response:

    book = crud.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    headers = {
        "Content-Disposition": f"attachment; filename={book.title}.pdf",
    }

    if book.price == 0:
        return Response(
            book.file, media_type="application/octet-stream", headers=headers
        )

    if not curr_user and not ordered_books:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if curr_user and not curr_user.is_admin:
        if book not in curr_user.books:  # type: ignore[operator]
            raise HTTPException(status_code=403, detail="You do not own this book")

    if ordered_books:
        if book_id not in ordered_books:
            raise HTTPException(status_code=403, detail="You have not bought this book")

    return Response(book.file, media_type="application/octet-stream", headers=headers)


@router.get("/books/{book_id}/image/")
def get_book_image(book_id: int, db: Session = Depends(deps.get_db)) -> Response:
    book = crud.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return Response(book.image, media_type="image/png")


@router.get("/books/{book_id}/reviews/", response_model=List[schemas.Review])
def read_reviews(book_id: int, db: Session = Depends(deps.get_db)) -> Any:
    book = crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book.reviews


@router.post("/books/{book_id}/reviews/", response_model=schemas.Review)
def review_book(
    book_id: int,
    review: schemas.ReviewCreate,
    curr_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:

    book = crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = crud.get_book_review_by_user(db=db, book=book, user=curr_user)
    if db_review:
        raise HTTPException(
            status_code=400, detail="You have already reviewed this book"
        )

    return crud.create_review(db=db, review=review, user=curr_user, book=book)


@router.get("/books/{book_id}/wishlist/")
def wishlist_book(
    book_id: int,
    curr_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    book = crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return crud.toggle_wishlist_book(db=db, book=book, user=curr_user)
