from pydantic import BaseModel,Field

class Blog(BaseModel):
    title: str= Field(...,min_length=2,max_length=10)
    author: str = Field(...,min_length=2,max_length=10)
    body: str = Field(...,min_length=2,max_length=10)

class ShowBlog(Blog):
    class Config:
        from_attributes=True

class User(BaseModel):
    name:str= Field(...,min_length=3,max_length=10)
    email:str= Field(...,min_length=5,max_length=20)
    password:str=Field(...,min_length=3,max_length=50)

class ShowUser(BaseModel):
    name:str
    email:str
    class Config:
        from_attributes=True
