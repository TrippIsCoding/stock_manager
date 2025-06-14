from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models import Stock, StockModel
from database import get_db

stock_router = APIRouter()

@stock_router.get('/view')
async def list_all_stock(db: Session = Depends(get_db)):
    """
    list_all_stock puts everything from the Stock database into a list of dictionaries and returns them
    """
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

    return {200: 'product successfully added to stock'}

@stock_router.put('/update/{id}')
async def update_products_stock(id: int, product_update: StockModel = Depends(), db: Session = Depends(get_db)):
    product = db.query(Stock).filter(Stock.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail=f'Product {id} not found make sure you use the correct id')

    product.name = product_update.name
    product.in_stock = product_update.in_stock
    product.price = product.price

    db.commit()
    db.refresh(product)

    return {200: 'product has been updated'}

@stock_router.delete('/remove/{id}')
async def remove_product_from_stock(id: int, db: Session = Depends(get_db)):
    product = db.query(Stock).filter(Stock.id==id).first()

    if not product:
        raise HTTPException(status_code=404, detail=f'Product {id} not found check that its the right id')

    db.delete(product)

    return {200: 'Product was deleted'}