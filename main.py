import fastapi
import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import JWTBearer

posts = [
    {
        "id": 1,
        "title": "Penguins ",
        "text": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "Tigers ",
        "text": "Tigers are the largest living cat species and a memeber of the genus panthera."
    },
    {
        "id": 3,
        "title": "Koalas ",
        "text": "Koala is arboreal herbivorous maruspial native to Australia."
    },
]

users = []

app = FastAPI()

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.get("/", tags=["test"])
def greet():
  return {"Hello": "World"}


# Get posts
@app.get("/posts", tags=["posts"])
def get_posts():
  return {"data": posts}

# Get post by id
@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
  if id > len(posts) or id <= 0:
    return {
      "error": "Post with this ID does not exists!"
    }
    
  for post in posts:
    if post["id"] == id:
      return {
        "data": post
      }
      
# Post a blog post
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post: PostSchema):
  post.id = len(posts) + 1
  posts.append(post.dict())
  return {
    "info": "post added"
  }
  

@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }