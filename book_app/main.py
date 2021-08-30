from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Why does 'from . import' not work
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
	db_author = crud.get_author_by_name(db, name = author.name)
	if db_author:
		raise HTTPException(status_code=400, detail="Author already exists")
	return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	authors = crud.get_authors(db, skip=skip, limit=limit)
	return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
	db_author = crud.get_author(db=db, author_id=author_id)
	if not db_author:
		raise HTTPException(status_code=404, detail="Author not found")
	return db_author


@app.post("/authors/{author_name}/books/", response_model=schemas.Book)
def create_book(author_name: str, book: schemas.BookCreate, db: Session = Depends(get_db)):
	db_book = crud.get_book_by_title(db, title=book.title)
	if db_book:
		raise HTTPException(status_code=400, detail="Book with this tile already exists")
	db_author = crud.get_author_by_name(db=db, name=author_name)
	if not db_author:
		crud.create_author(db=db, author=schemas.AuthorCreate(name=author_name))
	return crud.create_book(db=db, book=book, author=db_author)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/")
async def root():
	return {"message": "Hello World"}
