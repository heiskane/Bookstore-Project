from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Author(Base):
	__tablename__ = "authors"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)

	books = relationship("Book", back_populates="author")


class Book(Base):
	__tablename__ = "books"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String, index=True)
	author_id = Column(Integer, ForeignKey("authors.id"))

	author = relationship("Author", back_populates="books")


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True)
	password_hash = Column(String, index=True)