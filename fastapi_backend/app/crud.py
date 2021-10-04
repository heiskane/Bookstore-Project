from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext

from typing import List

from . import models, schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def get_user_by_name(db: Session, username: str):
	return db.query(models.User).filter(func.lower(models.User.username) == username.lower()).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
	password_hash = pwd_context.hash(user.password)
	db_user = models.User(
		username = user.username,
		password_hash = password_hash,
		is_active = True,
		is_admin = False,
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def get_author(db: Session, author_id: int):
	return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_genre(db: Session, genre_id: int):
	return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def get_genres(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Genre).offset(skip).limit(limit).all()


def get_genre_by_name(db: Session, name: str):
	return db.query(models.Genre).filter(
		func.lower(models.Genre.name) == name.lower()
	).first()


def delete_genre(db: Session, genre: models.Genre):
	db.delete(genre)
	db.commit()
	return


def create_genre(db: Session, genre: schemas.GenreCreate):
	db_genre = models.Genre(**genre.dict())
	db.add(db_genre)
	db.commit()
	db.refresh(db_genre)
	return db_genre


def create_genres_if_not_exists(db: Session, genres: List[str]):
	# Get existing genres and create the new ones
	db_genres = []
	for genre_name in genres:
		db_genre = get_genre_by_name(db=db, name=genre_name)

		if not db_genre:
			db_genres.append(create_genre(db=db, genre=schemas.GenreCreate(name=genre_name)))
			continue
		
		db_genres.append(db_genre)

	return db_genres


def get_authors(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str):
	return db.query(models.Author).filter(func.lower(models.Author.name) == name.lower()).first()


def create_author(db: Session, author: schemas.AuthorCreate):
	db_author = get_author_by_name(db=db, name=author.name)
	if not db_author:
		db_author = models.Author(**author.dict())
		db.add(db_author)
		db.commit()
		db.refresh(db_author)
	return db_author


# https://stackoverflow.com/questions/26643727/python-sqlalchemy-deleting-with-the-session-object
def delete_author(db: Session, author: models.Author):
	db.delete(author)
	db.commit()
	return


def create_authors_if_not_exists(db: Session, authors: List[str]):
	db_authors = []
	for author_name in authors:
		db_author = get_author_by_name(db=db, name=author_name)

		if not db_author:
			db_authors.append(create_author(db=db, author=schemas.AuthorCreate(name=author_name)))
			continue

		db_authors.append(db_author)

	return db_authors


def get_books(db: Session, skip: int = 0, limit: int = 100):
	# Maybe call skip 'page' and set offset as page * limit
	# or let frontend decide pagesize
	# Or rename 'skip' and 'limit' to 'page' and 'page_size'
	# Then set offset as (page * pagesize) and limit as page_size
	return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
	return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_title(db: Session, title: str):
	return db.query(models.Book).filter(func.lower(models.Book.title) == title.lower()).first()


def delete_book(db: Session, book: models.Book):
	db.delete(book)
	db.commit()
	return


# https://stackoverflow.com/questions/63143731/update-sqlalchemy-orm-existing-model-from-posted-pydantic-model-in-fastapi
def update_book(db: Session, book: models.Book, updated_book: schemas.BookUpdate):
	for var, value in vars(updated_book).items():
		setattr(book, var, value) if value else None

	db.add(book)
	db.commit()
	db.refresh(book)
	return book


def create_book(db: Session, book: schemas.BookCreate, authors: List[str]):
	
	# Get existing genres and create the new ones
	db_genres = create_genres_if_not_exists(db=db, genres=book.genres)
	book.genres = db_genres

	db_authors = create_authors_if_not_exists(db=db, authors=authors)

	db_book = models.Book(**book.dict(), authors=db_authors)

	db.add(db_book)
	db.commit()
	db.refresh(db_book)
	return db_book



def create_order_record(
		db: Session, order: schemas.OrderCreate,
		client: models.User,
		ordered_books: List[models.Book]):

	db_order = models.Order(**order.dict())
	db_order.client = client
	db_order.ordered_books = ordered_books

	db.add(db_order)
	db.commit()
	db.refresh(db_order)

	return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Order).offset(skip).limit(limit).all()
