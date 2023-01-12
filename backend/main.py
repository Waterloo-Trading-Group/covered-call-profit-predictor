from fastapi import FastAPI
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from functions.calcs import api_call
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/stocks/{ticker}")
async def get_stock(ticker: str):
    return {"ticker": ticker}


@app.get("/{ticker}/{daysTillStrike}/{premium}/{strikePrice}")
async def get_stock(ticker: str, daysTillStrike: int, premium: float, strikePrice: float):
    return {"Message": api_call(ticker, daysTillStrike, premium, strikePrice)}


# allow any request from any origin
origins = [
    "*"
]

# allow any request from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

