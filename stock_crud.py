from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models import Stock, StockModel
from database import get_db

stock_router = APIRouter()

@stock_router.get('/view')
async def list_all_stock(db: Session = Depends(get_db)):
    store_stock = db.query(Stock).order_by(Stock.id).all()

    return [{'id': stock.id, 'name': stock.name, 'stock left': stock.in_stock, 'price': stock.price} for stock in store_stock]

@stock_router.post('/create')
async def create_stock(stock_info: StockModel = Depends(), db: Session = Depends(get_db)):
    add_stock = Stock(
        name=stock_info.name,
        in_stock=stock_info.in_stock,
        price=stock_info.price if stock_info.price[0] == '$' else '$' + stock_info.price
    )

    db.add(add_stock)
    db.commit()
    db.refresh(add_stock)

    return {'successful': 'added the item to the stock'}

@stock_router.put('/update')
async def update_stock():
    pass

@stock_router.delete('/remove')
async def remove_stock():
    pass