from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.routing import APIRoute
from pydantic import BaseModel, EmailStr, Field
import router
app = FastAPI()
app.routes.append(router.hello_route)

'''
def hello() -> dict:
    return {"message": "hello"}

hello_route = APIRoute(
    path="/hello",
    endpoint=hello,
    methods=["GET"],
    name="hello",
)
app.routes.append(hello_route)
'''

'''
This line declares a field named name with the type str. 
In Python, the annotation name: str tells the program that this value
should be a string. The Field(...) part is typically used in frameworks 
such as Pydantic to define validation rules for the field.

The ... inside Field(...) means the field is required and must be provided 
when creating an object. The min_length=3 and max_length=50 arguments
add validation constraints, so the value of name must be at least 3 characters
long and no more than 50 characters long. In other words, this line ensures that
name is a required string that must fall within that length range.

pattern = regex in old version

Activate environment and pip install -r requirements.txt

pip install pydantic[email]

localhost:8000/docs            
'''

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    balance: float = Field(..., ge=0, description="Account balance must be zero or positive")
    account_type: str = Field(..., pattern="^(checking|savings)$")

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr]
    balance: Optional[float] = Field(None, ge=0)
    account_type: Optional[str] = Field(None, pattern="^(checking|savings)$")

class Customer(CustomerBase):
    id: int

fake_customers = [
    {"id": 1, "name": "Murthy", "email": "murthy@example.com", "balance": 1200.50, "account_type": "checking"},
    {"id": 2, "name": "Raj", "email": "raj@example.com", "balance": 3400.00, "account_type": "savings"},
    {"id": 3, "name": "Kiran", "email": "kiran@example.com", "balance": 980.75, "account_type": "checking"},
    {"id": 4, "name": "Daniel", "email": "daniel@example.com", "balance": 560.00, "account_type": "savings"},
    {"id": 5, "name": "Smith", "email": "smith@example.com", "balance": 4300.20, "account_type": "checking"},
]

@app.get("/customers", response_model=List[Customer])
def list_customers():
    return fake_customers

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    customer = next((item for item in fake_customers if item["id"] == customer_id), None)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@app.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate):
    next_id = max(item["id"] for item in fake_customers) + 1 if fake_customers else 1
    new_customer = customer.dict()
    new_customer["id"] = next_id
    fake_customers.append(new_customer)
    return new_customer

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer_update: CustomerUpdate):
    customer = next((item for item in fake_customers if item["id"] == customer_id), None)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    update_data = customer_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        customer[key] = value
    return customer

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int):
    index = next((i for i, item in enumerate(fake_customers) if item["id"] == customer_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    fake_customers.pop(index)
    return None

    