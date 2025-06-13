from fastapi import FastAPI
from database import Base, engine
from stock_crud import stock_router

app = FastAPI()
app.include_router(router=stock_router, prefix='/stock', tags=['stock'])

Base.metadata.create_all(bind=engine)