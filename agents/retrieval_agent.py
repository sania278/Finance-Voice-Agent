# agents/retriever_agent.py

from fastapi import FastAPI, Query
import requests

app = FastAPI()
API_KEY = "CAV6K68ALSOXO12E"  # Replace with your valid Alpha Vantage API key

# Simplified symbol lookup (could be replaced with ML NER in future)
COMPANY_SYMBOLS = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "tesla": "TSLA",
    "nvidia": "NVDA"
}

@app.get("/ask/")
def ask_question(query: str = Query(...)):
    print("🔎 Received query:", query)

    # Step 1: Extract stock symbol
    symbol = COMPANY_SYMBOLS.get(query.strip().lower(), None)
    if not symbol:
        return {"answers": [f"❌ Sorry, I couldn't find stock symbol for '{query}'"]}

    # Step 2: Call Alpha Vantage
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return {"answers": [f"❗ Error fetching data: {str(e)}"]}

    # Step 3: Parse and format news
    if "feed" not in data or not data["feed"]:
        return {"answers": [f"ℹ️ No recent news found for {query.title()}."]}

    results = [
        f"📰 {item.get('title', 'No title')}: {item.get('summary', 'No summary')}."
        for item in data["feed"][:3]
    ]
    return {"answers": results}
