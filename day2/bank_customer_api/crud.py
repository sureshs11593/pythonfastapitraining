from models import Customer

def create(db,d): 
    o=Customer(**d.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return o

def all(db): 
    return db.query(Customer).all()

def one(db,i): 
    return db.query(Customer).filter(Customer.id==i).first()

def update(db,i,d):
    o=one(db,i)
    if o:
        o.name,o.email,o.phone,o.account_type,o.balance=d.name,d.email,d.phone,d.account_type,d.balance
        db.commit(); db.refresh(o)
        return o
    
def delete(db,i):
    o=one(db,i)
    if o: db.delete(o); db.commit()
    return o
