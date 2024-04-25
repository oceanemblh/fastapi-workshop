from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, get_db
from sqlalchemy import Column, Integer, String, ForeignKey
import schemas, models


route = APIRouter()


# Add new user

@route.post("/users")
def add_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(name = request.name,
                           birthday =  request.birthday,
                           gender = request.gender,
                           email = request.email,
                        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Retrieve a list of all users:

@route.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# Retrieve details for a specific user:

@route.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update an existing user:

# delete an existing user:
