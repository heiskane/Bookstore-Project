from base64 import decodebytes

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import aggregated  # type: ignore[import]

from .database import Base

book_author = Table(
    "book_authors",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)


book_genre = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    books = relationship("Book", secondary=book_genre, back_populates="genres")


book_ownership = Table(
    "book_ownership",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)


ordered_books = Table(
    "ordered_books",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("book_id", ForeignKey("books.id")),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    language = Column(String, index=True)
    price = Column(Float, nullable=False, index=True)
    publication_date = Column(Date, index=True)
    # publisher = Column(String, index=True)
    isbn = Column(String, index=True)

    # https://sqlalchemy-utils.readthedocs.io/en/latest/aggregates.html#average-movie-rating
    @aggregated("reviews", Column(Float))
    def avg_rating(self) -> float:
        return func.avg(Review.rating)

    reviews = relationship("Review", back_populates="book")

    # https://gist.github.com/luhn/4170996
    _image = Column(LargeBinary)

    @hybrid_property
    def image(self):
        return self._image

    @image.setter  # type: ignore[no-redef]
    def image(self, b64_image):
        image_file = decodebytes(b64_image.encode("utf-8"))
        self._image = image_file

    _file = Column(LargeBinary)

    @hybrid_property
    def file(self):
        return self._file

    @file.setter  # type: ignore[no-redef]
    def file(self, b64_file):
        self._file = decodebytes(b64_file.encode("utf-8"))

    authors = relationship("Author", secondary=book_author, back_populates="books")

    genres = relationship("Genre", secondary=book_genre, back_populates="books")

    owners = relationship("User", secondary=book_ownership, back_populates="books")

    orders = relationship(
        "Order", secondary=ordered_books, back_populates="ordered_books"
    )

    # __mapper_args__ = {"eager_defaults": True}


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    books = relationship("Book", secondary=book_author, back_populates="authors")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)  # Set to unique later
    password_hash = Column(String, nullable=False, index=True)
    email = Column(String, index=True)  # Set to unique later
    is_admin = Column(Boolean, default=False, nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    register_date = Column(Date, index=True)

    orders = relationship("Order", back_populates="client")

    books = relationship("Book", secondary=book_ownership, back_populates="owners")

    reviews = relationship("Review", back_populates="user")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, index=True)
    comment = Column(String, index=True)
    edited = Column(Boolean, default=False, index=True)
    review_date = Column(Date, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="reviews")

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="reviews")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, index=True)
    total_price = Column(Float, index=True)

    client_user_id = Column(Integer, ForeignKey("users.id"))
    client = relationship("User", back_populates="orders")

    ordered_books = relationship(
        "Book", secondary=ordered_books, back_populates="orders"
    )
