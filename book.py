from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, get_db
from sqlalchemy import Column, Integer, String, ForeignKey
import schemas, models


route = APIRouter()




# Add new book
@route.post("/books")
def add_book(request: schemas.book, db: Session = Depends(get_db)):
    
    new_book = models.book (title = request.title,
                           author =  request.author,
                           description = request.description,
                           published_year = request.published_year,
                           publisher = request.publisher
                        )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

# Retrieve a list of all books:

@route.get("/book")
def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.book).all()

# Retrieve details for a specific book:

@route.get("/books/{book_id}")
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.book).filter(models.book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="book not found") # Catch de l'exception si le livre est introuvable
    return book

# Update an existing book:

@route.put("/books/{book_id}")
def update_book(book_id: int, request: schemas.book, db: Session = Depends(get_db)):
    # Récupération du livre dans base de données
    book = db.query(models.book).filter(models.book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="book not found") # Catch de l'exception si le livre est introuvable
    
    # Mise à jour des champs du livre avec les nouvelles données
    for field, value in request.dict().items():
        setattr(book, field, value)
    
    # Mise à jour des modifications dans la base de données
    db.commit()
    
    # Rafraîchir l'objet livre dans la session
    db.refresh(book)
    
    return book


# delete an existing book:

@route.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # Récupération du livre dans la base de données
    book = db.query(models.book).filter(models.book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    
    # Supprimer le livre de la base de données
    db.delete(book)
    db.commit()
    
    return {"message": "Book deleted successfully"}
