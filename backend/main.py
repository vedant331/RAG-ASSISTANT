# from fastapi import FastAPI — pulls in the FastAPI toolkit you just installed.
# app = FastAPI() — creates your application object. Everything you build attaches to this app variable — think of it as "the kitchen" itself.
# @app.get("/health") — this line is called a decorator. It tells FastAPI: "when a request comes in as a GET to the URL path /health, run the function directly below me."
# def health_check(): — just a normal Python function. The name can be anything — it's the @app.get(...) line above it that actually wires it up.
# return {"status": "ok", "message": "Backend is alive"} — a Python dictionary. FastAPI automatically converts this to JSON and sends it back as the response.

# import models — this import is important even though we never directly use the word models elsewhere in this file. Just importing it runs the User class definition, which registers it with Base. Without this line, SQLAlchemy wouldn't know the users table needs to be created.
# Base.metadata.create_all(bind=engine) — this line looks at every model registered with Base (right now, just User) and creates the corresponding table in Postgres if it doesn't already exist. Safe to run every time the app starts — it won't wipe or duplicate existing tables.

from fastapi import FastAPI
from pydantic import BaseModel
from database import engine,Base 
import models

Base.metadata.create_all(bind =engine)

app = FastAPI()

@app.get("/health") # decorator 
def health_chec():
    return {"status":"ok","message":"Backend is alive"}

# @app.get("/greet/{name}") — the {name} inside curly braces is a placeholder. It means: "whatever text appears in this part of the URL, capture it as a variable called name."
# def greet_user(name: str): — notice the function's parameter is also called name, and FastAPI automatically matches it to the {name} from the URL. The : str is a type hint telling FastAPI (and Python) this value should be treated as text.
# f"Hello, {name}!..." — this is an f-string, a Python feature for inserting variables directly into text. The f before the quotes lets you use {variable_name} inside the
@app.get("/greet/{name}")
def greet_user(name:str):
    return {"message":f"hello,{name}! Welcome to RAG assistant backend."}

class MessageRequest(BaseModel):
    question : str

@app.post("/ask")
def ask_question(request:MessageRequest):
    return {
        "you asked": request.question,
        "answer":"This is a placedholder - we'll connect this to a real AI answer soon"
    }

