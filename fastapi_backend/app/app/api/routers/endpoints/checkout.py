from datetime import date
from datetime import timedelta
from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.PayPal.CaptureOrder import CaptureOrder
from app.PayPal.CreateOrder import CreateOrder
from app.PayPal.GetOrder import GetOrder

router = APIRouter()


@router.post("/checkout/paypal/order/create/")
def paypal_create_order(
    shopping_cart: schemas.ShoppingCart,
    curr_user: models.User = Depends(deps.get_current_user_or_none),
    db: Session = Depends(deps.get_db),
) -> Any:

    # Exclude duplicates
    uniq = list(set(shopping_cart.book_ids))

    if len(shopping_cart.book_ids) != len(uniq):
        raise HTTPException(
            status_code=400, detail="Duplicate products not allowed in shopping cart"
        )

    books = []
    for book_id in shopping_cart.book_ids:
        db_book = crud.get_book(db=db, book_id=book_id)
        books.append(db_book) if db_book else False

    total_price = sum([book.price for book in books])

    if total_price <= 0:
        raise HTTPException(status_code=400, detail="Price must be above 0")

    order = CreateOrder().create_order(books=books, debug=settings.DEBUG)

    order_id = order.result._dict["id"]  # type: ignore[attr-defined]

    crud.create_order_record(
        db=db,
        order_date=date.today(),
        total_price=total_price,  # type: ignore[arg-type]
        client=curr_user,
        ordered_books=books,
        order_id=order_id,
    )

    return order


@router.post("/checkout/paypal/order/{order_id}/capture/")
def paypal_capture_order(
    order_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    order = GetOrder().get_order(order_id=order_id)

    # Maybe implement this in a function
    ordered_books: List[models.Book] = []
    for book in order.result.purchase_units[0].items:  # type: ignore[attr-defined]
        db_book = crud.get_book_by_title(db=db, title=book.name)
        if not db_book:
            continue
        ordered_books.append(db_book)

    total_price = sum([book.price for book in ordered_books])

    order_id = order.result._dict["id"]  # type: ignore[attr-defined]
    db_order = crud.get_order_by_order_id(db=db, order_id=order_id)
    client = db_order.client

    print(client)

    if not client:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_anon_buyer_token(
            ordered_books,
            expires_delta=access_token_expires,
        )
        # Find a better way to do this later
        CaptureOrder().capture_order(order_id, debug=settings.DEBUG)
        crud.complete_order(db=db, order=db_order)
        return {"access_token": access_token, "token_type": "bearer"}

    crud.complete_order(db=db, order=db_order)

    client.books += ordered_books  # type: ignore[operator]
    db.add(client)
    db.commit()
    db.refresh(client)

    return CaptureOrder().capture_order(order_id, debug=settings.DEBUG)


@router.get("/mobile/checkout/paypal/order/capture/")
def paypal_capture_mobile_order(
    token: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    order = GetOrder().get_order(order_id=token)

    ordered_books: List[models.Book] = []
    for book in order.result.purchase_units[0].items:  # type: ignore[attr-defined]
        db_book = crud.get_book_by_title(db=db, title=book.name)
        if not db_book:
            continue
        ordered_books.append(db_book)

    total_price = sum([book.price for book in ordered_books])

    order_id = order.result._dict["id"]  # type: ignore[attr-defined]
    db_order = crud.get_order_by_order_id(db=db, order_id=order_id)
    client = db_order.client

    crud.complete_order(db=db, order=db_order)

    client.books += ordered_books  # type: ignore[operator]
    db.add(client)
    db.commit()
    db.refresh(client)

    return CaptureOrder().capture_order(token, debug=settings.DEBUG)
