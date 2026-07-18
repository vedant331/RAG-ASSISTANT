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

# document_id: int as a function parameter, matching {document_id} in the route path — same pattern as /greet/{name}, just typed as int this time instead of str. 
# FastAPI automatically converts the URL text to an integer, and rejects the request with a clean validation error if someone passes something that isn't a number.
# status_code=404 — "Not Found." Different from 401/403: this means the thing you're asking about doesn't exist at all, not that you're unauthorized to see it.
# The duplicate-check (existing = db.query(...)) prevents granting the same role the same document twice — good defensive practice, same instinct as the duplicate-email check in signup.
# f"Role '{role.name}' granted access to document {document_id}" — an f-string building a human-readable confirmation message


# .join(models.DocumentPermission, models.Document.id == models.DocumentPermission.document_id) — this is a SQL JOIN, combining rows from documents and document_permissions wherever their IDs match. In plain terms: "connect each document to its permission records."
# .filter(models.DocumentPermission.role_id == current_user.role_id) — this is the critical line. It only keeps documents where the joined permission record's role_id matches the logged-in user's own role. This filtering happens as part of the database query itself — before any results are ever pulled into Python or returned to the client. This is exactly the "filter before retrieval, not after" principle from your original project plan. A user literally cannot receive a document row their role isn't permitted to see — it's excluded at the SQL level.
# [{...} for doc in documents] — a list comprehension, a compact way of building a list by transforming each item. This is equivalent to writing a for loop that appends a dictionary for each document, just more concise. Worth getting comfortable reading this pattern since it's everywhere in Python.

# from fastapi import UploadFile, File — UploadFile is the type representing an uploaded file; File(...) marks the parameter as required and tells FastAPI to expect it as a file upload, not a JSON field.
# async def upload_document(...) — notice async def instead of plain def for the first time. File reading is an operation that can involve waiting (I/O), and async/await is Python's way of handling operations that "pause" without blocking your whole program. For now, the practical rule: when you use await inside a function, the function itself must be declared async def.
# title: str — a plain string parameter, but notice it's not wrapped in a Pydantic model this time. When you mix file uploads with other fields, 
# FastAPI expects simple fields like this to come in as form fields, not JSON — this is a quirk of how multipart/form-data works.
# file: UploadFile = File(...) — the actual uploaded file object.
# contents = await file.read() — reads the raw bytes of the uploaded file. 
# The await here is what makes this an asynchronous operation — your server can handle other requests while waiting for this read to complete, rather than freezing.
# text = contents.decode("utf-8") — the file arrives as raw bytes; .decode("utf-8") converts those bytes into an actual Python string, assuming the file is UTF-8 encoded text (true for basic .txt files).
# file.filename — FastAPI automatically captures the original filename the user uploaded.
# text[:200] — this is Python's slice syntax, meaning "take the first 200 characters." 
# We're just returning a preview so you can visually confirm extraction worked, not the full text (which could be huge).
# from chunking import chunk_text — importing your new function, add this near the top of main.py with your other imports.
# chunks = chunk_text(text) — runs your chunking logic on the extracted text, using the default chunk_size=500, overlap=50.
# for chunk in chunks: — loops through every chunk produced.
# new_chunk = models.DocumentChunk(document_id=new_document.id, chunk_text=chunk) — creates a database row for each chunk, linking it back to the parent document. 
# Notice: embedding is deliberately left unset here — we haven't generated real embeddings yet, that's tomorrow's step. 
# For now, this column will just be NULL for each row, which is fine.
# db.add(new_chunk) — stages each chunk for insertion, but notice this is inside the loop while db.commit() is outside it, after the loop finishes. T
# his is intentional: staging multiple inserts and committing them all at once is more efficient than committing after every single chunk — one round-trip to the database instead of many.
# The return no longer includes extracted_text_preview — swapped for num_chunks, a more meaningful confirmation now that chunking is the actual output we care about.
# embedding = get_embedding(chunk) — generates a real vector for this specific chunk's text
# embedding=embedding — passes it into the DocumentChunk object, filling in the column that's been sitting empty until now
# from sqlalchemy import text as sql_text — SQLAlchemy normally wants you to build queries through its ORM, but for pgvector's special <=> operator, 
# it's clearer (and very common practice) to just write the SQL directly. text(...) wraps a raw SQL string so SQLAlchemy knows to execute it as-is.
# query: str as a plain function parameter (not from a Pydantic body) — for a GET endpoint, 
# FastAPI automatically treats simple parameters like this as query parameters, meaning you'd call this endpoint like /test-search?query=how many vacation days. This is a new pattern: not a path parameter ({query} in the URL), not a request body — a third kind of input, appended after a ? in the URL.
# embedding <=> CAST(:query_embedding AS vector) — the actual similarity search. :query_embedding is a named parameter placeholder — SQLAlchemy safely substitutes in the actual value, which prevents SQL injection attacks (never build SQL by directly gluing strings together with user input — this parameterized style is the safe way).
# CAST(:query_embedding AS vector) — we're passing the embedding in as a string representation, and this tells Postgres to interpret it as an actual vector type for the comparison.
# AS distance — names this calculated column distance so we can reference it afterward.
# ORDER BY distance ASC LIMIT 3 — sort by closeness (smallest distance = most similar), take the top 3 matches.
# WHERE embedding IS NOT NULL — skips that old empty row from Day 17 we talked about, so it doesn't cause an error trying to compare against nothing.
# db.execute(...) instead of db.query(...) — this is how you run raw SQL text through SQLAlchemy, as opposed to the ORM query builder you've used everywhere else.
# .fetchall() — retrieves all matching rows.
# row.id, row.document_id, etc. — accessing columns by name off each result row.
# Depends(get_current_user) instead of no auth at all — this endpoint now requires a logged-in user, 
# since the whole point is filtering by who they are.
# JOIN documents d ON dc.document_id = d.id — connects each chunk back to its parent document (so we can also show the document's title in results — useful context, and a preview of the "citations" feature coming next).
# JOIN document_permissions dp ON d.id = dp.document_id — connects each document to its permission records. This is the exact same join pattern from Week 2's GET /documents, just now combined with vector search in a single query.
# WHERE dp.role_id = :role_id — this is the critical line. Only chunks belonging to documents permitted for the current user's role are even considered. '
# 'Combined with the ORDER BY distance happening on this already-filtered set, unauthorized chunks are mathematically excluded from ranking — they were never compared against the query embedding for this user's results at all.
# {"query_embedding": ..., "role_id": current_user.role_id} — two named parameters now, both safely substituted in.




from fastapi import FastAPI,Depends,HTTPException,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine,Base ,get_db
from auth import hash_password,verify_password,create_access_token
from dependencies import get_current_user,require_admin
from chunking import chunk_text
from sqlalchemy import text as sql_text
from embeddings import get_embedding
from llm import generate_answer
import models

Base.metadata.create_all(bind =engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub":user.email})

    return {"access_token":access_token,"token_type":"bearer"}

@app.get("/me")
def read_current_user(current_user:models.User=Depends(get_current_user)):
    return{
        "id":current_user.id,
        "email":current_user.email,
        "role":current_user.role.name
    }

class DocumentCreateRequest(BaseModel):
    title:str
    filename: str

@app.post("/documents")
def create_document(
    request:DocumentCreateRequest,
    db:Session = Depends(get_db),
    admin_user: models.User = Depends(require_admin)
):
    new_document = models.Document(
        title = request.title,
        filename = request.filename,
        uploaded_by = admin_user.id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return{
        "id":new_document.id,
        "title":new_document.title,
        "filename":new_document.filename,
        "uploaded_by": new_document.uploaded_by,
        "created_at": new_document.created_at
    }

class GrantPermissionRequest(BaseModel):
    role_name : str

@app.post("/documents/{document_id}/permissions")
def grant_permission(
    document_id : int,
    request : GrantPermissionRequest,
    db:Session = Depends(get_db),
    admin_user: models.User = Depends(require_admin)
):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code = 404,detail="Document not found")
    
    role = db.query(models.Role).filter(models.Role.name == request.role_name).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    existing = db.query(models.DocumentPermission).filter(
        models.DocumentPermission.document_id == document_id,
        models.DocumentPermission.role_id == role.id,
    ).first()
    if existing:
        raise HTTPException(status_code = 400,detail="Permission already registered")
    
    new_permission = models.DocumentPermission(document_id = document_id,role_id = role.id)
    db.add(new_permission)
    db.commit()

    return{"message":f"Role '{role.name}' granted access to document {document_id}"}

@app.get("/documents")
def list_documents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    documents = (
        db.query(models.Document)
        .join(models.DocumentPermission, models.Document.id == models.DocumentPermission.document_id)
        .filter(models.DocumentPermission.role_id == current_user.role_id)
        .all()
    )

    return [
        {"id": doc.id, "title": doc.title, "filename": doc.filename, "created_at": doc.created_at}
        for doc in documents
    ]

@app.post("/documents/upload")
async def upload_document(
    title: str,
    file : UploadFile = File(...),
    db : Session = Depends(get_db),
    admin_user: models.User = Depends(require_admin)
):
    contents = await file.read()
    text = contents.decode("utf-8")

    new_document = models.Document(
        title = title,
        filename = file.filename,
        uploaded_by = admin_user.id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    chunks = chunk_text(text)
    
    for chunk in chunks:
        embedding = get_embedding(chunk)
        new_chunk = models.DocumentChunk(
            document_id = new_document.id,
            chunk_text = chunk,
            embedding = embedding
        )
        db.add(new_chunk)
    db.commit()

    return {
        "id" : new_document.id,
        "title" : new_document.title,
        "filename" : new_document.filename,
        "extracted_text_preview" : len(chunks)
    }

@app.get("/search")
def search_documents(
    query:str,
    db:Session = Depends(get_db),
    current_user : models.User = Depends(get_current_user)
):
    query_embedding = get_embedding(query)

    results = db.execute(
        sql_text("""
                 SELECT dc.id, dc.document_id, dc.chunk_text, d.title,
                    dc.embedding <=> CAST(:query_embedding AS vector) AS distance
                FROM document_chunks dc
                JOIN documents d ON dc.document_id = d.id
                JOIN document_permissions dp ON d.id = dp.document_id
                WHERE dp.role_id = :role_id
                    AND dc.embedding IS NOT NULL
                    AND dc.embedding <=> CAST(:query_embedding AS vector) < 0.6
                ORDER BY distance ASC
                LIMIT 3
                 """),
                 {"query_embedding":str(query_embedding),"role_id":current_user.role_id}
    ).fetchall()

    return [
        {
            "chunk_id": row.id,
            "document_id": row.document_id,
            "document_title": row.title,
            "chunk_text": row.chunk_text,
            "distance": row.distance
        }
        for row in results
    ]

@app.get("/ask")
def ask(
    query:str,
    db:Session = Depends(get_db),
    current_user:models.User = Depends(get_current_user)
):
    query_embedding = get_embedding(query)

    results = db.execute(
        sql_text("""
                 SELECT dc.id, dc.document_id, dc.chunk_text, d.title,
                   dc.embedding <=> CAST(:query_embedding AS vector) AS distance
                 FROM document_chunks dc
                 JOIN documents d ON dc.document_id = d.id
                 JOIN document_permissions dp ON d.id = dp.document_id
                 WHERE dp.role_id = :role_id
                    AND dc.embedding IS NOT NULL
                    AND dc.embedding <=> CAST(:query_embedding AS vector) < 0.6
                 ORDER BY distance ASC
                 LIMIT 3
        """),
        {"query_embedding":str(query_embedding),"role_id":current_user.role_id}
    ).fetchall()

    if not results:
        return {
            "answer": "I couldn't find any relevant information in the documents you have access to.",
            "sources": []
        }
    
    context_chunks = [row.chunk_text for row in results]
    answer = generate_answer(query,context_chunks)

    sources = [
        {"document_title":row.title,"document_id":row.document_id}
        for row in results
    ]
    return {
        "answer":answer,
        "sources":sources
    }
 