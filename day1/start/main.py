'''
pip install fastapi uvicorn
pip install python-multipart   (for uploading file)

uvicorn main:app --reload
'''

from fastapi import Depends, FastAPI
from typing import Optional

app = FastAPI()
print("Uvicorn Server is running on port 8000....")

@app.get("/")
def home():
    return {"message": "FastAPI Server Running"}

#Route Parameters
@app.get("/users/{id}")
async def get_user(id: int):
    return {
        "UserID": id
    }

#optional params
@app.get("/contact/{cid}")
def contact_details(cid:int,page:Optional[int]=1):
    if page:
        return {'contact_id':cid,'page':page}
    return {'contact_id':cid}

#Query Parameters
@app.get("/search",description='Search for name Murthy')
async def search(name: str, age: int):
    return {
        "Name": name,
        "Age": age
    }

#Request
#/search?name=murthy&age=30

from fastapi import FastAPI
from pydantic import BaseModel

#pydantic demo
class User(BaseModel):
    id: int
    name: str

@app.get('/user', response_model=User)
def get_user():
    return User(id=1, name='Murthy')


#POST Request
from pydantic import BaseModel

class Employee(BaseModel):
    id:int
    name:str
    salary:float

@app.post("/employee",description='Create new employee')
async def create(emp:Employee):
    return emp


# Dependency Injection
from fastapi import Depends
def verify():
    return {
        "user":"admin"
    }

@app.get("/dashboard")
async def dashboard(user=Depends(verify)):
    return user

#Middleware
from fastapi import  Request
@app.middleware("http")
async def timer(request: Request, call_next):
    print("Before Request")
    response = await call_next(request)
    print("After Request")
    return response

'''
#Authentication Middleware
from fastapi import Request
from fastapi.responses import JSONResponse

@app.middleware("http")
async def auth(request:Request, call_next):
    token=request.headers.get("Authorization")
    if token!="secret":
        return JSONResponse(
            {"error":"Unauthorized"},
            status_code=401
        )
    return await call_next(request)

@app.get("/")
async def home():
    return {"message":"Authorized"}
'''
#Logging Every Request
import time

@app.middleware("http")
async def logger(request:Request, call_next):
    start=time.time()
    response=await call_next(request)
    duration=time.time()-start
    print(
        request.method,
        request.url.path,
        duration
    )
    return response

# Custom Headers
from fastapi.responses import JSONResponse
@app.get("/headers")
async def home():
    response=JSONResponse({"status":"success"})
    response.headers["Server"]="FastAPI"
    return response

#Background Tasks
from fastapi import  BackgroundTasks
def send_email():
    print("Email Sent")

@app.get("/register")
async def register(background_tasks:BackgroundTasks):
    background_tasks.add_task(send_email)
    return {"message":"Registered"}

# File Upload
from fastapi import UploadFile, File
@app.post("/upload")
async def upload(file:UploadFile=File(...)):  #... means required
    contents=await file.read()
    return {
        "filename":file.filename,
        "size":len(contents)
    }

#Static Files
from fastapi.staticfiles import StaticFiles
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

#Access
#http://localhost:8000/static/mind3.png

# HTML Templates
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates(directory="templates")

@app.get("/homepage")
async def homepage(request:Request):
    return templates.TemplateResponse(
        "index.html",
        {"request":request}
    )

# WebSocket Chat
from fastapi import WebSocket
@app.websocket("/ws")
async def websocket_endpoint(ws:WebSocket):
    await ws.accept()
    while True:
        data=await ws.receive_text()
        await ws.send_text(f"Echo : {data}")

# Exception Handling
from fastapi import HTTPException
@app.get("/product/{id}")
async def product(id:int):
    if id>10:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )
    return {"id":id}


#======================================