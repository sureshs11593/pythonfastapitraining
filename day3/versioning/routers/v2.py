from fastapi import APIRouter
from models import ProductV2

router=APIRouter( prefix="/api/v2" , tags=["Products - V2.0"])

products=[
    {"id" :1, "product_name": "Computer", "price": 40000,"currency":'INR'},
    {"id" :2, "product_name": "Printer", "price": 10000,"currency":'INR'}
]
@router.get("/products", response_model=list[ProductV2])
def get_products():
    return products
