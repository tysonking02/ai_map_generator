function_specs = [
    {
        "name": "filter_dataframe",
        "description": "Apply filters to the asset_metrics DataFrame",
        "parameters": {
            "type": "object",
            "properties": {
                "internal_only": {
                    "type": "boolean",
                    "description": "If true, include only internal Cortland properties"
                },
                "comps_only": {
                    "type": "boolean",
                    "description": "If true, include only competitor properties"
                },
                "comp_property_filter": {
                    "type": "string",
                    "description": "Filter by the internal property that this property is a comp for"
                },
                "market_filter": {
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
                }
            }
        }
    }
]
