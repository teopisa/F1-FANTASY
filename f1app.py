import streamlit as st
import json
import pandas as pd
from datetime import datetime
from data_extraction import filtra_dati_stagione, trova_prossima_gara
from user_players import manage_users
from result_races import estrai_risultati_gara  # <-- nuova importazione

# Carica il file JSON
with open('f1db.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Estrai dati stagione 2025
stagione, races_df, drivers_df, constructors_df = filtra_dati_stagione(data, 2025)

# Trova prossima gara
next_race = trova_prossima_gara(races_df)

# Gare passate (per F1Result)
oggi = datetime.now().date()
gare_passate_df = races_df[races_df["date"].apply(lambda d: datetime.strptime(d, "%Y-%m-%d").date() < oggi)]

def streamlit_app():
    st.set_page_config(page_title="F1 Fantasy 2025", layout="centered")
    st.title("🏎️ F1 2025 Prediction Game")

    # Aggiorna DB (assumo aggiorna_db è in aggiornamento_db.py)
    from aggiornamento_db import aggiorna_db  
    if st.sidebar.button("🔄 Aggiorna Database"):
        aggiorna_db()
        st.experimental_rerun()

    # Menu principale
    menu = st.sidebar.radio("Navigazione", ["🏁 Game", "📊 Info Data"])

    if menu == "🏁 Game":
        sub_menu = st.sidebar.radio("Game Menu", ["Gestione Squadra", "F1Result"])

        if sub_menu == "Gestione Squadra":
            manage_users(drivers_df=drivers_df, season_2025=stagione, next_race=next_race)

        elif sub_menu == "F1Result":
            st.header("📋 Risultati Gare Passate 2025")
            if gare_passate_df.empty:
                st.warning("Nessuna gara passata trovata nel DB.")
                return
            
            # Selettore gara
            race_selected = st.selectbox(
                "Seleziona una gara",
                options=gare_passate_df["grandPrixId"],
                format_func=lambda gp_id: f"{gp_id} - {races_df[races_df['grandPrixId'] == gp_id]['date'].values[0]}"
            )

            # Estrai dati gara selezionata per il 2025
            gara_dettagli = estrai_risultati_gara(data, race_selected, 2025)
            if gara_dettagli is None:
                st.error("Dettagli gara 2025 non trovati.")
                return
            
            st.subheader(f"Risultati per {gara_dettagli.get('grandPrixId', 'N/D')} - {gara_dettagli.get('date', '')}")
            
            # Mostra risultati qualifiche
            qualifiche = gara_dettagli.get("qualifyingResults", [])
            if qualifiche:
                st.markdown("### Qualifiche")
                qual_df = pd.DataFrame(qualifiche)
                st.dataframe(qual_df)
            else:
                st.info("Nessun risultato qualifiche disponibile.")
            
            # Mostra risultati gara
            gara = gara_dettagli.get("raceResults", [])
            if gara:
                st.markdown("### Gara")
                race_df = pd.DataFrame(gara)
                st.dataframe(race_df)
            else:
                st.info("Nessun risultato gara disponibile.")

    elif menu == "📊 Info Data":
        sub_menu = st.sidebar.radio("Dati", ["Drivers", "Constructors", "Races"])
        if sub_menu == "Drivers":
            st.header("👨‍✈️ Piloti 2025")
            st.dataframe(drivers_df)
        elif sub_menu == "Constructors":
            st.header("🏭 Team 2025")
            st.dataframe(constructors_df)
        elif sub_menu == "Races":
            st.header("📆 Gare 2025")
            st.dataframe(races_df)

if __name__ == "__main__":
    streamlit_app()
