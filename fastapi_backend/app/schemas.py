from typing import List, Optional

from pydantic import BaseModel, EmailStr


class BookBase(BaseModel):
	title: str
	description: Optional[str] = None
	language: Optional[str] = None
	price: float = 0
	isbn: Optional[str] = None


class BookCreate(BookBase):
	pass


class Book(BookBase):
	id: int
	author_id: int

	class Config:
		orm_mode = True


class AuthorBase(BaseModel):
	fname: str
	lname: str


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