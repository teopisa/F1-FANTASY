import streamlit as st
import json
import pandas as pd
from data_extraction import *
from user_players import * 

# Load JSON Data (Replace with correct path)
with open('f1db.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract 2025 Season Data
season_2025 = next((season for season in data['seasons'] if season['year'] == 2025), None)

# Get Drivers & Constructors DataFrames
drivers_df, constructors_df = extract_f1_data(season_2025)

# ---------------------- STREAMLIT APP ---------------------- #
def streamlit_app():
    """Main Streamlit UI."""
    st.title("🏎️ F1 2025 Prediction Game")
    
    # Sidebar Navigation
    menu = st.sidebar.radio("Select a View", ["Drivers", "Constructors", "Game"])
    
    if menu == "Drivers":
        st.header("🏁 2025 Drivers List")
        st.dataframe(drivers_df)

    elif menu == "Constructors":
        st.header("🏎️ 2025 Constructors List")
        st.dataframe(constructors_df)

    elif menu == "Game":
        manage_users(drivers_df=drivers_df, season_2025= season_2025)

# Run Streamlit App
if __name__ == "__main__":
    streamlit_app()
