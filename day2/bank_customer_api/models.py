from sqlalchemy import Column,Integer,String
from database import Base

class Customer(Base):
    __tablename__="customers"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String,unique=True)
    phone=Column(String)
    account_type=Column(String)
    balance=Column(Integer)
