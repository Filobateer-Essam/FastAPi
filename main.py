from typing import Optional
from fastapi import FastAPI , Response , status ,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import *

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
        "id" : 1
    },
    {
        "title": "Second Post",
        "content": "This is the second post",
         "id" : 2
    },
    {
        "title": "Third Post",
        "content": "This is the third post",
        "id" : 3
    }
]

def findpost(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/") # called decorator which is used to define the path of the API
def root():
    return {"message": "Hello, World!"}


# Get All Posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Get the Latest Post
@app.get("/posts/latest")
def get_latest_post():
    l_p = my_posts[len(my_posts) - 1]
    return {"latest_post" :l_p }

# Get ID of Post
@app.get("/posts/{id}")
def get_postID(id : int ):
    post = findpost(id)
    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post not found for id {id}")
    print(post)
    return {"post": f"the post {post}"}



@app.post("/posts" ,status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    print(new_post)
    print(new_post.model_dump()) # Convert to json format
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0,100000000)
    my_posts.append(post_dict)  # Add new post to the list of posts
    return {"data": post_dict}

