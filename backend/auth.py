# CryptContext(schemes=["bcrypt"], ...) — sets up a hashing "context" configured to use bcrypt specifically. deprecated="auto" is boilerplate that lets you migrate to a newer scheme later without breaking old hashes — not something to worry about now.
# hash_password(password) — takes a plain password, returns the bcrypt hash. This is what we call during signup.
# verify_password(plain_password, hashed_password) — takes what the user just typed at login, plus the stored hash, and returns True/False. Internally it re-hashes plain_password and compares — you never manually compare strings yourself, passlib handles the comparison safely (important, since naive string comparison can leak timing information to attackers — you don't need to implement that defense yourself, just know it's why we use a library instead of writing this by hand).


from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY = "replace-this-with-a-long-random-string-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

def hash_password(password:str) ->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict)->str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def decode_access_token(token:str)->str:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            raise JWTError("Token missing subject")
        return email
    except JWTError:
        raise ValueError("Could not validate token")