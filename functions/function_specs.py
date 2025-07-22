def generate_filter_schema(amenity_columns):
    properties = {
        "internal_filter": {
            "type": "boolean",
            "description": "If true, include only internal Cortland properties"
        },
        "comp_filter": {
            "type": "boolean",
            "description": "If true, include only competitor properties"
        },
        "comp_property_filter": {
            "type": "string",
            "description": "Filter by the internal property that this property is a comp for"
        },
        "market_name_filter": {
            "type": "string",
            "description": "Filter by name of market"
        },
        "city_filter": {
            "type": "string",
            "description": "Filter by name of city"
        },
        "state_filter": {
            "type": "string",
            "description": "Filter by name of state"
        },
        "zip_filter": {
            "type": "string",
            "description": "Filter by zip code"
        },
        "style_filter": {
            "type": "string",
            "description": "Filter by style. Must be one of: Mid-Rise, Hi-Rise, Low-Rise, or Garden.",
            "enum": ["Low-Rise", "Mid-Rise", "Hi-Rise", "Garden"]
        },
        "location_filter": {
            "type": "object",
            "description": "Filter by distance from a latitude/longitude point",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude of the target location"
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude of the target location"
                },
                "max_distance_miles": {
                    "type": "number",
                    "description": "Maximum distance in miles from the target location"
                }
            },
            "required": ["latitude", "longitude", "max_distance_miles"]
        },
        "year_built_filter": {
            "type": "object",
            "description": "Filter properties based on year built",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "integer"
                }
            },
            "required": ["comparison", "value"]
        },
        "building_age_filter": {
            "type": "object",
            "description": "Filter properties based on building age in years",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "integer"
                }
            },
            "required": ["comparison", "value"]
        },
        "year_acquired_filter": {
            "type": "object",
            "description": "Filter properties based on acquisition year",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "integer"
                }
            },
            "required": ["comparison", "value"]
        },
        "year_renovated_filter": {
            "type": "object",
            "description": "Filter properties based on renovation year",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "integer"
                }
            },
            "required": ["comparison", "value"]
        },
        "num_units_filter": {
            "type": "object",
            "description": "Filter properties based on number of units",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "integer"
                }
            },
            "required": ["comparison", "value"]
        },
        "property_quality_filter": {
            "type": "object",
            "description": "Filter properties based on property quality",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "number"
                }
            },
            "required": ["comparison", "value"]
        },
        "revpasf_filter": {
            "type": "object",
            "description": "Filter properties based on their revenue per available sqft (revpasf)",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "number"
                }
            },
            "required": ["comparison", "value"]
        },
        "studio_rent_filter": {
            "type": "object",
            "description": "Filter properties based on average studio rent",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "number"
                }
            },
            "required": ["comparison", "value"]
        },
        "onebed_rent_filter": {
            "type": "object",
            "description": "Filter properties based on average one-bedroom rent",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "number"
                }
            },
            "required": ["comparison", "value"]
        },
        "twobed_rent_filter": {
            "type": "object",
            "description": "Filter properties based on average two-bedroom rent",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "number"
                }
            },
            "required": ["comparison", "value"]
        },
        "threebed_rent_filter": {
            "type": "object",
            "description": "Filter properties based on average three-bedroom rent",
            "properties": {
                "comparison": {
                    "type": "string",
                    "enum": [">=", "<=", "==", ">", "<"]
                },
                "value": {
                    "type": "number"
                }
            },
            "required": ["comparison", "value"]
        }
    }

    for amenity in amenity_columns:
        properties[f"{amenity}_filter"] = {
            "type": "boolean",
            "description": f"If true, include only properties that have {amenity.replace('_', ' ')}"
        }
        
    return [
        {
            "name": "filter_dataframe",
            "description": "Apply filters to the asset_metrics DataFrame",
            "parameters": {
                "type": "object",
                "properties": properties
            }
        }
    ]

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

function_specs = generate_filter_schema(amenity_cols)
