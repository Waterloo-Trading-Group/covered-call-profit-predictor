from fastapi import FastAPI
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Stock Ticker, Strike Price, Premium, men

