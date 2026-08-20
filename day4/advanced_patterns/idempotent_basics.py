#Non-Idempotent POST
from fastapi import FastAPI

app = FastAPI()
orders = []

@app.post("/orders")
def create_order(order: dict):
    orders.append(order)
    return {"message": "Order Created", "count": len(orders)}
'''
Request
POST /orders
{
    "item":"Laptop"
}

If sent three times:
orders =
[
  {"item":"Laptop"},
  {"item":"Laptop"},
  {"item":"Laptop"}
]
Three different orders are created.
________________________________________
'''

#Example 2: Idempotent PUT
from fastapi import FastAPI

app = FastAPI()
users = {}

@app.put("/users/{id}")
def update_user(id: int, user: dict):
    users[id] = user
    return users[id]
'''
Calling
PUT /users/1
{
   "name":"Murthy"
}
10 times still results in
{
   1:{
      "name":"Murthy"
   }
}
The resource remains the same.
________________________________________
'''

'''
Making POST Idempotent Using an Idempotency Key:

Many payment gateways (such as Stripe) use an Idempotency-Key.
Client sends:
POST /payments

Headers:
Idempotency-Key: abc123

Server logic:
1.	Check if key exists. 
2.	If yes, return the previous response. 
3.	Otherwise, process the request. 
4.	Store the response using the key. 
5.	Return the response. 
________________________________________
'''
#FastAPI Example
from fastapi import FastAPI, Header
import uuid

app = FastAPI()

processed = {}

@app.post("/payments")
def make_payment(
    amount: int,
    idempotency_key: str = Header(...)
):

    if idempotency_key in processed:
        return processed[idempotency_key]

    payment = {
        "payment_id": str(uuid.uuid4()),
        "amount": amount,
        "status": "Success"
    }

    processed[idempotency_key] = payment

    return payment
'''

First Request
POST /payments

Headers:
Idempotency-Key: xyz123

Body:
amount=1000
Response
{
    "payment_id":"b91d...",
    "amount":1000,
    "status":"Success"
}
________________________________________
Retry (Same Key)
POST /payments

Headers:
Idempotency-Key: xyz123
Response
{
    "payment_id":"b91d...",
    "amount":1000,
    "status":"Success"
}
#Notice the same payment ID is returned. A second payment is not created.
'''