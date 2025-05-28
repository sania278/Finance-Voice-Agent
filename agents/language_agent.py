from fastapi import FastAPI, Body
from transformers import pipeline

app = FastAPI()

# Load local HuggingFace model (Flan-T5-small)
summarizer = pipeline("text2text-generation", model="google/flan-t5-small")

@app.post("/summarize/")
def summarize_answer(answers: list = Body(..., embed=True)):
    # Combine retrieved chunks into one prompt
    combined_input = " ".join(answers)
    prompt = f"Summarize this like a financial advisor would: {combined_input}"

    result = summarizer(prompt, max_length=100, do_sample=False)
    return {
        "summary": result[0]['generated_text']
    }
