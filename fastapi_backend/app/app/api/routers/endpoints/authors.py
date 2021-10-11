from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List

from app import crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(deps.get_db)):
    # This endpoint might not be needed
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@router.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@router.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(deps.get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.delete("/authors/{author_id}/")
def delete_author(author_id: int, db: Session = Depends(deps.get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.delete_author(db=db, author=author)


@router.get("/authors/{author_id}/books", response_model=List[schemas.Book])
def read_author_books(author_id: int, db: Session = Depends(deps.get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author.books
