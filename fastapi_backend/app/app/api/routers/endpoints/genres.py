from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List

from app import crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.get("/genres/", response_model=List[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    genres = crud.get_genres(db, skip=skip, limit=limit)
    return genres


@router.get("/genres/{genre_id}/", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(deps.get_db)):
    genre = crud.get_genre(db=db, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.get("/genres/{genre_id}/books/", response_model=List[schemas.Book])
def read_genre_books(genre_id: int, db: Session = Depends(deps.get_db)):
    genre = crud.get_genre(db=db, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre.books


@router.delete("/genres/{genre_id}/")
def delete_genre(genre_id: int, db: Session = Depends(deps.get_db)):
    genre = crud.get_genre(db=db, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return crud.delete_genre(db=db, genre=genre)
