from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

#pip install sqlalchemy sqlalchemy[asyncio]

engine=create_engine("sqlite:///bank.db",connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base=declarative_base()
