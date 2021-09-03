from sqlalchemy.orm import Session
from sqlalchemy import func, and_
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
		username=user.username,
		password_hash=password_hash,
		is_active = True,
		is_admin = False,
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def get_author(db: Session, author_id: int):
	return db.query(models.Author).filter(models.Author.id == author_id).first()



def get_genre_by_name(db: Session, name: str):
	return db.query(models.Genre).filter(
		func.lower(models.Genre.name) == name.lower()
	).first()


def create_genre(db: Session, genre: schemas.GenreCreate):
	db_genre = models.Genre(**genre.dict())
	db.add(db_genre)
	db.commit()
	db.refresh(db_genre)
	return db_genre


def get_authors(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_names(db: Session, names: List[str]):
	# Not sure if this is good enough performance
	db_authors = db.query(models.Author).all()

	# Names are capitalized when added to db so do the same here
	names = [name.capitalize() for name in names]

	db_author_found = None
	for db_author in db_authors:
		db_author_found = db_author if db_author.names == names else None

	return db_author_found


def create_authors(db: Session, authors: List[schemas.AuthorCreate]):
	new_authors = []
	for author in authors:
		db_author = get_author_by_names(db=db, names=author.names)
		if not db_author:
			# Capitalize first letter in names in case some madman doesnt do that
			# Also makes uniquenes fairly reliable assuming it would be used by admin only
			author.names = [name.capitalize() for name in author.names]
			author = models.Author(**author.dict())
			db.add(author)
			db.commit()
			db.refresh(author)
			new_authors.append(author)

	return new_authors


					# Maybe call skip 'page' and set offset as page * limit
					# or let frontend decide pagesize
					# Or rename 'skip' and 'limit' to 'page' and 'page_size'
					# Then set offset as (page * pagesize) and limit as page_size
def get_books(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str):
	return db.query(models.Book).filter(func.lower(models.Book.title) == title.lower()).first()


def create_book(db: Session, book: schemas.BookCreate, authors: List[schemas.AuthorCreate]):
	
	# Get existing genres and create the new ones
	db_genres = []
	for genre_name in book.genres:
		db_genre = get_genre_by_name(db=db, name=genre_name)
		if not db_genre:
			db_genres.append(create_genre(db=db, genre=schemas.GenreCreate(name=genre_name)))
		else:
			db_genres.append(db_genre)

	authors = create_authors(db=db, authors=authors)

	# Empty out List[str] so that **book.dict() works
	book.genres = []
	db_book = models.Book(**book.dict(), authors=authors)

	db_book.genres = db_genres
	db.add(db_book)
	db.commit()
	db.refresh(db_book)
	return db_book