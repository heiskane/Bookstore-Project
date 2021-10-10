from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app import crud
from app import schemas
from app.api import deps

router = APIRouter()

@router.patch("/reviews/{review_id}/", response_model=schemas.Review)
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


@router.delete("/reviews/{review_id}/")
def delete_review(book_id: int, review_id: int, db: Session = Depends(deps.get_db)):
	review = crud.get_review(db=db, review_id=review_id)
	return crud.delete_review(db=db, review=review)
