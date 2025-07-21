import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

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

def safe_int(val):
    return "-" if pd.isna(val) else int(val)

def make_details(row, comp):
    
    details = (
        f"<br><br><b>Property:</b> {row['property_name']}<br>"
        f"<b>Manager:</b> {row['manager']}<br>"
        f"<b>Owner:</b> {row['owner']}<br>"
        f"<b>Location:</b> {row['city']}, {row['state']}<br>"
        f"<b>Market:</b> {row['market_name']}<br>"
        f"<b>Submarket:</b> {row['submarket_name']}<br>"
        f"<b>Units:</b> {safe_int(row['unit_count'])}<br>"
        f"<b>Style:</b> {row['style']}<br>"
        f"<b>Year Built:</b> {safe_int(row['year_built'])}<br>"
        f"<b>Year Renovated:</b> {safe_int(row['year_renovated'])}<br>"
        f"<b>Year Acquired:</b> {safe_int(row['year_acquired'])}<br>"
    )

    if comp and not pd.isna(row.get('comp_property')):
        details += f"<b>Comp Property:</b> {row['comp_property']}<br>"

    return details

# UI
st.sidebar.title("Text-to-Map Generator")

with st.sidebar.expander('Example Queries:'):
    st.markdown("""
    - Plot our properties in:
        - market
        - city
        - state
        - zip code
    - Plot our comps in:
        - market
        - city
        - state
        - zip code
    - Map properties built after **2015**
    - Plot all properties within **3 miles of downtown Dallas**
    - Plot our acquisitions in the **last 3 years**
    - Map our properties that **haven't been renovated since at least 2000**
    - Plot all properties within **1 mile of the Old Fourth Ward** with **at least 200 units**   
    - Map all high-rises within **3 miles of Buckhead**      
    - *Any combination of the above filters^^*
    """)

user_query = st.sidebar.text_input("Enter your query:")
submit = st.sidebar.button("Submit")

if submit and user_query.strip():
    try:
        tool_args, filtered = orchestrate_filtering(user_query, asset_metrics)

        with st.sidebar.expander("Filters applied:"):
            st.dataframe(tool_args)

        st.success(f"Found {len(filtered)} matching properties.")
    
        with st.expander("Properties found:"):
            st.dataframe(filtered)

    except Exception as e:
        st.error(f"Something went wrong:\n\n{str(e)}")

    filtered['Details'] = filtered.apply(lambda row: make_details(row, comp='comp_property' in row), axis=1)

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

    m.add_circle_markers_from_xy(
        data=filtered,
        x='longitude',
        y='latitude',
        popup=['Details'],
        layer_name='Properties',
        radius=6,
        fill_opacity=0.3,
        stroke=False,
        show=True
    )

    m.set_center(lat=center_lat, lon=center_lon, zoom=zoom)

    m.to_streamlit(height=700)
