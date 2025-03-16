import streamlit as st
import json

# Load your JSON file (replace with the path to your downloaded F1DB data)
with open('f1db.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Get the 2025 season data
season_2025 = next((season for season in data['seasons'] if season['year'] == 2025), None)

# Streamlit UI Setup
st.title('F1DB Data Exploration')

# Sidebar for navigation
option = st.sidebar.selectbox(
    'What would you like to explore?',
    ('2025 Data', 'Constructors List', 'Drivers List')
)

# Function to extract constructors and drivers from 2025 entrants
def extract_entrants_2025():
    entrants_2025 = []
    constructors_list = []
    drivers_list = []

    # Loop through each entrant in 2025 season
    for entrant in season_2025.get('entrants', []):
        entrant_id = entrant['entrantId']
        constructors = entrant.get('constructors', [])
        
        for constructor in constructors:
            constructor_data = {
                'entrantId': entrant_id,
                'constructorId': constructor['constructorId'],
            }
            constructors_list.append(constructor_data)
            
            # Loop through each driver in the constructor's drivers and extract their driverId
            for driver_info in constructor.get('drivers', []):
                driver_data = {
                    'driverId': driver_info['driverId'],
                    'driverName': driver_info['driverId'].replace('-', ' ').title(),
                    'constructorId': constructor['constructorId']
                }
                drivers_list.append(driver_data)

    return constructors_list, drivers_list

# Extract data
constructors_list, drivers_list = extract_entrants_2025()

# Display data based on user selection
if option == '2025 Data':
    st.write("### 2025 Season Data (Entrants, Constructors, and Drivers)")
    st.write(season_2025)

elif option == 'Constructors List':
    st.write("### List of Constructors in 2025")
    constructor_names = [constructor['constructorId'].title() for constructor in constructors_list]
    st.write(constructor_names)

elif option == 'Drivers List':
    st.write("### List of Drivers in 2025")
    driver_names = [f"{driver['driverName']} ({driver['constructorId'].title()})" for driver in drivers_list]
    st.write(driver_names)
