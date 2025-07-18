from filter_data import filter_data
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap

st.title('Text-to-Map Generator')

asset_metrics = pd.read_csv('data/processed/asset_metrics.csv')

with st.expander('Example Queries:'):
    st.markdown("""
    - Plot our properties in **X market/city/zip**
    - Plot our comps in **X market/city/zip**
    - Map properties built after **2015**
    - Plot all properties within **3 miles of downtown Dallas**
    - Plot our acquisitions in the **last 3 years**
    - Map our properties that **haven't been renovated since at least 2000**
    - Plot all properties within **1 mile of the Old Fourth Ward** with **at least 200 units**   
    - Map all high-rises within **3 miles of Buckhead**      
    - *Any combination of the above ^^*
    """)

user_input = st.text_area("Request the information that you'd like to be mapped:")

def safe_int(val):
    return "-" if pd.isna(val) else int(val)

def make_details(row):
    return (
        f"<br><br><b>Property:</b> {row['property_name']}<br>"
        f"<b>Manager:</b> {row['manager']}<br>"
        f"<b>Owner:</b> {row['owner']}<br>"
        f"<b>Location:</b> {row['city']}, {row['state']}<br>"
        f"<b>Market:</b> {row['market_name']}<br>"
        f"<b>Submarket:</b> {row['submarket_name']}<br>"
        f"<b>Units:</b> {safe_int(row['unit_count'])}<br>"
        f"<b>Star Rating:</b> {safe_int(row['star_rating'])}<br>"
        f"<b>Year Built:</b> {safe_int(row['year_built'])}<br>"
        f"<b>Year Renovated:</b> {safe_int(row['year_renovated'])}<br>"
        f"<b>Year Acquired:</b> {safe_int(row['year_acquired'])}"
    )

if st.button("Run"):
    response, filtered_df = filter_data(asset_metrics, user_input)

    if not filtered_df.empty:

        filtered_df['Details'] = filtered_df.apply(make_details, axis=1)
        center_lat = filtered_df['latitude'].mean()
        center_lon = filtered_df['longitude'].mean()

        lat_range = filtered_df['latitude'].max() - filtered_df['latitude'].min()
        lon_range = filtered_df['longitude'].max() - filtered_df['longitude'].min()
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

        with st.expander("Details"):
            st.code(response)
            st.dataframe(filtered_df, use_container_width=True)

        m = leafmap.Map()
        m.add_basemap("CartoDB.Positron")

        m.add_circle_markers_from_xy(
            data=filtered_df,
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
    
    else:
        st.warning("No data to display on map.")
        center_lat, center_lon, zoom = 0, 0, 2 