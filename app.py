import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Function to store user credentials
def store_credentials(username, password):
    with open("credentials.txt", "a") as file:
        file.write(f"{username}:{password}\n")

# Function to authenticate user
def authenticate(username, password):
    with open("credentials.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if stored_username == username and stored_password == password:
                return True
    return False

# Function to check if a username exists
def check_username(username):
    with open("credentials.txt", "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(":")
            if stored_username == username:
                return True
    return False

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success("You are now logged in as {}".format(username))
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password.")

def signup():
    st.title("Sign Up")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if check_username(new_username):
            st.error("Username already exists.")
        else:
            store_credentials(new_username, new_password)
            st.success("You have successfully signed up as {}".format(new_username))

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.markdown("<p style='font-family:Serif Fonts; font-size:40px'>Air Quality </p>", unsafe_allow_html=True)
        st.sidebar.markdown("<p style='font-family:serif;font-size:40px'>Welcome", unsafe_allow_html=True)
        st.sidebar.image('pin-42871_1920.png')
        # Load the data
        df = pd.read_csv('city_day.csv')
        # Convert the 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Preprocess the data - handling missing values for each column individually
        columns_to_fill = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'AQI']
        for column in columns_to_fill:
            df[column] = df.groupby('Date')[column].transform(lambda x: x.fillna(x.median()))
        df['AQI_Bucket'] = df['AQI_Bucket'].fillna('Moderate')

        # City coordinates approximation
        city_coordinates = {
            'Ahmedabad': (23.0225, 72.5714),
            'Aizawl': (23.7271, 92.7176),
            'Amaravati': (16.5170, 80.6376),
            'Amritsar': (31.6340, 74.8737),
            'Bengaluru': (12.9716, 77.5946),
            'Bhopal': (23.2599, 77.4126),
            'Brajrajnagar': (21.8189, 83.9222),
            'Chandigarh': (30.7333, 76.7794),
            'Chennai': (13.0827, 80.2707),
            'Coimbatore': (11.0168, 76.9558),
            'Delhi': (28.7041, 77.1025),
            'Ernakulam': (10.8505, 76.2711),
            'Gurugram': (28.4595, 77.0266),
            'Guwahati': (26.1445, 91.7362),
            'Hyderabad': (17.3850, 78.4867),
            'Jaipur': (26.9124, 75.7873),
            'Jorapokhar': (23.6751, 86.3752),
            'Kochi': (9.9312, 76.2673),
            'Kolkata': (22.5726, 88.3639),
            'Lucknow': (26.8467, 80.9462),
            'Mumbai': (19.0760, 72.8777),
            'Patna': (25.5941, 85.1376),
            'Shillong': (25.5788, 91.8933),
            'Talcher': (20.9502, 85.2074),
            'Thiruvananthapuram': (8.5241, 76.9366),
            'Visakhapatnam': (17.6868, 83.2185)
        }

        # Get user input - select city
        city = st.selectbox('Select City', df['City'].unique())

        # Get all unique dates for the selected city
        dates_for_city = df[df['City'] == city]['Date'].dt.date.unique()

        # Get user input - select date
        selected_date = st.selectbox('Select Date', dates_for_city)

        # Filter the data based on user input
        filtered_data = df[(df['City'] == city) & (df['Date'].dt.date == selected_date)]

        # Create a Folium map
        if city in city_coordinates:
            city_coords = city_coordinates[city]
            m = folium.Map(location=city_coords, zoom_start=10)
        else:
            m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Center of India

        # Add a marker cluster to the map
        marker_cluster = MarkerCluster().add_to(m)

        # Add markers to the map if there's data available for the selected city and date
        for index, row in filtered_data.iterrows():
            folium.Marker([city_coords[0], city_coords[1]],
                           popup=f'<b>{row["City"]}</b><br>{row["Date"]}<br>PM2.5: {row["PM2.5"]}<br>PM10: {row["PM10"]}<br>NO: {row["NO"]}<br>NO2: {row["NO2"]}<br>NOx: {row["NOx"]}<br>NH3: {row["NH3"]}<br>CO: {row["CO"]}<br>SO2: {row["SO2"]}<br>O3: {row["O3"]}<br>Benzene: {row["Benzene"]}<br>Toluene: {row["Toluene"]}<br>Xylene: {row["Xylene"]}<br>AQI: {row["AQI"]}<br>Air Quality: {row["AQI_Bucket"]}').add_to(marker_cluster)

        # Display the map in Streamlit
        folium_static(m, width=900, height=600)

        # Display pollutant information for all input dates
        st.subheader('Location Information')
        for index, row in filtered_data.iterrows():
            st.markdown(f"**City:** {row['City'].capitalize()}")
            st.write(f"PM2.5: {row['PM2.5']}")
            st.write(f"PM10: {row['PM10']}")
            st.write(f"NO: {row['NO']}")
            st.write(f"NO2: {row['NO2']}")
            st.write(f"NOx: {row['NOx']}")
            st.write(f"NH3: {row['NH3']}")
            st.write(f"CO: {row['CO']}")
            st.write(f"SO2: {row['SO2']}")
            st.write(f"O3: {row['O3']}")
            st.write(f"Benzene: {row['Benzene']}")
            st.write(f"Toluene: {row['Toluene']}")
            st.write(f"Xylene: {row['Xylene']}")
            st.write(f"AQI: {row['AQI']}")
            st.write(f"Air Quality: {row['AQI_Bucket']}")
            st.write('---')  # Add a separator between data points
            
            if st.button("Logout"):
                
                st.session_state.logged_in = False
                st.success("You have been logged out.")

    else:
        st.title("Login or Sign Up")
        menu = ["Login", "SignUp"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Login":
            login()
        elif choice == "SignUp":
            signup()

if __name__ == "__main__":
    main()
