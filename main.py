from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

my_posts = [
    {
        "title": "First Post",
        "content": "This is the first post",
    },
    {
        "title": "Second Post",
        "content": "This is the second post",
    },
]

@app.get("/") # called decorator which is used to define the path of the API
def root():
    return {"message": "Hello, World!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(new_post:Post):
    print(new_post)
    print(new_post.model_dump()) # Convert to json format
    return {"message": f"Posts created Successfully so the title is {new_post.title} it will be published {new_post.published}"}

