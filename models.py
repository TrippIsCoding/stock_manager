from sqlalchemy import Integer, String, Column
from typing import Annotated
from pydantic import BaseModel, Field
from database import Base

class StockModel(BaseModel):
    name: str
    in_stock: int
    price: str

class Stock(Base):
    __tablename__ = 'Stock'

    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    name = Column(String, index=True)
    in_stock = Column(Integer)
    price = Column(Integer)