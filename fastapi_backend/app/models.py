from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Author(Base):
	__tablename__ = "authors"

	id = Column(Integer, primary_key=True, index=True)
	fname = Column(String, index=True)
	lname = Column(String, index=True)

	books = relationship("Book", back_populates="author")


class Book(Base):
	__tablename__ = "books"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String, index=True)
	language = Column(String, index=True)
	price = Column(Float, index=True)
	publisher = Column(String, index=True)
	isbn = Column(String, index=True)

	author_id = Column(Integer, ForeignKey("authors.id"))

	author = relationship("Author", back_populates="books")


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True) # Set to unique later
	password_hash = Column(String, index=True)
	email = Column(String, index=True) # Set to unique later
	is_admin = Column(Boolean, index=True)
	is_active = Column(Boolean, index=True)