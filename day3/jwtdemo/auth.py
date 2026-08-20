from datetime import datetime,timedelta,timezone
#pip install pyjwt  bcrypt  email-validator

import jwt # to work with JWT
import bcrypt # store hashed password in db

SECRET_KEY="change-this-secret-key-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

#hash the pwd and write it in db for security
def hash_password(password:str) ->str:
    password_bytes=password.encode("utf-8")[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

def verify_password(password:str, hashed_password:str) ->bool:
    pasword_bytes=password.encode("utf-8")[:72]
    return bcrypt.checkpw(pasword_bytes,hashed_password.encode("utf-8"))
    
#create the jwt token ( header - payload - signature)
def create_access_token(username:str) -> str:
    expire= datetime.now(timezone.utc) + timedelta (minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={ "sub":username, "exp":expire}
    return jwt.encode(payload,SECRET_KEY,ALGORITHM)#   xxxx.yyyyy.zzzzzz

def decode_access_token(token:str):
    return jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM] )
    
    
    
