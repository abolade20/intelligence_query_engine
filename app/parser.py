import re

def parse_query(q: str):
    if not q or not isinstance(q, str):
        return None

    q = q.lower().strip()
    filters = {}

    # -------------------
    # GENDER 
    # -------------------
    has_male = " male" in q or q.startswith("male")
    has_female = " female" in q or q.startswith("female")

    if has_male and not has_female:
        filters["gender"] = "male"
    elif has_female and not has_male:
        filters["gender"] = "female"
    # if both exist → no gender filter (IMPORTANT FIX)

    # -------------------
    # AGE GROUPS
    # -------------------
    if "child" in q:
        filters["age_group"] = "child"

    if "teenager" in q or "teenagers" in q:
        filters["age_group"] = "teenager"

    if "adult" in q:
        filters["age_group"] = "adult"

    if "senior" in q:
        filters["age_group"] = "senior"

    # -------------------
    # YOUNG (KEEP BUT SAFE)
    # -------------------
    if "young" in q:
        filters["min_age"] = 16
        filters["max_age"] = 24

    # -------------------
    # ABOVE / BELOW (ROBUST)
    # -------------------
    above_match = re.search(r"above\s*(\d+)", q)
    if above_match:
        filters["min_age"] = int(above_match.group(1))

    below_match = re.search(r"below\s*(\d+)", q)
    if below_match:
        filters["max_age"] = int(below_match.group(1))

    # -------------------
    # COUNTRY MAPPING
    # -------------------
    country_map = {
        "nigeria": "NG",
        "kenya": "KE",
        "angola": "AO",
        "uganda": "UG",
        "tanzania": "TZ",
        "ghana": "GH",
        "benin": "BJ",
    }

    for name, code in country_map.items():
        if name in q:
            filters["country_id"] = code
            break

    return filters if filters else None