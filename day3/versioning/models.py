from pydantic import BaseModel

class ProductV1(BaseModel):
    id:int
    name:str
    price :float
    
class ProductV2(BaseModel):
    id:int
    product_name:str
    price :float
    currency: str   