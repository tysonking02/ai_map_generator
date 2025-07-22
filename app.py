import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium
from collections.abc import MutableMapping

from agents.orchestrator import orchestrate_filtering

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            width: 350px;
        }
    </style>
""", unsafe_allow_html=True)

# Load the full dataset once
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/asset_metrics.csv")

asset_metrics = load_data()

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def safe_int(val):
    return "-" if pd.isna(val) else int(val)

def make_details(row):
    
    details = (
        f"<br><br><b>Property:</b> {row['property_name']}<br>"
        f"<b>Manager:</b> {row['manager']}<br>"
        f"<b>Owner:</b> {row['owner']}<br>"
        f"<b>Market:</b> {row['market_name']}<br>"
        f"<b>Submarket:</b> {row['submarket_name']}<br>"
        f"<b>Units:</b> {safe_int(row['unit_count'])}<br>"
        f"<b>Style:</b> {row['style']}<br>"
        f"<b>Year Built:</b> {safe_int(row['year_built'])}<br>"
        f"<b>Year Renovated:</b> {safe_int(row['year_renovated'])}<br>"
        f"<b>Year Acquired:</b> {safe_int(row['year_acquired'])}<br>"
        f"<b>Property Quality:</b> {round(row['property_quality'], 3)}<br>"
    )

    return details

# Text to Map Generator
st.sidebar.title("Text-to-Map Generator")

with st.sidebar.expander('Features that you can filter:'):
    st.markdown("""
    - **Internal/Comps Only:**
        - Show only **internal Cortland** properties
        - Show only **competitor** properties
    - **Comp Property:** Filter by the internal property that a comp is associated with
    - **Market/City/State/Zip:**
        - Filter by **market**, **city**, **state**, or **zip code**
    - **Style:** Filter by building style (Low-Rise, Mid-Rise, Hi-Rise, Garden)
    - **Location Radius:** 
        - Provide a location and **max distance in miles** to show nearby properties
    - **Year Built / Acquired / Renovated:**
        - e.g., properties **built after 2015**, or **renovated before 2000**
    - **Building Age:** 
        - Filter by age of property in years (e.g., **less than 10 years old**)
    - **Number of Units:**
        - e.g., properties with **at least 200 units**
    - **Property Quality Rating:**
        - Filter by property quality score (0-1 scale)
    - **Amenities:**
        - Filter for properties that have a **pool**, **fitness center**, **concierge**, etc.
    - **Rent Ranges by Unit Type:**
        - Filter based on **studio**, **1BR**, **2BR**, or **3BR** rent values
    """)

user_query = st.sidebar.text_input("Enter your query:")
submit = st.sidebar.button("Submit")

if submit and user_query.strip():
    try:
        tool_args, filtered = orchestrate_filtering(user_query, asset_metrics)

        st.success(f"Found {len(filtered)} matching properties.")

        with st.expander("Filters applied:"):
            flat_args = flatten_dict(tool_args)
            st.dataframe(pd.DataFrame(flat_args.items(), columns=["Filter", "Value"]))
    
        display_columns = ['property_name', 'comp', 'comp_property', 'revpasf', 'manager', 'owner', 'property_address', 'city', 'state', 'market_name', 'submarket_name',
                                'unit_count', 'number_of_stories', 'style', 'building_age', 'years_since_reno', 'years_since_acquisition',
                                'property_quality', 'studio_rent', 'onebed_rent', 'twobed_rent', 'threebed_rent']
        
        for key in tool_args:
            if key.endswith("_filter"):
                base_col = key.replace("_filter", "")
                if base_col in filtered.columns and base_col not in display_columns:
                    display_columns.append(base_col)

        with st.expander("Properties found:"):
            display_df = filtered[display_columns]
            st.dataframe(display_df)

    except Exception as e:
        st.error(f"Something went wrong:\n\n{str(e)}")

    filtered['Details'] = filtered.apply(lambda row: make_details(row), axis=1)

    center_lat = filtered['latitude'].mean()
    center_lon = filtered['longitude'].mean()

    lat_range = filtered['latitude'].max() - filtered['latitude'].min()
    lon_range = filtered['longitude'].max() - filtered['longitude'].min()
    max_range = max(lat_range, lon_range)

    if max_range < 0.01:
        zoom = 15
    elif max_range < 0.05:
        zoom = 13
    elif max_range < 0.1:
        zoom = 12
    elif max_range < 0.5:
        zoom = 11
    elif max_range < 1:
        zoom = 10
    else:
        zoom = 4

    m = leafmap.Map()
    m.add_basemap("CartoDB.Positron")

    internal = filtered[filtered["internal"] == True]
    external = filtered[filtered["internal"] == False]

    m.add_circle_markers_from_xy(
        data=external,
        x='longitude',
        y='latitude',
        popup=['Details'],
        layer_name='Properties',
        radius=6,
        fill_opacity=0.3,
        stroke=False,
        show=True
    )

    cortland_icon = folium.CustomIcon(
        icon_image='cortland_logo.png',
        icon_size=(24, 24),
    )

    for _, row in internal.iterrows():
        popup = folium.Popup(row["Details"], max_width=300)
        m.add_marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=cortland_icon
        )

    if "location_filter" in tool_args:
        loc = tool_args["location_filter"]
        if "latitude" in loc and "longitude" in loc:
            lat = loc["latitude"]
            lon = loc["longitude"]
            distance_miles = loc.get("max_distance_miles", 1)
            distance_meters = distance_miles * 1609.34

            # Add dashed circle
            folium.Circle(
                location=[lat, lon],
                radius=distance_meters,
                color='blue',
                fill=False,
                dash_array='5,5',
                weight=2
            ).add_to(m)


    m.set_center(lat=center_lat, lon=center_lon, zoom=zoom)

    m.to_streamlit(height=700)
