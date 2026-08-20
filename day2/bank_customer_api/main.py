from fastapi import FastAPI,HTTPException
from database import Base,engine,SessionLocal
from schemas import CustomerIn,CustomerOut
import crud as crud

Base.metadata.create_all(bind=engine) 

app=FastAPI(title="Bank Customer API")

@app.post("/customers",response_model=CustomerOut)
def c(x:CustomerIn):
    db=SessionLocal()
    o=crud.create(db,x)
    db.close()
    return o
 
@app.get("/customers",response_model=list[CustomerOut])
def g():
    db=SessionLocal()
    r=crud.all(db)
    db.close()
    return r
 
@app.get("/customers/{id}",response_model=CustomerOut)
def o(id:int):
    db=SessionLocal()
    r=crud.one(db,id)
    db.close()
    if not r :
        raise HTTPException(404,"Not found")
    return r

@app.put("/customers/{id}",response_model=CustomerOut)
def u(id:int,x:CustomerIn):
    db=SessionLocal()
    r=crud.update(db,id,x)
    db.close()
    if not r:
        raise HTTPException(404,"Not found")
    return r

@app.delete("/customers/{id}")
def d(id:int):
    db=SessionLocal()
    r=crud.delete(db,id)
    db.close()
    if not r:
        raise HTTPException(404,"Not found")
    return {"message":"Deleted"}
