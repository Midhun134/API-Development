from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix="/users",
                   tags=['users']) #tags for categorising each functions into users and post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserValidate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserValidate)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return user