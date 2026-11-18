from fastapi import FastAPI
from app.restaurant_config import restaurant_tables, demo_shift
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.services.seating_flow import find_seating_recommendation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

class RecommendationRequest(BaseModel):
    party_size: int = Field(gt = 0)
@app.get("/api/tables")
def get_tables():
    return restaurant_tables

@app.post("/api/recommendations")
def get_recommendation(request: RecommendationRequest):
    party_size = request.party_size

    recommendation = find_seating_recommendation(
        tables = restaurant_tables,
        party_size = party_size,
        shift = demo_shift
    )

    # Handle cases where no suitable seating is available
    if recommendation is None:
        return {
            "recommendation": None,
            "message": "No suitable table is available."
        }

    # Unpack the recommendation tuple into table and server objects
    table, server = recommendation

    return {
        "table_number": table.table_number,
        "server_name" : server.name
    }