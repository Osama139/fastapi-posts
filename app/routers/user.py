from typing import List
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/users",
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")

@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    updated_query = db.query(models.User).filter(models.User.id == id)
    user = updated_query.first()
    if user:
        hashed_password = utils.hash(updated_user.password)
        updated_user.password = hashed_password
        updated_query.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        db.refresh(user)
        return user
    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):
    user  =db.query(models.User).filter(models.User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
        return {'message': f'Deleted post with id: {id} successfully'}
    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")

