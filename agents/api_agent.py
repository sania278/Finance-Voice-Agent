from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/stock/{ticker}")
def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2d")
    info = stock.info

    return {
        "name": info.get("shortName"),
        "current_price": info.get("currentPrice"),
        "previous_close": info.get("previousClose"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "history": hist.tail(2).to_dict()
    }
