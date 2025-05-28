from fastapi import FastAPI, Query
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os

app = FastAPI()

# Dummy financial data
dummy_text = """
Today, Asia tech stocks rose by 3.2% led by gains in TSMC and Samsung Electronics.
The overall AUM allocation in Asia tech now stands at 22%, up from 18% yesterday.
TSMC reported quarterly earnings beating analyst expectations by 4%, while Samsung missed by 2%.
Global investor sentiment remains cautious due to rising bond yields in the US.
"""

# Split into small chunks
splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=30)
docs = [Document(page_content=chunk) for chunk in splitter.split_text(dummy_text)]

# Embeddings + FAISS Index
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embeddings)

@app.get("/ask/")
def ask_question(query: str = Query(..., description="Enter your question")):
    result = vectorstore.similarity_search(query, k=3)
    return {
        "query": query,
        "answers": [doc.page_content for doc in result]
    }
