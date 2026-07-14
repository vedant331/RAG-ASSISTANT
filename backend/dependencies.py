# HTTPBearer() replaces OAuth2PasswordBearer(...) — this is a simpler auth scheme that just expects a raw Authorization: Bearer <token> header, without trying to simulate a login form itself. It matches what we're actually doing much more directly.
# credentials: HTTPAuthorizationCredentials = Depends(security) — Swagger will now just give you a single text box to paste your token into.
# token = credentials.credentials — extracts the actual token string out of that object.



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