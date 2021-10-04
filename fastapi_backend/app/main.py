from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import Response
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, date
from base64 import decodebytes
from binascii import Error
from magic import from_buffer

from . import crud, models, schemas
from .database import SessionLocal, engine
from .PayPal.CreateOrder import CreateOrder
from .PayPal.CaptureOrder import CaptureOrder
from .PayPal.GetOrder import GetOrder

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

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Remember to change later and use .env
SECRET_KEY = "a155c5104f0f8fcc9c2c2506588a218476c72fb0c40897f3f93d501c75c8db32"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

DEBUG = True

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def verify_password(password_plain: str, password_hash: str):
	return pwd_context.verify(password_plain, password_hash)


def authenticate_user(db: Session, username: str, password: str):
	db_user = crud.get_user_by_name(db=db, username=username)
	if not db_user:
		return False
	if not verify_password(password, db_user.password_hash):
		return False
	return db_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=30)):
	to_encode = data.copy()
	expire = datetime.utcnow() + expires_delta
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	credentials_exception = HTTPException(
		status_code=401,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = schemas.TokenData(username=username)
	except JWTError:
		raise credentials_exception
	user = crud.get_user_by_name(db=db, username=token_data.username)
	if user is None:
		raise credentials_exception
	return user


# https://stackoverflow.com/questions/66254024/fastapi-optional-oauth2-authentication
async def get_current_user_or_none(db: Session = Depends(get_db), token: str = Depends(optional_oauth2_scheme)):
	if not token:
		return None
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			return None
		token_data = schemas.TokenData(username=username)
	except JWTError:
		return None
	user = crud.get_user_by_name(db=db, username=token_data.username)
	return user


def get_ordered_books_token(token: str = Depends(optional_oauth2_scheme)):
	if not token:
		return None

	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		ordered_books: str = payload.get("ordered_book_ids")
		if ordered_books is None:
			return None
	except JWTError:
		return None

	return ordered_books


def require_admin(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
	user = Depends(get_current_user)):
	
	if not user.is_admin:
		raise HTTPException(status_code=401, detail="Admin privileges required")
	return user


@app.get("/admin_required/", response_model=schemas.User)
def admin_required(curr_user: schemas.User = Depends(require_admin)):
	return curr_user


# Require authentication
@app.get("/auth_required/", response_model=schemas.User)
def auth_required(curr_user: schemas.User = Depends(get_current_user)):
	return curr_user


@app.get("/auth_optional/", response_model=schemas.User)
def auth_optional(curr_user: schemas.User = Depends(get_current_user_or_none)):
	return curr_user


# Fix pls
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
	# This endpoint might not be needed
	db_author = crud.get_author_by_name(db=db, name=author.name)
	if db_author:
		raise HTTPException(status_code=400, detail="Author already exists")
	return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	authors = crud.get_authors(db, skip=skip, limit=limit)
	return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
	db_author = crud.get_author(db=db, author_id=author_id)
	if not db_author:
		raise HTTPException(status_code=404, detail="Author not found")
	return db_author


@app.delete("/authors/{author_id}/")
def delete_author(author_id: int, db: Session = Depends(get_db)):
	author = crud.get_author(db=db, author_id=author_id)
	if not author:
		raise HTTPException(status_code=404, detail="Author not found")

	crud.delete_author(db=db, author=author)
	return "asd"


@app.get("/authors/{author_id}/books", response_model=List[schemas.Book])
def read_author_books(author_id: int, db: Session = Depends(get_db)):
	db_author = crud.get_author(db=db, author_id=author_id)
	if not db_author:
		raise HTTPException(status_code=404, detail="Author not found")
	return db_author.books


@app.post("/books/", response_model=schemas.Book)
def create_book(authors: List[str], book: schemas.BookCreate, db: Session = Depends(get_db)):
	db_book = crud.get_book_by_title(db, title=book.title)
	if db_book:
		raise HTTPException(status_code=400, detail="Book with this tile already exists")

	try:
		image_file = decodebytes(book.image.encode('utf-8'))
	except Error:
		raise HTTPException(status_code=400, detail="Decoding image failed")

	# https://github.com/ahupp/python-magic
	file_type = from_buffer(image_file).split(',')[0]
	if file_type != 'PNG image data':
		raise HTTPException(status_code=400, detail='Wrong filetype for image (Has to be PNG)')
	book.image = image_file

	try:
		book_file = decodebytes(book.file.encode('utf-8'))
	except Error:
		raise HTTPException(status_code=400, detail="Decoding file failed")

	file_type = from_buffer(book_file).split(',')[0]
	if file_type != 'PDF document':
		raise HTTPException(status_code=400, detail="Wrong filetype for file (Has to be PDF)")
	book.file = book_file

	return crud.create_book(db=db, book=book, authors=authors)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
	db_book = crud.get_book(db=db, book_id=book_id)
	if not db_book:
		raise HTTPException(status_code=404, detail="Book not found")
	return db_book


@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
	book = crud.get_book(db=db, book_id=book_id)
	if not book:
		raise HTTPException(status_code=404, detail="Book not found")
	crud.delete_book(db=db, book=book)
	return


@app.get("/books/{book_id}/download/")
def download_book(
		book_id: int,
		curr_user: schemas.User = Depends(get_current_user_or_none),
		ordered_books: List = Depends(get_ordered_books_token),
		db: Session = Depends(get_db)):

	book = crud.get_book(db = db, book_id = book_id)

	if not curr_user and not ordered_books:
		raise HTTPException(status_code=403, detail="Unauthorized")

	if curr_user and not curr_user.is_admin:
		if book not in curr_user.books:
			raise HTTPException(status_code=403, detail="You do not own this book")

	if ordered_books:
		if book_id not in ordered_books:
			raise HTTPException(status_code=403, detail="You have not bought this book")

	headers = {"Content-Disposition": f"attachment; filename={book.title}.pdf"}
	return Response(book.file, media_type='application/octet-stream', headers=headers)


@app.get("/books/{book_id}/image/")
def get_book_image(book_id: int, db: Session = Depends(get_db)):
	book = crud.get_book(db = db, book_id = book_id)
	return Response(book.image, media_type='image/png')


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_name(db=db, username=user.username)
	if db_user:
		raise HTTPException(status_code=400, detail="Username taken")
	return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/user/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
	return crud.get_user_by_name(db=db, username=username)


@app.post("/login/", response_model=schemas.Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = authenticate_user(db=db, username=form_data.username, password=form_data.password)

	if not user:
		raise HTTPException(status_code=401, detail="Login failed")

	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data = {
			"sub": user.username,
			# Probably dont need to set is_admin and is_active
			# Unless the frontend wants it
			"is_admin": user.is_admin,
			"is_active": user.is_active
		}, expires_delta=access_token_expires
	)

	token = schemas.Token(access_token=access_token)

	return token


@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_orders(db=db, skip=skip, limit=limit)


@app.post("/checkout/paypal/order/create/")
def paypal_create_order(shopping_cart: schemas.ShoppingCart, db: Session = Depends(get_db)):
	books = []
	for book_id in shopping_cart.book_ids:
		db_book = crud.get_book(db=db, book_id=book_id)
		books.append(db_book) if db_book else False

	# Error if price is not above zero
	return CreateOrder().create_order(books=books, debug=DEBUG)


@app.post("/checkout/paypal/order/{order_id}/capture/")
def paypal_capture_order(order_id: str, curr_user: schemas.User = Depends(get_current_user_or_none), db: Session = Depends(get_db)):
	response = CaptureOrder().capture_order(order_id, debug=DEBUG)
	order = GetOrder().get_order(order_id = order_id)

	ordered_books = []
	for book in order.result.purchase_units[0].items:
		ordered_books.append(crud.get_book_by_title(db = db, title = book.name))

	# Maybe implement this in a function

	if not curr_user:
		access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
		access_token = create_access_token(
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
