# DATABASE_URL — this string is the "address" telling Python exactly how to reach your database: postgresql://<username>:<password>@<host>:<port>/<database_name>. 
# Match this against what you created: rag_user, rag_password, localhost (your own machine), 5432 (the port), rag_assistant (the database name).
# engine = create_engine(...) — this creates the actual connection engine — the object that knows how to open connections to Postgres whenever needed.
# SessionLocal = sessionmaker(...) — a "session" is a single conversation with the database (open it, do some work, close it). This line doesn't open a session yet 
# — it just creates a factory for making sessions whenever your code needs one.
# Base = declarative_base() — this is a special base class. 
# Any Python class that inherits from Base will automatically become a real database table. We'll use this in the next step to define your first table: users.

# Only the new part is get_db() at the bottom.
# This is a generator function (note yield instead of return) 
# — FastAPI has special support for using generators like this as "dependencies.
# " In plain terms: for each incoming request, FastAPI calls get_db(), hands your endpoint the session (the yielded value), and once the endpoint finishes 
# — success or failure — it automatically runs the finally: db.close() to clean up. You never have to manually open/close sessions yourself in each endpoint.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://rag_user:rag_password@localhost:5432/rag_assistant"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()