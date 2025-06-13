from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models import Stock, StockModel
from database import get_db

stock_router = APIRouter()

@stock_router.get('/view')
async def list_all_stock(db: Session = Depends(get_db)):
    store_stock = db.query(Stock).order_by(Stock.id).all()

    if not store_stock:
        raise HTTPException(status_code=404, detail='There are no products in stock')

    return [{'id': stock.id, 'name': stock.name, 'stock left': stock.in_stock, 'price': stock.price} for stock in store_stock]

@stock_router.post('/create')
async def add_product_to_stock(stock_info: StockModel = Depends(), db: Session = Depends(get_db)):
    add_product = Stock(
        name=stock_info.name,
        in_stock=stock_info.in_stock,
        price=stock_info.price if stock_info.price[0] == '$' else '$' + stock_info.price
    )

    db.add(add_product)  
    db.commit()
    db.refresh(add_product)

    return {'successful': 'added the product to the stock'}

@stock_router.put('/update')
async def update_product(id: int = Depends(), product_update: StockModel = Depends(), db: Session = Depends(get_db)):
    product = db.query(Stock).filter(Stock.id == id).first()

    product.name = product_update.name
    product.in_stock = product_update.in_stock
    product.price = product.price

    db.commit()
    db.refresh(product)

@stock_router.delete('/remove')
async def remove_product_from_stock(id: int = Depends(), db: Session = Depends(get_db)):
    product = db.query(Stock).filter(Stock.id==id).first()

    db.delete(product)