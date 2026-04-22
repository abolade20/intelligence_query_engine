def parse_query(q: str):
    q = q.lower()
    filters = {}

    # gender
    if "male" in q and "female" in q:
        pass

    elif "male" in q:
        filters["gender"] = "male"

    elif "female" in q:
        filters["gender"] = "female"

    # age keywords
    if "young" in q:
        filters["min_age"] = 16
        filters["max_age"] = 24

    if "above" in q:
        try:
            filters["min_age"] = int(q.split("above")[1].split()[0])
        except:
            pass

    if "below" in q:
        try:
            filters["max_age"] = int(q.split("below")[1].split()[0])
        except:
            pass

    # age groups
    for g in ["child", "teenager", "adult", "senior"]:
        if g in q:
            filters["age_group"] = g

    # country mapping (expand if needed)
    country_map = {
        "nigeria": "NG",
        "kenya": "KE",
        "angola": "AO",
        "uganda": "UG",
        "tanzania": "TZ",
    }

    for name, code in country_map.items():
        if name in q:
            filters["country_id"] = code

    return filters if filters else None