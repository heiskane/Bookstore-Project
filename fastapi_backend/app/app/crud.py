from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

from passlib.context import CryptContext  # type: ignore[import]
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models
from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def get_user_by_name(db: Session, username: str) -> Optional[models.User]:
    return (
        db.query(models.User)
        .filter(func.lower(models.User.username) == username.lower())
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    password_hash = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=password_hash,
        is_active=True,
        is_admin=False,
        register_date=datetime.today(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_genre(db: Session, genre_id: int) -> Optional[models.Genre]:
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def get_genres(db: Session, skip: int = 0, limit: int = 100) -> List[models.Genre]:
    return db.query(models.Genre).offset(skip).limit(limit).all()


def get_genre_by_name(db: Session, name: str) -> Optional[models.Genre]:
    return (
        db.query(models.Genre)
        .filter(func.lower(models.Genre.name) == name.lower())
        .first()
    )


def delete_genre(db: Session, genre: models.Genre) -> None:
    db.delete(genre)
    db.commit()
    return


def create_genre(db: Session, genre: schemas.GenreCreate) -> models.Genre:
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def create_genres_if_not_exists(
    db: Session, genres: List[schemas.GenreCreate]
) -> List[models.Genre]:
    # Get existing genres and create the new ones
    db_genres = []
    for genre in genres:
        db_genre = get_genre_by_name(db=db, name=genre.name)

        if not db_genre:
            db_genres.append(
                create_genre(db=db, genre=schemas.GenreCreate(name=genre.name))
            )
            continue

        db_genres.append(db_genre)

    return db_genres


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> Optional[models.Author]:
    return (
        db.query(models.Author)
        .filter(func.lower(models.Author.name) == name.lower())
        .first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = get_author_by_name(db=db, name=author.name)
    if not db_author:
        db_author = models.Author(**author.dict())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    return db_author


# https://stackoverflow.com/questions/26643727/python-sqlalchemy-deleting-with-the-session-object
def delete_author(db: Session, author: models.Author) -> None:
    db.delete(author)
    db.commit()
    return


def create_authors_if_not_exists(
    db: Session, authors: List[str]
) -> List[models.Author]:
    db_authors = []
    for author_name in authors:
        db_author = get_author_by_name(db=db, name=author_name)

        if not db_author:
            db_authors.append(
                create_author(db=db, author=schemas.AuthorCreate(name=author_name))
            )
            continue

        db_authors.append(db_author)

    return db_authors


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    # Maybe call skip 'page' and set offset as page * limit
    # or let frontend decide pagesize
    # Or rename 'skip' and 'limit' to 'page' and 'page_size'
    # Then set offset as (page * pagesize) and limit as page_size
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_title(db: Session, title: str) -> Optional[models.Book]:
    return (
        db.query(models.Book)
        .filter(func.lower(models.Book.title) == title.lower())
        .first()
    )


def delete_book(db: Session, book: models.Book) -> None:
    db.delete(book)
    db.commit()
    return


# https://stackoverflow.com/questions/63143731/update-sqlalchemy-orm-existing-model-from-posted-pydantic-model-in-fastapi
def update_book(
    db: Session, book: models.Book, updated_book: schemas.BookUpdate
) -> models.Book:
    for var, value in vars(updated_book).items():
        setattr(book, var, value) if value else None

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def create_book(
    db: Session,
    book: schemas.BookCreate,
    authors: List[str],
    genres: List[schemas.GenreCreate],
) -> models.Book:

    # Get existing genres and create the new ones
    db_genres = create_genres_if_not_exists(db=db, genres=genres)

    db_authors = create_authors_if_not_exists(db=db, authors=authors)

    db_book = models.Book(**book.dict())

    # MyPy doesnt Like this for some reason
    # Probably just lack of support for orm stuff
    # TODO: Fix bug when genres or authors has duplicates
    db_book.genres = db_genres  # type: ignore[assignment]
    db_book.authors = db_authors  # type: ignore[assignment]

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def toggle_wishlist_book(db: Session, book: models.Book, user: models.User):
    if not user.wishlist:
        wishlist = models.Wishlist()
        user.wishlist = wishlist

    if book not in user.wishlist.books:
        # Book needs to be iterable for some reason
        user.wishlist.books.append(book)
    else:
        # https://stackoverflow.com/questions/10378468/deleting-an-object-from-collection-in-sqlalchemy
        user.wishlist.books.remove(book)

    db.add(user)
    db.commit()
    return


def create_review(
    db: Session, review: schemas.ReviewCreate, user: models.User, book: models.Book
) -> models.Review:
    db_review = models.Review(**review.dict())
    db_review.user = user
    db_review.book = book
    db_review.review_date = datetime.today()
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review(db: Session, review_id: int) -> Optional[models.Review]:
    return db.query(models.Review).filter(models.Review.id == review_id).first()


def get_book_review_by_user(
    db: Session, book: models.Book, user: models.User
) -> Optional[models.Review]:
    return (
        db.query(models.Review)
        .filter(models.Review.user == user, models.Review.book == book)
        .first()
    )


def update_review(
    db: Session, review: models.Review, updated_review: schemas.ReviewCreate
) -> models.Review:
    for var, value in vars(updated_review).items():
        setattr(review, var, value) if value else None

    review.edited = True
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def delete_review(db: Session, review: models.Review) -> None:
    db.delete(review)
    db.commit()
    return


def create_order_record(
    db: Session,
    order_date: date,
    order_id: str,
    total_price: float,
    ordered_books: List[models.Book],
    client: Optional[models.User] = None,
) -> models.Order:

    db_order = models.Order(
        completed=False,
        order_date=order_date,
        order_id=order_id,
        total_price=total_price,
        ordered_books=ordered_books,
    )

    if client:
        db_order.client = client

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def complete_order(db: Session, order: models.Order):
    order.completed = True
    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def get_order_by_order_id(db: Session, order_id: str):
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    return db.query(models.Order).offset(skip).limit(limit).all()
