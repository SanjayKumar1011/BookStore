from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field, field_validator
from typing import List,Optional
api=FastAPI()

@api.get("/")
def home():
    return "Hello world using Fast API!!"

@api.get("/greet")
def Greet():
    return {"Greetings" : "Welcome to Fast Api!!!"}


class Book(BaseModel):
    id:int
    title:str = Field(...,min_length=3)
    author:str = Field(...,min_length=3)
    price:int = Field(...,gt=0)
    description: Optional[str] = None

    @field_validator("title",mode="after")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v[0].isupper():
            raise ValueError("Title must start with a capital letter")
        return v

    @field_validator("author")
    @classmethod
    def validate_author(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("Author name must be at least 3 characters")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v < 1 or v > 10000:
            raise ValueError("Price must be between ₹1 and ₹10,000")
        return v

books: List[Book]=[]

@api.post("/book")
def createBook(book:Book):
    for b in books:
        if book.id==b.id:
            raise HTTPException(status_code=400,detail="Book already exists with id ")
    books.append(book)
    return book


@api.get("/books")
def getbooks():
    return books

@api.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")