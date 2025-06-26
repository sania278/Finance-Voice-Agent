# agents/summarizer_agent.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SummaryRequest(BaseModel):
    answers: List[str]

@app.post("/summarize/")
async def summarize(request: SummaryRequest):
    """
    Very basic summarization: joins the first few answers.
    Can be replaced with GPT-based or extractive models later.
    """
    if not request.answers:
        return {"summary": "No input provided to summarize."}
    
    summary = " ".join(request.answers[:3])  # use top 3 to avoid long responses
    return {"summary": summary}
