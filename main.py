from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from sqlalchemy.orm import Session
from  sqlalchemy.sql.expression import func
from database import SessionLocal, engine
import models, schemas
from models import Coins, CoinMetrics


from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class CoinRequest(BaseModel):
    symbol: str

# get db session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



@app.get("/")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Displays the coin screener dashboard / homepage
    """

    coins = db.query(models.Coins).order_by(func.random()).limit(5).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "coins": coins
    })

    # return templates.TemplateResponse("dashboard.html", {
    #     "request" : request
    # })


# def fetch_coin_data(id: int):
#     """
#     id is reference to key id of database
#     """
#     db = SessionLocal()
#     coin = db.query(Coins).filter(Coins.id == id).first()


#     db.add(coin)
#     db.commit()


# @app.post("/coin")
# async def create_coin(coin_request: CoinRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     """
#     Creates a coin and stores it in database
#     """
#     coin = Coins()
#     coin.symbol = coin_request.symbol

#     db.add(coin)
#     db.commit()

#     background_tasks.add_task(fetch_coin_data, coin.id)

#     return {
#         "code": "success",
#         "message": "stock created"

#     }