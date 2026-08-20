from fastapi import FastAPI, Depends,HTTPException
from fastapi.security  import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

import models
import schemas
from database import engine,get_db
from auth import hash_password,verify_password,create_access_token,decode_access_token
#===================================================================

#create db and tables to  perform CRUD
models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="FastAPI with JWT Authentication", version="1.0.0")

bearer_scheme=HTTPBearer()

@app.get("/")
def root():
    return {"message":"Fast API with JWT Authentication API is running..."}

@app.post("/register")
def register(user: schemas.UserCreate, db: Session= Depends(get_db)):
    existing_user=db.query(models.User).filter(models.User.username == user.username).first()
    
    if existing_user:
        raise HTTPException(status_code=400,details="Username already exists")
    existing_email=db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user=models.User(
                         username=user.username, 
                         email=user.email, 
                         password= hash_password(user.password)
                         )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return { "message": "User registered successully.... congrats", "username":new_user.username}
#==========================================================================

@app.post("/login",response_model=schemas.Token)
def login(user: schemas.UserLogin, db:Session= Depends(get_db)):
    db_user=db.query(models.User).filter( models.User.username == user.username).first()
    
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token=create_access_token(db_user.username)
    return {"access_token": access_token, "token_type": "bearer"}

#========================================================================
def get_current_user( 
                     credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme),
                     db : Session=Depends(get_db)
                      ):
    try:
        payload=decode_access_token(credentials.credentials)
        username=payload.get("sub")
        
        if not username:
            raise HTTPException(status_code=401, detail= "Invalid Token")
    except Exception:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    
    user=db.query(models.User).filter( models.User.username== username).first()
    if not user:
        raise HTTPException(status_code=401, details="User not found")
    
    return user
#=========================================================

@app.get("/profile")
def profile(current_user: models.User= Depends(get_current_user)):
    return {
        "message":"Welcome to your profile",
        "username": current_user.username,
        "email": current_user.email
    }
    #=======================================================
        


