from typing import List, Optional

from pydantic import BaseModel, EmailStr


class GenreBase(BaseModel):
	name: str


class GenreCreate(GenreBase):
	# This must be here instead of 'Genre' class to avoid 
	# recursion error when genre and book show eachother
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
	isbn: Optional[str] = None


class BookCreate(BookBase):
	genres: List[str]


class Book(BookBase):
	id: int
	author_id: int # Is it better to return author names instead?
	genres: List[Genre] = []

	class Config:
		orm_mode = True


# https://github.com/samuelcolvin/pydantic/issues/1333
# Need this so classes can refrence each other
Genre.update_forward_refs()


class AuthorBase(BaseModel):
	names: List[str] = []


class AuthorCreate(AuthorBase):
	pass


class Author(AuthorBase):
	id: int
	books: List[Book] = []

	class Config:
		orm_mode = True


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