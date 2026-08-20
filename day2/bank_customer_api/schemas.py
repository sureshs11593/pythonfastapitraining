from pydantic import BaseModel

class CustomerIn(BaseModel):
    name:str
    email:str
    phone:str
    account_type:str
    balance:int
    
class CustomerOut(CustomerIn):
    id:int
    class Config: from_attributes=True

'''
from_attributes=True tells pydantic to allow creating the model from
an object's attributes, not only from a dictionery.

this code means CustomerOut can be built from an ORM/DB object
like a SQLAlcmemy model instance, using fields such as id,name,email etc
'''
