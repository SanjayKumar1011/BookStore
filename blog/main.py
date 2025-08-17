from fastapi import FastAPI,Depends,status,HTTPException
from .database import engine,get_db
from . import models,schemas
from sqlalchemy.orm import Session
from typing import List

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get('/')
def ping():
    return  "Pong"

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def createBlog(requestBlog:schemas.Blog, db: Session= Depends(get_db)):
    blog=models.Blog(title=requestBlog.title,
         author=requestBlog.author,
         body=requestBlog.body)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@app.get('/blog',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
def getAllBlogs(db: Session= Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK)
def getBlogById(id:int, db: Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} does not exists")
    return blog

@app.put('/blog/{id}')
def updateBlogById(id:int,requestBlog:schemas.Blog,db: Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} does not exists")
    blog.update(requestBlog.model_dump())
    db.commit()
    db.refresh(blog)
    return f"Successfully Updated the blog with id {id}"

@app.delete('/blog/{id}')
def deleteBlogById(id:int,db: Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} does not exists")
    blog.delete()
    db.commit()
    db.refresh(blog)
    return f"Successfully deleted the blog with id {id}"


@app.post('/user',status_code=status.HTTP_201_CREATED)
def createUser(requestBlog:schemas.User, db: Session= Depends(get_db)):
    user=models.User(name=requestBlog.name,
                     email=requestBlog.email,
                     password=requestBlog.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/user',status_code=status.HTTP_200_OK,response_model=List[schemas.User])
def getUser(db: Session= Depends(get_db)):
    user=db.query(models.User).all()
    return user
