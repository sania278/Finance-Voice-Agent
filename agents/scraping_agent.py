from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/earnings/{ticker}")
def get_earnings_news(ticker: str):
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"

    try:
        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, features="xml")

        items = soup.find_all("item")
        earnings_news = []

        for item in items:
            title = item.title.text
            if any(word in title.lower() for word in ["earnings", "beat", "miss", "q1", "q2", "results"]):
                earnings_news.append(title)

        return {
            "ticker": ticker.upper(),
            "earnings_headlines": earnings_news[:5]  # Top 5
        }

    except Exception as e:
        return {"error": str(e)}
