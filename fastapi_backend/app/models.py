from sqlalchemy import Boolean, Column, ForeignKey, Integer, Date
from sqlalchemy import String, Float, Table, PickleType
from sqlalchemy.orm import relationship

from .database import Base


book_author = Table('book_authors', Base.metadata,
	Column('author_id', ForeignKey('authors.id'), primary_key=True),
	Column('book_id', ForeignKey('books.id'), primary_key=True)
)


class Author(Base):
	__tablename__ = "authors"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True, unique=True)

	books = relationship(
		"Book",
		secondary=book_author,
		back_populates="authors"
	)


book_genre = Table('book_genres', Base.metadata,
	Column('book_id', ForeignKey('books.id'), primary_key=True),
	Column('genre_id', ForeignKey('genres.id'), primary_key=True)
)


class Genre(Base):
	__tablename__ = "genres"

	id = Column(Integer, primary_key=True)
	name = Column(String, index=True)

	books = relationship(
		"Book",
		secondary=book_genre,
		back_populates="genres"
	)


class Book(Base):
	__tablename__ = "books"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String, index=True)
	language = Column(String, index=True)
	price = Column(Float, index=True)
	publication_date = Column(Date, index=True)
	#publisher = Column(String, index=True)
	isbn = Column(String, index=True)

	authors = relationship(
		"Author",
		secondary=book_author,
		back_populates="books"
	)

	genres = relationship(
		"Genre",
		secondary=book_genre,
		back_populates="books"
	)


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True) # Set to unique later
	password_hash = Column(String, index=True)
	email = Column(String, index=True) # Set to unique later
	is_admin = Column(Boolean, index=True)
	is_active = Column(Boolean, index=True)
