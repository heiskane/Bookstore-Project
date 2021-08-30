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
