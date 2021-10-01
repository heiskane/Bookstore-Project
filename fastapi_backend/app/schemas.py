from typing import List, Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field

class GenreBase(BaseModel):
	name: str


class GenreCreate(GenreBase):
	# This must be here instead of 'Genre' class to avoid
	# recursion error when genre and book show eachother
	# On a second thought i might not need books here at all
	books: List['Book'] = []


class Genre(GenreBase):
	id: int

	class Config:
		orm_mode = True


class BookBase(BaseModel):
	title: str
	description: Optional[str] = None
	language: Optional[str] = None
	price: float = 0
	publication_date: date
	isbn: Optional[str] = None


class BookCreate(BookBase):
	image: str
	genres: List[str]


class Book(BookBase):
	id: int
	authors: List['Author'] # Is it better to return author names instead?
	genres: List[Genre]

	class Config:
		orm_mode = True


# https://github.com/samuelcolvin/pydantic/issues/1333
# Need this so classes can refrence each other
Genre.update_forward_refs()


class ShoppingCart(BaseModel):
	book_ids: List[int]


class AuthorBase(BaseModel):
	name: str


class AuthorCreate(AuthorBase):
	pass

class Author(AuthorBase):
	id: int
	#books: List[Book] = []

	class Config:
		orm_mode = True


Book.update_forward_refs()


class UserBase(BaseModel):
	username: str
	email: Optional[EmailStr] = None


class UserCreate(UserBase):
	password: str


class User(UserBase):
	id: int
	is_active: Optional[bool] = True
	is_admin: Optional[bool] = False

	class Config:
		orm_mode = True


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None