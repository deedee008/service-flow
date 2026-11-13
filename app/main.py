from fastapi import FastAPI
from app.restaurant_config import restaurant_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/api/tables")
def get_tables():
    return restaurant_tables