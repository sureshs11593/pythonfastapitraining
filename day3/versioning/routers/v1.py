from fastapi import APIRouter
from models import ProductV1

router=APIRouter( prefix="/api/v1" , tags=["Products - V1.0"])

products=[
    {"id" :1, "name": "Computer", "price": 40000},
    {"id" :2, "name": "Printer", "price": 10000},
]
@router.get("/products", response_model=list[ProductV1])
def get_products():
    return products
