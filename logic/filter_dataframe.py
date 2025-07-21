import pandas as pd
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Radius of Earth in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def apply_filter(df: pd.DataFrame, args: dict) -> pd.DataFrame:
    df = df.copy()

    # Boolean filters
    if args.get("internal_only") is True:
        df = df[df["internal"] == True]

    if args.get("comps_only") is True:
        df = df[df["comp"] == True]

    # Exact match filters
    if comp_property := args.get("comp_property_filter"):
        df = df[df["comp_property"] == comp_property]

    if market := args.get("market_filter"):
        df = df[df["market_name"] == market]

    if city := args.get("city_filter"):
        df = df[df["city"] == city]

    if state := args.get("state_filter"):
        df = df[df["state"] == state]

    if zip := args.get("zip_filter"):
        df = df[df["zip_code"] == zip]

    if style := args.get("style_filter"):
        df = df[df["style"] == style]

    # Distance filtering
    if loc := args.get("location_filter"):
        lat, lon = loc["latitude"], loc["longitude"]
        max_miles = loc["max_distance_miles"]
        df["distance"] = df.apply(
            lambda row: haversine(lat, lon, row["latitude"], row["longitude"]), axis=1
        )
        df = df[df["distance"] <= max_miles]

    # Numeric field filters with comparison
    comparison_fields = {
        "year_built_filter": "year_built",
        "building_age_filter": "building_age",
        "year_acquired_filter": "year_acquired",
        "year_renovated_filter": "year_renovated",
        "num_units_filter": "num_units"
    }

    for arg_key, column in comparison_fields.items():
        if f := args.get(arg_key):
            comp = f["comparison"]
            val = f["value"]
            if comp in [">", ">=", "<", "<=", "=="]:
                df = df.query(f"{column} {comp} @val")

    return df
