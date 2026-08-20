from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route

#startlette server does not support get/post/put/delete
#no built-in support for swagger

# In-memory database
customers = []


# GET /customers
async def get_customers(request: Request):
    return JSONResponse(customers)


# GET /customers/{id}
async def get_customer(request: Request):
    customer_id = int(request.path_params["id"])

    for customer in customers:
        if customer["id"] == customer_id:
            return JSONResponse(customer)

    return JSONResponse({"message": "Customer not found"}, status_code=404)


# POST /customers
async def create_customer(request: Request):
    data = await request.json()

    customer = {
        "id": len(customers) + 1,
        "name": data.get("name"),
        "email": data.get("email"),
        "city": data.get("city")
    }

    customers.append(customer)

    return JSONResponse(customer, status_code=201)


# PUT /customers/{id}
async def update_customer(request: Request):
    customer_id = int(request.path_params["id"])
    data = await request.json()

    for customer in customers:
        if customer["id"] == customer_id:
            customer["name"] = data.get("name", customer["name"])
            customer["email"] = data.get("email", customer["email"])
            customer["city"] = data.get("city", customer["city"])

            return JSONResponse(customer)

    return JSONResponse({"message": "Customer not found"}, status_code=404)


# DELETE /customers/{id}
async def delete_customer(request: Request):
    customer_id = int(request.path_params["id"])

    for customer in customers:
        if customer["id"] == customer_id:
            customers.remove(customer)
            return JSONResponse(
                {"message": "Customer deleted successfully"}
            )

    return JSONResponse({"message": "Customer not found"}, status_code=404)


routes = [
    Route("/customers", endpoint=get_customers, methods=["GET"]),
    Route("/customers/{id:int}", endpoint=get_customer, methods=["GET"]),
    Route("/customers", endpoint=create_customer, methods=["POST"]),
    Route("/customers/{id:int}", endpoint=update_customer, methods=["PUT"]),
    Route("/customers/{id:int}", endpoint=delete_customer, methods=["DELETE"]),
]

app = Starlette(debug=True, routes=routes)

#uvicorn main:app --reload

'''
Test APIs
1. Create Customer

POST

http://127.0.0.1:8000/customers

Body

{
    "name":"murthy",
    "email":"murthy@gmail.com",
    "city":"Hyderabad"
}

Response

{
    "id":1,
    "name":"John",
    "email":"john@gmail.com",
    "city":"Hyderabad"
}
2. Get All Customers

GET

http://127.0.0.1:8000/customers

Response

[
    {
        "id":1,
        "name":"John",
        "email":"john@gmail.com",
        "city":"Hyderabad"
    }
]
3. Get Customer by ID

GET

http://127.0.0.1:8000/customers/1
4. Update Customer

PUT

http://127.0.0.1:8000/customers/1

Body

{
    "city":"Bangalore"
}

Response

{
    "id":1,
    "name":"John",
    "email":"john@gmail.com",
    "city":"Bangalore"
}
5. Delete Customer

DELETE

http://127.0.0.1:8000/customers/1

Response

{
    "message":"Customer deleted successfully"
}
'''
