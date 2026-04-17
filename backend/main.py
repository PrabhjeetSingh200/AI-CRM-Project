import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from graph import graph

app = FastAPI()

# ✅ CORS (frontend connect ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request Schema
class Query(BaseModel):
    message: str

# ✅ Test route
@app.get("/")
def read_root():
    return {"message": "Backend running 🚀"}

# 🔥 MAIN AI AUTOFILL API
@app.post("/ai-fill")
def ai_fill(query: Query):
    print("API HIT:", query.message)

    result = graph.invoke({"input": query.message})

    print("RESULT:", result)

    return result