from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Profile
from .crud import query_profiles
from .parser import parse_query

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def error(message: str):
    return {"status": "error", "message": message}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def serialize_profile(p):
    return {
        "id": p.id,
        "name": p.name,
        "gender": p.gender,
        "gender_probability": p.gender_probability,
        "age": p.age,
        "age_group": p.age_group,
        "country_id": p.country_id,
        "country_name": p.country_name,
        "country_probability": p.country_probability,
        "created_at": p.created_at.isoformat() + "Z" if p.created_at else None
    }

@app.get("/api/profiles")
def get_profiles(
    gender: str = None,
    age_group: str = None,
    country_id: str = None,
    min_age: int = None,
    max_age: int = None,
    min_gender_probability: float = None,
    min_country_probability: float = None,
    sort_by: str = None,
    order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    
    VALID_SORT_FIELDS = ["age", "created_at", "gender_probability"]

    if sort_by and sort_by not in VALID_SORT_FIELDS:
        return error("Invalid query parameters")

    if order not in ["asc", "desc"]:
        return error("Invalid query parameters")

    if limit > 50 or page < 1:
        return error("Invalid query parameters")
    

    filters = {
        "gender": gender,
        "age_group": age_group,
        "country_id": country_id,
        "min_age": min_age,
        "max_age": max_age,
        "min_gender_probability": min_gender_probability,
        "min_country_probability": min_country_probability
    }

    total, data = query_profiles(db, filters, sort_by, order, page, limit)

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": [serialize_profile(p) for p in data]
    }

@app.get("/api/profiles/search")
def search(q: str, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):

    # -------------------
    # VALIDATION FIX
    # -------------------
    if q is None or not isinstance(q, str) or q.strip() == "":
        return error("Invalid query parameters")

    if len(q) > 200:
        return error("Invalid query parameters")

    filters = parse_query(q)

    if not filters:
        return error("Unable to interpret query")

    total, data = query_profiles(db, filters, "created_at", "desc", page, limit)

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": [serialize_profile(p) for p in data]
    }