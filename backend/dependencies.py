# HTTPBearer() replaces OAuth2PasswordBearer(...) — this is a simpler auth scheme that just expects a raw Authorization: Bearer <token> header, without trying to simulate a login form itself. It matches what we're actually doing much more directly.
# credentials: HTTPAuthorizationCredentials = Depends(security) — Swagger will now just give you a single text box to paste your token into.
# token = credentials.credentials — extracts the actual token string out of that object.

# Depends(get_current_user) — 
# this reuses your existing dependency. 
# FastAPI runs get_current_user first (verifying the token, loading the user), and hands the result in as current_user here.
# current_user.role.name != "admin" — 
# this is that relationship we built paying off: current_user.role gives you the full Role object, 
# .name gives you the string, and we compare it directly.
# status_code=403 — this is different from 401. 401 "Unauthorized" means "I don't know who you are" (bad/missing token). 
# 403 "Forbidden" means "I know exactly who you are, but you're not allowed to do this." That distinction matters and is worth remembering — it comes up constantly in real APIs.
# return current_user — if the check passes, hand back the user object so the endpoint itself can use it (e.g. to know who's creating the document).


from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth import decode_access_token
import models

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        email = decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(status_code = 403,detail="Admin access required")
    return current_user