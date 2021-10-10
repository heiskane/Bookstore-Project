from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, date

from app.api.routers.api import api_router
from app import crud, models, schemas
from app.database import engine
from app.core import security
from app.core.config import settings
from app.api import deps
from app.PayPal.CreateOrder import CreateOrder
from app.PayPal.CaptureOrder import CaptureOrder
from app.PayPal.GetOrder import GetOrder

models.Base.metadata.create_all(bind=engine, checkfirst=True)

description = """

Backend API for the Bookstore project

"""

app = FastAPI(description=description)

# https://fastapi.tiangolo.com/tutorial/cors/
# Allowed origins required to allow react to communicate from "diffrent origin"
# Will have to chech if a subdomain is "diffrent origin"
origins = [
	"*",
]

# https://stackoverflow.com/questions/60680870/cors-issues-when-running-a-dockerised-fastapi-application
# for some reason without an endpoint before CORS the cors fails in docker-compose
@app.get("/")
def health_check():
	return {"detail": "I am aliiiiiive"}

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["Content-Disposition"] # Allow frontend to get filename
)


DEBUG = True

def authenticate_user(db: Session, username: str, password: str):
	db_user = crud.get_user_by_name(db=db, username=username)
	if not db_user:
		return False
	if not security.verify_password(password, db_user.password_hash):
		return False
	return db_user

app.include_router(api_router)


# Fix pls
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(deps.get_db)):
	# This endpoint might not be needed
	db_author = crud.get_author_by_name(db=db, name=author.name)
	if db_author:
		raise HTTPException(status_code=400, detail="Author already exists")
	return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
	authors = crud.get_authors(db, skip=skip, limit=limit)
	return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(deps.get_db)):
	db_author = crud.get_author(db=db, author_id=author_id)
	if not db_author:
		raise HTTPException(status_code=404, detail="Author not found")
	return db_author


@app.delete("/authors/{author_id}/")
def delete_author(author_id: int, db: Session = Depends(deps.get_db)):
	author = crud.get_author(db=db, author_id=author_id)
	if not author:
		raise HTTPException(status_code=404, detail="Author not found")

	return crud.delete_author(db=db, author=author)


@app.get("/authors/{author_id}/books", response_model=List[schemas.Book])
def read_author_books(author_id: int, db: Session = Depends(deps.get_db)):
	db_author = crud.get_author(db=db, author_id=author_id)
	if not db_author:
		raise HTTPException(status_code=404, detail="Author not found")
	return db_author.books


@app.get("/genres/", response_model=List[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
	genres = crud.get_genres(db, skip=skip, limit=limit)
	return genres


@app.get("/genres/{genre_id}/", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(deps.get_db)):
	genre = crud.get_genre(db=db, genre_id=genre_id)
	if not genre:
		raise HTTPException(status_code=404, detail="Genre not found")
	return genre


@app.get("/genres/{genre_id}/books/", response_model=List[schemas.Book])
def read_genre_books(genre_id: int, db: Session = Depends(deps.get_db)):
	genre = crud.get_genre(db=db, genre_id=genre_id)
	if not genre:
		raise HTTPException(status_code=404, detail="Genre not found")
	return genre.books


@app.delete("/genres/{genre_id}/")
def delete_genre(genre_id: int, db: Session = Depends(deps.get_db)):
	genre = crud.get_genre(db=db, genre_id=genre_id)
	if not genre:
		raise HTTPException(status_code=404, detail="Genre not found")
	return crud.delete_genre(db=db, genre=genre)


@app.post("/books/", response_model=schemas.Book)
def create_book(authors: List[str], book: schemas.BookCreate, db: Session = Depends(deps.get_db)):
	db_book = crud.get_book_by_title(db, title=book.title)
	if db_book:
		raise HTTPException(status_code=400, detail="Book with this tile already exists")

	# https://github.com/ahupp/python-magic
	#file_type = from_buffer(image_file).split(',')[0]
	#if file_type != 'PNG image data':
	#	raise HTTPException(status_code=400, detail='Wrong filetype for image (Has to be PNG)')
	#book.image = image_file

	return crud.create_book(db=db, book=book, authors=authors)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
	return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(deps.get_db)):
	db_book = crud.get_book(db=db, book_id=book_id)
	if not db_book:
		raise HTTPException(status_code=404, detail="Book not found")
	return db_book


# https://stackoverflow.com/questions/63143731/update-sqlalchemy-orm-existing-model-from-posted-pydantic-model-in-fastapi
@app.patch("/books/{book_id}/", response_model=schemas.Book)
def update_book(book_id: int, updated_book: schemas.BookUpdate, db: Session = Depends(deps.get_db)):
	db_book = crud.get_book(db=db, book_id=book_id)
	if not db_book:
		raise HTTPException(status_code=404, detail="Books not found")

	return crud.update_book(db=db, book=db_book, updated_book=updated_book)


@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(deps.get_db)):
	book = crud.get_book(db=db, book_id=book_id)
	if not book:
		raise HTTPException(status_code=404, detail="Book not found")
	return crud.delete_book(db=db, book=book)


@app.get("/books/{book_id}/download/")
def download_book(
		book_id: int,
		curr_user: schemas.User = Depends(deps.get_current_user_or_none),
		ordered_books: List = Depends(deps.get_ordered_books_token),
		db: Session = Depends(deps.get_db)):

	book = crud.get_book(db = db, book_id = book_id)

	headers = {
		"Content-Disposition": f"attachment; filename={book.title}.pdf",
	}

	if book.price == 0:
		return Response(book.file, media_type='application/octet-stream', headers=headers)

	if not curr_user and not ordered_books:
		raise HTTPException(status_code=403, detail="Unauthorized")

	if curr_user and not curr_user.is_admin:
		if book not in curr_user.books:
			raise HTTPException(status_code=403, detail="You do not own this book")

	if ordered_books:
		if book_id not in ordered_books:
			raise HTTPException(status_code=403, detail="You have not bought this book")

	return Response(book.file, media_type='application/octet-stream', headers=headers)


@app.get("/books/{book_id}/image/")
def get_book_image(book_id: int, db: Session = Depends(deps.get_db)):
	book = crud.get_book(db = db, book_id = book_id)
	return Response(book.image, media_type='image/png')


@app.get("/books/{book_id}/reviews/", response_model=List[schemas.Review])
def read_reviews(book_id: int, db: Session = Depends(deps.get_db)):
	book = crud.get_book(db=db, book_id=book_id)
	if not book:
		raise HTTPException(status_code=404, detail="Book not found")

	return book.reviews


@app.patch("/reviews/{review_id}/", response_model=schemas.Review)
def update_review(
		review_id: int,
		updated_review: schemas.ReviewCreate,
		curr_user: schemas.User = Depends(deps.get_current_user),
		db: Session = Depends(deps.get_db)):
	db_review = crud.get_review(db=db, review_id=review_id)
	if not db_review:
		raise HTTPException(status_code=404, detail="Review not found")

	if not db_review.user == curr_user and not curr_user.is_admin:
		raise HTTPException(status_code=403, detail="Unauthorized")

	return crud.update_review(db=db, review=db_review, updated_review=updated_review)


@app.delete("/reviews/{review_id}/")
def delete_review(book_id: int, review_id: int, db: Session = Depends(deps.get_db)):
	review = crud.get_review(db=db, review_id=review_id)
	return crud.delete_review(db=db, review=review)


@app.post("/books/{book_id}/reviews/", response_model=schemas.Review)
def review_book(
		book_id: int,
		review: schemas.ReviewCreate,
		curr_user: schemas.User = Depends(deps.get_current_user),
		db: Session = Depends(deps.get_db)):

	book = crud.get_book(db=db, book_id=book_id)
	if not book:
		raise HTTPException(status_code=404, detail="Book not found")

	db_review = crud.get_book_review_by_user(db=db, book=book, user=curr_user)
	if db_review:
		raise HTTPException(status_code=400, detail="You have already reviewed this book")

	return crud.create_review(db=db, review=review, user=curr_user, book=book)


@app.post("/users/", response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
	db_user = crud.get_user_by_name(db=db, username=user.username)
	if db_user:
		raise HTTPException(status_code=400, detail="Username taken")

	created_user = crud.create_user(db=db, user=user)

	# Login user when registered
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	return {
		"access_token": security.create_access_token(
			created_user, expires_delta=access_token_expires
		),
		"token_type": "bearer"
	}


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
	return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/user/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(deps.get_db)):
	return crud.get_user_by_name(db=db, username=username)


@app.post("/login/", response_model=schemas.Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
	user = authenticate_user(db=db, username=form_data.username, password=form_data.password)

	if not user:
		raise HTTPException(status_code=401, detail="Login failed")

	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Change later

	return {
		"access_token": security.create_access_token(
			user, expires_delta=access_token_expires
		),
		"token_type": "bearer"
	}


@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
	return crud.get_orders(db=db, skip=skip, limit=limit)


@app.post("/checkout/paypal/order/create/")
def paypal_create_order(shopping_cart: schemas.ShoppingCart, db: Session = Depends(deps.get_db)):
	books = []
	for book_id in shopping_cart.book_ids:
		db_book = crud.get_book(db=db, book_id=book_id)
		books.append(db_book) if db_book else False

	# this errors if price is not above zero
	return CreateOrder().create_order(books=books, debug=DEBUG)


@app.post("/checkout/paypal/order/{order_id}/capture/")
def paypal_capture_order(order_id: str, curr_user: schemas.User = Depends(deps.get_current_user_or_none), db: Session = Depends(deps.get_db)):
	response = CaptureOrder().capture_order(order_id, debug=DEBUG)
	order = GetOrder().get_order(order_id = order_id)

	ordered_books = []
	for book in order.result.purchase_units[0].items:
		ordered_books.append(crud.get_book_by_title(db = db, title = book.name))

	# Maybe implement this in a function

	if not curr_user:
		access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
		access_token = security.create_access_token(
			data = {
				"sub": "anonymous",
				"ordered_book_ids": [book.id for book in ordered_books],
			}, expires_delta=access_token_expires
		)
		return {"access_token": access_token, "token_type": "bearer"}

	curr_user.books += ordered_books
	db.add(curr_user)
	db.commit()
	db.refresh(curr_user)

	total_price = sum([book.price for book in ordered_books])

	# TODO: Track orders for anonymous users
	order = schemas.OrderCreate(
		order_date = date.today(),
		total_price = total_price
	)

	crud.create_order_record(db=db, order=order, client=curr_user, ordered_books=ordered_books)

	return response
