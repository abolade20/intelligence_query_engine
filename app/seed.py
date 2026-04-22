import json
from datetime import datetime
from .database import SessionLocal, engine
from .models import Base, Profile

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    with open("seed_profiles.json", "r", encoding="utf-8") as f:
        data = json.load(f)["profiles"]

    for item in data:
        exists = db.query(Profile).filter(Profile.name == item["name"]).first()
        if exists:
            continue

        profile = Profile(
            name=item["name"],
            gender=item["gender"],
            gender_probability=item["gender_probability"],
            age=item["age"],
            age_group=item["age_group"],
            country_id=item["country_id"],
            country_name=item["country_name"],
            country_probability=item["country_probability"],
        )

        db.add(profile)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()