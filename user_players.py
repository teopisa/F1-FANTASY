import streamlit as st
import pandas as pd

# ---------------------- USER MANAGEMENT ---------------------- #
def manage_users(drivers_df, season_2025):
    """Handles user registration & prediction storage."""
    if "users" not in st.session_state:
        st.session_state.users = {}

    option = st.sidebar.radio("Select an Option", ["Join the League", "Predict Grand Prix", "Leaderboard", "2025 Data"])

    # User Registration
    if option == "Join the League":
        st.header("🏁 Join the F1 Prediction League")
        username = st.text_input("Enter your nickname:")

        if st.button("Join Now"):
            if username.strip() and username not in st.session_state.users:
                st.session_state.users[username] = {"predictions": {}}
                st.success(f"Welcome {username}! You have joined the league. 🏆")
            elif username in st.session_state.users:
                st.warning("This nickname is already taken! Try another one.")

    # Predict Grand Prix
    elif option == "Predict Grand Prix":
        st.header("🔮 Predict the Grand Prix Winners")

        if not st.session_state.users:
            st.warning("Join the league first before making predictions!")
        else:
            username = st.selectbox("Select Your Nickname:", list(st.session_state.users.keys()))
            race_round = st.selectbox("Select the Grand Prix Round:", list(range(1, 24)))

            st.subheader("Select Your Top 3 Drivers:")
            pick_1 = st.selectbox("🏆 Winner", drivers_df["Driver"])
            pick_2 = st.selectbox("🥈 Second Place", drivers_df["Driver"])
            pick_3 = st.selectbox("🥉 Third Place", drivers_df["Driver"])

            if st.button("Submit Prediction"):
                st.session_state.users[username]["predictions"][race_round] = [pick_1, pick_2, pick_3]
                st.success(f"Prediction for Round {race_round} saved!")

    # Leaderboard
    elif option == "Leaderboard":
        st.header("🏆 F1 2025 Leaderboard")

        if not st.session_state.users:
            st.warning("No players have joined yet!")
        else:
            leaderboard_data = []
            for user, data in st.session_state.users.items():
                total_points = len(data["predictions"]) * 10  # Example: 10 points per prediction
                leaderboard_data.append({"User": user, "Points": total_points})

            leaderboard_df = pd.DataFrame(leaderboard_data).sort_values(by="Points", ascending=False)
            st.table(leaderboard_df)

    # Show 2025 JSON Data
    elif option == "2025 Data":
        st.header("📜 Full 2025 Season Data")
        st.write(season_2025)