# Concept: what is a "model"?
# In SQLAlchemy, a model is a Python class that represents a database table. Each class attribute becomes a column in that table. When you create an instance of the class and save it, SQLAlchemy translates that into an INSERT INTO users (...) SQL statement behind the scenes — you never write that SQL yourself.
# Step 15: Create models.py
# Inside backend/, create a new file called models.py:
# pythonfrom sqlalchemy import Column, Integer, String
# from database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     role = Column(String, default="user", nullable=False)
# Breaking this down line by line:

# from database import Base — importing the Base class you created in the last step. Inheriting from it is what turns this plain Python class into a real database table.
# class User(Base): — defining the table. The class name doesn't have to match the table name exactly, which is why the next line exists.
# __tablename__ = "users" — explicitly sets what the actual table will be called in Postgres.
# id = Column(Integer, primary_key=True, index=True) — every table needs a unique identifier per row. primary_key=True means this column uniquely identifies each row (like a serial number), and Postgres will auto-increment it (1, 2, 3...) for you. index=True makes lookups by this column fast.
# email = Column(String, unique=True, index=True, nullable=False) — a text column. unique=True means no two users can share an email (the database itself will reject duplicates — a safety net beyond just your Python code). nullable=False means this field is required — can't be left empty.
# hashed_password = Column(String, nullable=False) — notice: hashed, not plain password. We will never store a user's actual password in the database — only a one-way scrambled version. We'll cover exactly how/why when we build signup in the next step.
# role = Column(String, default="user", nullable=False) — this is the field that will later power your permission system (e.g. "admin" vs "user" vs "hr"). default="user" means if nothing is specified, new accounts default to a basic role.

from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)

