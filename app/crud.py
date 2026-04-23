from .models import Profile

def query_profiles(db, filters, sort_by, order, page, limit):
    query = db.query(Profile)

    # -------------------
    # FILTERS
    # -------------------
    if filters.get("gender"):
        query = query.filter(Profile.gender == filters["gender"])

    if filters.get("age_group"):
        query = query.filter(Profile.age_group == filters["age_group"])

    if filters.get("country_id"):
        query = query.filter(Profile.country_id == filters["country_id"])

    if filters.get("min_age") is not None:
        query = query.filter(Profile.age >= filters["min_age"])

    if filters.get("max_age") is not None:
        query = query.filter(Profile.age <= filters["max_age"])

    if filters.get("min_gender_probability") is not None:
        query = query.filter(
            Profile.gender_probability >= filters["min_gender_probability"]
        )

    if filters.get("min_country_probability") is not None:
        query = query.filter(
            Profile.country_probability >= filters["min_country_probability"]
        )

    # -------------------
    # SORTING (FIXED)
    # -------------------
    sort_column_map = {
        "age": Profile.age,
        "created_at": Profile.created_at,
        "gender_probability": Profile.gender_probability
    }

    column = sort_column_map.get(sort_by, Profile.created_at)

    reverse = True if order == "desc" else False

    query = query.order_by(
        column.desc() if reverse else column.asc(),
        Profile.id.desc()   # tie-breaker (VERY IMPORTANT)
    )

    # -------------------
    # TOTAL (ONLY ONCE)
    # -------------------
    total = query.count()

    # -------------------
    # PAGINATION
    # -------------------
    results = query.offset((page - 1) * limit).limit(limit).all()

    return total, results