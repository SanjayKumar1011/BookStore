from fastapi import FastAPI,Depends
from pydantic import BaseModel
from .database import engine,get_db
from . import models,schemas
from sqlalchemy.orm import Session
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get('/')
def ping():
    return  "Pong"

@app.post('/blog')
def createBlog(requestBlog:schemas.Blog, db: Session= Depends(get_db)):
    blog=models.Blog(title=requestBlog.title,
         author=requestBlog.author,
         body=requestBlog.body)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog
