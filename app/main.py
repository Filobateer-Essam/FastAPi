from typing import Optional
from fastapi import FastAPI , Response , status ,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import *
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    # Connect to database here
    conn = psycopg2.connect(host='localhost',
    database = 'fastapi', user = 'postgres' , password = 'sniper1',cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Connect To Database Successfully 😎😎")
except psycopg2.Error as e:
    print("Unable to connect to the database")
    print(e.pgerror)
    print(e.diag.message_detail)

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
    },
    {
        "title": "Fourth Post",
        "content": "This is the fourth post",
        "id" : 4
    },
    {
        "title": "Fifth Post",
        "content": "This is the fifth post",
        "id" : 5
    }
]

def findpost(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def findIndexArr(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    

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
    lst_posts = []
    for i in range(len(my_posts) - 1, 1, -1):
        lst_posts.append(my_posts[i])
    print(lst_posts)
    return {"latest Posts" : lst_posts}
    # l_p = my_posts[len(my_posts) - 1]
    # return {"latest_post" :l_p }

# Get ID of Post
@app.get("/posts/{id}")
def get_postID(id : int ):
    post = findpost(id)
    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post not found for id {id}")
    print(post)
    return {"post": post}

@app.post("/posts" ,status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    print(new_post)
    print(new_post.model_dump()) # Convert to json format
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0,100000000)
    my_posts.append(post_dict)  # Add new post to the list of posts
    return {"data": post_dict}

@app.delete("/posts/{id}")
def delete_post(id : int):
    post = findpost(id)
    post_index = findIndexArr(id)
    print(post_index)
    if post not in my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found for id {id}")
    my_posts.remove(post)
    return {"detail": f"Post index in Array is {post_index} with id {id}  has been deleted."}

@app.put("/posts/{id}")
def update_post(id : int , post: Post):
    
    post_index = findIndexArr(id)
    print(post_index) # the place in the Array not the actual id
    
    post_withID = findpost(id)
    
    if post_withID not in my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found for id {id}")
    
    else:
        # must convert th e Object into Dic first 
        post_dict = post.model_dump()
        post_dict["id"] = id  # replace id with the actual id
        
        # update the post in the list
        my_posts[post_index] = post_dict
        return {"data": post_dict}
        
        