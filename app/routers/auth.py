from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, utils, models, oauth2

router = APIRouter(
    prefix="/auth",
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Credentials")

    if not utils.verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Credentials")

    access_token = oauth2.create_access_token(data={"user_id": db_user.id})

    return {"access_token": access_token, "token_type": "bearer"}

