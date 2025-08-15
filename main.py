from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field, field_validator
from typing import List,Optional
app=FastAPI()

@app.get("/")
def home():
    return "Hello world using Fast API!!"

@app.get("/greet")
def Greet():
    return {"Greetings" : "Welcome to Fast Api!!!"}


class Book(BaseModel):
    id:int
    title:str = Field(...,min_length=3)
    author:str = Field(...,min_length=3)
    price:float = Field(...,gt=0)
    description: Optional[str] = None

    @field_validator("title")
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

books: List[Book]=[
    Book(id=1, title="Harry Potter", author="J.K. Rowling", price=499.99, description="A wizarding adventure."),
    Book(id=2, title="The Hobbit", author="J.R.R. Tolkien", price=399.50, description="A hobbit's journey to a dragon's lair."),
    Book(id=3, title="The Alchemist", author="Paulo Coelho", price=299.00, description="A philosophical quest for treasure."),
    Book(id=4, title="To Kill a Mockingbird", author="Harper Lee", price=349.99, description="A classic of race and justice."),
    Book(id=5, title="GOT", author="George Orwell", price=199.00, description="A dystopian world of surveillance."),
    Book(id=6, title="Atomic Habits", author="James Clear", price=550.00, description="Build good habits, break bad ones.")
]

@app.post("/book")
def createBook(book:Book):
    for b in books:
        if book.id==b.id:
            raise HTTPException(status_code=400,detail="Book already exists with id ")
    books.append(book)
    return book


@app.get("/books")
def getbooks():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")

@app.get("/jsonBooks")
def get_books_json():
    return [book.model_dump_json() for book in books]

