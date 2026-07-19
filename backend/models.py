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

# ForeignKey("roles.id") — this is how a "reference" is expressed in SQL/SQLAlchemy. User.role_id doesn't store a role's name — it stores the id number of a row in the roles table. This is the actual database-level link.
# relationship("Role", back_populates="users") — this is a SQLAlchemy-only convenience, not a real database column. It lets you write Python like some_user.role.name to directly access the related Role object, instead of manually writing a join query yourself every time. 
# back_populates just means "these two relationships are two sides of the same connection" — so Role.users and User.role stay in sync with each other conceptually.
# Document.uploaded_by = Column(Integer, ForeignKey("users.id")) — same pattern: this column stores which user's id uploaded the document.
# DateTime(timezone=True), server_default=func.now() — this tells Postgres itself (not Python) to automatically stamp the current time when a row is created. 
# server_default (vs a Python-side default) means it's reliable even if multiple different services insert rows — the database's clock is the single source of truth.
# DocumentPermission — exactly the join table from the diagram: just two foreign keys (document_id, role_id) plus its own id. 
# # Each row is literally one permission grant.
# user_id = Column(Integer, ForeignKey("users.id")) — links each log entry to exactly who asked.
# query_text — the actual question asked, stored verbatim.
# document_ids_used = Column(String, nullable=True) — we'll store which document IDs contributed to the answer, as a comma-separated string (a simple, pragmatic choice — a more sophisticated version might use a proper join table like document_permissions, but for an audit log, a simple string is genuinely fine and common in practice). nullable=True since a query with zero results (nothing found) legitimately has no documents to log.
# created_at — same auto-timestamp pattern as your Document model 



from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import DateTime as DateTimeColumn
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DocumentPermission(Base):
    __tablename__ = "document_permissions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)          

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer,primary_key=True,index=True)
    document_id = Column(Integer,ForeignKey("documents.id"),nullable=False)
    chunk_text = Column(String,nullable=False)
    embedding = Column(Vector(384))

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query_text = Column(String, nullable=False)
    document_ids_used = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())