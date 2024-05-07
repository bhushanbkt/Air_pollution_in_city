import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Load your data
mean_years = pd.read_csv('mean_years.csv')

# Create a Streamlit app
st.title('Pollution Map')

# User inputs
locations = mean_years['City'].unique()
location = st.sidebar.selectbox('Select Location/Area', locations)
year = st.sidebar.selectbox('Select Year', ['2019', '2020'])

# Filter data based on user input
filtered_data = mean_years[mean_years['City'] == location]

# Display the map
if not filtered_data.empty:
    st.subheader('Map')
    m = folium.Map(location=[filtered_data['Lat'].iloc[0], filtered_data['Long'].iloc[0]], zoom_start=10)
    
    marker_cluster = MarkerCluster().add_to(m)

    for index, row_values in filtered_data.iterrows():
        popup_html = f'<strong>City</strong>: {row_values["City"].capitalize()}<br>'
        popup_html += f'<strong>AQI 2018</strong>: {row_values["AQI_2018"]}<br>'
        popup_html += f'<strong>AQI 2019</strong>: {row_values["AQI_2019"]}<br>'
        popup_html += f'<strong>AQI 2020</strong>: {row_values["AQI_2020"]}<br>'
        popup_html += f'<strong>Percentage Decrease</strong>: {row_values["pct_decrease"]}<br>'
        popup_html += f'<strong>Country</strong>: {row_values["country"]}<br>'
        popup_html += f'<strong>ISO2</strong>: {row_values["iso2"]}<br>'
        popup_html += f'<strong>State</strong>: {row_values["State"]}<br>'

        folium.Marker(
            location=[row_values['Lat'], row_values['Long']],
            popup=folium.Popup(popup_html, max_width=500),
            icon=folium.Icon(color='red' if year == '2019' else 'orange', icon='info-sign')
        ).add_to(marker_cluster)

    # Display the map in Streamlit
    # folium_static(m)
    folium_static(m, width=900, height=600)


    
    st.subheader('AQI Trends')
    fig = px.line(filtered_data, x='City', y=[f"AQI_{year}" for year in range(2018, 2021)],
                  title='AQI Trends Over the Years')
    st.plotly_chart(fig)
    

    st.subheader('Location Information')
    for index, row in filtered_data.iterrows():
        st.markdown(f"**City:** {row['City'].capitalize()}")
        st.write(f"AQI 2018: {row['AQI_2018']}")
        st.write(f"AQI 2019: {row['AQI_2019']}")
        st.write(f"AQI 2020: {row['AQI_2020']}")
        st.write(f"Percentage Decrease: {row['pct_decrease']}")
        st.write(f"Country: {row['country']}")
        st.write(f"ISO2: {row['iso2']}")
        st.write(f"State: {row['State']}")
        st.write('---')  # Add a separator between data points
else:
    st.warning("No data available for the selected location. Please choose another location.")
