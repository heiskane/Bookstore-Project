from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import timedelta, date

from app import schemas
from app import crud
from app.api import deps
from app.core import security
from app.core.config import settings
from app.PayPal.CreateOrder import CreateOrder
from app.PayPal.CaptureOrder import CaptureOrder
from app.PayPal.GetOrder import GetOrder

router = APIRouter()

@router.post("/checkout/paypal/order/create/")
def paypal_create_order(shopping_cart: schemas.ShoppingCart, db: Session = Depends(deps.get_db)):
	books = []
	for book_id in shopping_cart.book_ids:
		db_book = crud.get_book(db=db, book_id=book_id)
		books.append(db_book) if db_book else False

	# this errors if price is not above zero
	return CreateOrder().create_order(books=books, debug=settings.DEBUG)


@router.post("/checkout/paypal/order/{order_id}/capture/")
def paypal_capture_order(order_id: str, curr_user: schemas.User = Depends(deps.get_current_user_or_none), db: Session = Depends(deps.get_db)):
	response = CaptureOrder().capture_order(order_id, debug=settings.DEBUG)
	order = GetOrder().get_order(order_id = order_id)

	ordered_books = []
	for book in order.result.purchase_units[0].items:
		ordered_books.append(crud.get_book_by_title(db=db, title=book.name))

	# Maybe implement this in a function

	if not curr_user:
		access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
		access_token = security.create_access_token(
			data={
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
		order_date=date.today(),
		total_price=total_price
	)

	crud.create_order_record(db=db, order=order, client=curr_user, ordered_books=ordered_books)

	return response
