from typing import List, Optional

from pydantic import BaseModel


class BookBase(BaseModel):
	title: str
	description: Optional[str] = None


class BookCreate(BookBase):
	pass


class Book(BookBase):
	id: int
	author_id: int

	class Config:
		orm_mode = True


class AuthorBase(BaseModel):
	name: str


class AuthorCreate(AuthorBase):
	pass


class Author(AuthorBase):
	id: int
	books: List[Book] = []

	class Config:
		orm_mode = True


class UserBase(BaseModel):
	username: str


class UserCreate(UserBase):
	password: str


class User(UserBase):
	id: int

	class Config:
		orm_mode = True


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None