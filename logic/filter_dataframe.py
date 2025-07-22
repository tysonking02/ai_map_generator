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

amenity_cols = [
    "air_conditioning", "business_center", "controlled_access", "clubhouse", "fitness_center",
    "laundry_facilities", "pool", "dry_cleaning_service", "gameroom", "grill", "on-site_retail",
    "package_service", "smoke_free", "roof_terrace", "24_hour_access", "fenced_lot",
    "planned_social_activities", "conference_rooms", "elevator", "online_services", "dining_room",
    "recreation_room", "wheelchair_accessible_(rooms)", "picnic_area", "gated",
    "breakfast/coffee_concierge", "disposal_chutes", "media_center/movie_theatre",
    "trash_pickup_-_door_to_door", "wi-fi", "maintenance_on_site", "island_kitchen", "linen_closet",
    "pantry", "patio", "courtyard", "property_manager_on_site", "spa", "lounge", "deck", "sauna",
    "basketball_court", "doorman", "storage_space", "den", "loft_layout", "window_coverings",
    "sundeck", "laundry_service", "yard", "concierge", "energy_star_labeled", "car_wash_area",
    "guest_apartment", "maid_service", "pet_play_area", "recycling", "bicycle_storage",
    "grocery_service", "pet_care", "garden", "public_transportation", "furnished_units_available",
    "tenant_controlled_hvac", "trash_pickup_-_curbside", "corporate_suites",
    "renters_insurance_program", "tennis_court", "playground", "cabana", "shuttle_to_train",
    "racquetball_court", "walking/biking_trails", "hearing_impaired_accessible", "multi_use_room",
    "vision_impaired_accessible", "handrails", "trash_compactor", "vinyl_flooring",
    "warming_drawer", "individual_locking_bedrooms", "private_bathroom", "vintage_building",
    "skylights", "instant_hot_water", "intercom", "tanning_salon", "health_club_discount",
    "breakfast_nook", "security_system", "video_patrol", "waterfront", "dock", "gas_range",
    "built-in_bookshelves", "double_pane_windows", "freezer", "volleyball_court", "office",
    "family_room", "pond", "porch", "community-wide_wifi", "basement", "green_community",
    "zen_garden", "key_fob_entry", "putting_greens", "pet_washing_station", "lawn",
    "car_charging_station", "workshop", "on-site_atm", "day_care", "study_lounge", "framed_mirrors",
    "walk_to_campus", "house_sitter_services", "composting", "coffee_system", "meal_service",
    "wet_bar", "google_fiber", "mother-in-law_unit", "greenhouse", "lake_access",
    "roommate_matching", "vacuum_system", "attic", "individual_leases_available", "golf_course"
]

def apply_filter(df, args):
    df = df.copy()

    # Boolean filters
    if args.get("internal_filter") is True:
        df = df[df["internal"] == True]

    if args.get("comp_filter") is True:
        df = df[df["comp"] == True]

    # Exact match filters
    if comp_property := args.get("comp_property_filter"):
        df = df[df["comp_property"] == comp_property]

    if market := args.get("market_name_filter"):
        df = df[df["market_name"] == market]

    if city := args.get("city_filter"):
        df = df[df["city"] == city]

    if state := args.get("state_filter"):
        df = df[df["state"] == state]

    if zip := args.get("zip_filter"):
        df = df[df["zip_code"] == zip]

    if style := args.get("style_filter"):
        df = df[df["style"] == style]

    for amenity in amenity_cols:
        arg_key = f"{amenity}_filter"
        if arg_key in args:
            df = df[df[amenity] == int(args[arg_key])]

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
        "num_units_filter": "unit_count",
        "property_quality_filter": "property_quality",
        "studio_rent_filter": "studio_rent",
        "onebed_rent_filter": "onebed_rent",
        "twobed_rent_filter": "twobed_rent",
        "threebed_rent_filter": "threebed_rent",
        "revpasf_filter": "revpasf"
    }

    for arg_key, column in comparison_fields.items():
        if f := args.get(arg_key):
            comp = f["comparison"]
            val = f["value"]
            if comp in [">", ">=", "<", "<=", "=="]:
                df = df.query(f"{column} {comp} @val")

    return df
