'''
from pydantic import BaseModel

#simple model without validation
class Employee(BaseModel):
    id: int
    name: str
    department: str
    age: int
'''
from pydantic import BaseModel, Field, StrictInt
from typing import Optional


class Employee(BaseModel):
    id: int = Field(..., gt=0, title='Employee ID')
    name: str = Field(..., min_length=3, max_length=30)
    department: str = Field(..., min_length=3, max_length=30)
    age: Optional[StrictInt] = Field(default=None, ge=21)
