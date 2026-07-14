# from fastapi import FastAPI — pulls in the FastAPI toolkit you just installed.
# app = FastAPI() — creates your application object. Everything you build attaches to this app variable — think of it as "the kitchen" itself.
# @app.get("/health") — this line is called a decorator. It tells FastAPI: "when a request comes in as a GET to the URL path /health, run the function directly below me."
# def health_check(): — just a normal Python function. The name can be anything — it's the @app.get(...) line above it that actually wires it up.
# return {"status": "ok", "message": "Backend is alive"} — a Python dictionary. FastAPI automatically converts this to JSON and sends it back as the response.

# import models — this import is important even though we never directly use the word models elsewhere in this file. Just importing it runs the User class definition, which registers it with Base. 
# Without this line, SQLAlchemy wouldn't know the users table needs to be created.
# Base.metadata.create_all(bind=engine) — this line looks at every model registered with Base (right now, just User) and creates the corresponding table in Postgres if it doesn't already exist. Safe to run every time the app starts — it won't wipe or duplicate existing tables.

# Depends(get_db) — this is FastAPI's dependency injection. It tells FastAPI: "before running this endpoint, call get_db(), and pass whatever it yields in as the db parameter." 
# This is how the endpoint gets a live database session without manually creating one.
# db.query(models.User).filter(models.User.email == request.email).first() — this is SQLAlchemy's ORM query syntax, equivalent to SELECT * FROM users WHERE email = ... LIMIT 1. .first() returns either the matching row (as a User object) or None if nothing matched.
# raise HTTPException(status_code=400, detail="...") — this is how you return an error response in FastAPI. 400 means "Bad Request" — the client sent something wrong (trying to register a duplicate email, in this case).
# new_user = models.User(...) — creating a new Python object matching your User model. 
# At this point it only exists in memory — nothing's been saved yet.
# db.add(new_user) — stages the new object to be inserted, but still doesn't write to Postgres yet.
# db.commit() — this is what actually executes the INSERT and saves it permanently to the database. Nothing is real until commit.
# db.refresh(new_user) — after committing, the database may have set values you didn't provide (like the auto-generated id). 
# This reloads new_user from the database so your Python object has that up-to-date id.
# The return statement deliberately excludes hashed_password — never send password hashes back in an API response, even hashed ones.

# THIS IS JUST A EXAMPLE CODE
# @app.get("/greet/{name}") — the {name} inside curly braces is a placeholder. It means: "whatever text appears in this part of the URL, capture it as a variable called name."
# def greet_user(name: str): — notice the function's parameter is also called name, and FastAPI automatically matches it to the {name} from the URL. The : str is a type hint telling FastAPI (and Python) this value should be treated as text.
# f"Hello, {name}!..." — this is an f-string, a Python feature for inserting variables directly into text. The f before the quotes lets you use {variable_name} inside the
# @app.get("/greet/{name}")
# def greet_user(name:str):
#     return {"message":f"hello,{name}! Welcome to RAG assistant backend."}

# class MessageRequest(BaseModel):
#     question : str

# @app.post("/ask")
# def ask_question(request:MessageRequest):
#     return {
#         "you asked": request.question,
#         "answer":"This is a placedholder - we'll connect this to a real AI answer soon"
#     }

# db.query(models.Role).filter(models.Role.name == "general").first() 
# — looks up the actual Role row by name, rather than hardcoding a number like role_id=4. 
# This is safer/clearer — if you ever reseed roles and the IDs shift, this code doesn't break.
# role_id=general_role.id 
# — assigns the new user to that role's numeric ID, matching the foreign key column.

#This works because of the relationship("Role", ...) 
# we defined in models.py — current_user.role now gives you the full related Role object, and .name pulls the actual string off it.

from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine,Base ,get_db
from auth import hash_password,verify_password,create_access_token
from dependencies import get_current_user
import models

Base.metadata.create_all(bind =engine)

app = FastAPI()

@app.get("/health") # decorator 
def health_chec():
    return {"status":"ok","message":"Backend is alive"}

class SignupRequest(BaseModel):
    email:str
    password:str

@app.post("/signup")
def signup(request:SignupRequest,db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    general_role = db.query(models.Role).filter(models.Role.name == "general").first()

    new_user = models.User(
        email = request.email,
        hashed_password=hash_password(request.password),
        role_id = general_role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{"id":new_user.id,"email":new_user.email,"role":new_user.role.name}


class LoginRequest(BaseModel):
    email:str
    password:str

@app.post("/login")
def login(request:LoginRequest,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user or not verify_password(request.password,user.hashed_password):
        raise HTTPException(status_Code=401,detail="Incorrect email or passowrd")

    access_token = create_access_token(data={"sub":user.email})

    return {"accesss_token":access_token,"token_type":"bearer"}

@app.get("/me")
def read_current_user(current_user:models.User=Depends(get_current_user)):
    return{
        "id":current_user.id,
        "email":current_user.email,
        "role":current_user.role.name
    }
