from pydantic import BaseModel,Field

class Blog(BaseModel):
    title: str= Field(...,min_length=2,max_length=10)
    author: str = Field(...,min_length=2,max_length=10)
    body: str = Field(...,min_length=2,max_length=10)


