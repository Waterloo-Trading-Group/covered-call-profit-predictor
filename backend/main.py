from fastapi import FastAPI
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from functions.calcs import api_call
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/stocks/{ticker}")
async def get_stock(ticker: str):
    return {"ticker": ticker}


@app.get("/{ticker}/{daysTillStrike}/{premium}/{strikePrice}")
async def get_stock(ticker: str, daysTillStrike: int, premium: float, strikePrice: float):
    return {"Message: ": api_call(ticker, daysTillStrike, premium, strikePrice)}

# Stock Ticker, Strike Price, Premium, men

