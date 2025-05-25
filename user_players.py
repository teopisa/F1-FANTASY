import streamlit as st
import json
import os

def manage_users(drivers_df, season_2025, next_race):
    st.header(f"🎮 Prediction Game – {next_race['officialName']}")

    # Username (può diventare login in futuro)
    username = st.text_input("👤 Inserisci il tuo nome utente")

    if not username:
        st.warning("Inserisci un nome utente per iniziare.")
        return

    drivers_list = drivers_df['Driver'].tolist()

    with st.form("prediction_form"):
        st.subheader("🏁 Qualifiche – Top 3")
        qual_1 = st.selectbox("🥇 1° Posto (Qualifiche)", drivers_list, key="q1")
        qual_2 = st.selectbox("🥈 2° Posto", drivers_list, key="q2")
        qual_3 = st.selectbox("🥉 3° Posto", drivers_list, key="q3")

        sprint_top3 = []
        if next_race.get("sprintQualifyingFormat"):
            st.subheader("🏁 Sprint Race – Top 3")
            sprint_1 = st.selectbox("🥇 1° Posto (Sprint)", drivers_list, key="s1")
            sprint_2 = st.selectbox("🥈 2° Posto", drivers_list, key="s2")
            sprint_3 = st.selectbox("🥉 3° Posto", drivers_list, key="s3")
            sprint_top3 = [sprint_1, sprint_2, sprint_3]

        st.subheader("🏆 Gara – Podio Finale")
        race_1 = st.selectbox("🥇 Vincitore", drivers_list, key="r1")
        race_2 = st.selectbox("🥈 2° Posto (Gara)", drivers_list, key="r2")
        race_3 = st.selectbox("🥉 3° Posto (Gara)", drivers_list, key="r3")

        st.subheader("⭐ MVP della Gara")
        mvp = st.selectbox("MVP", drivers_list, key="mvp")

        st.subheader("💥 Ritiro piloti (1–3)")
        dnf = st.multiselect("Piloti che si ritireranno", drivers_list, max_selections=3)

        submitted = st.form_submit_button("✅ Invia Predizione")

        if submitted:
            prediction_data = {
                "username": username.lower(),
                "race_id": next_race["id"],
                "prediction": {
                    "qualifying_top3": [qual_1, qual_2, qual_3],
                    "sprint_top3": sprint_top3 if sprint_top3 else None,
                    "race_top3": [race_1, race_2, race_3],
                    "mvp": mvp,
                    "dnf": dnf
                },
                "points": 0
            }

            save_prediction(prediction_data)
            st.success("✅ Predizione salvata con successo!")

# 🔒 Salva prediction in JSON locale
def save_prediction(prediction, filename='predictions.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            all_predictions = json.load(file)
    else:
        all_predictions = []

    # Rimuovi eventuali duplicati per stesso utente e gara
    all_predictions = [p for p in all_predictions if not (
        p['username'] == prediction['username'] and p['race_id'] == prediction['race_id']
    )]

    all_predictions.append(prediction)

    with open(filename, 'w') as file:
        json.dump(all_predictions, file, indent=2)
