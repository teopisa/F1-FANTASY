import streamlit as st
import requests
import zipfile
import io
import os
from datetime import datetime

def aggiorna_db(path_locale="f1db.json"):
    """
    Scarica l'ultima versione del DB F1 in formato JSON dal repository GitHub
    e salva il file localmente.
    """
    url_zip = "https://github.com/f1db/f1db/releases/latest/download/f1db-json-single.zip"

    try:
        st.info("📦 Scaricamento del database in corso...")
        response = requests.get(url_zip)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            json_trovato = False
            for file in z.namelist():
                if file.endswith(".json"):
                    z.extract(file, path=".")
                    os.replace(file, path_locale)
                    json_trovato = True
                    break

            if not json_trovato:
                st.error("❌ Nessun file JSON trovato nello ZIP.")
                return

        st.success("✅ Database aggiornato con successo!")

    except Exception as e:
        st.error(f"❌ Errore durante l'aggiornamento del database: {e}")

def get_ultimo_aggiornamento(path_locale="f1db.json"):
    """
    Restituisce la data e ora dell'ultima modifica del file JSON locale.
    """
    if not os.path.exists(path_locale):
        return "File DB non trovato."
    ts = os.path.getmtime(path_locale)
    data_agg = datetime.fromtimestamp(ts)
    return f"Ultimo aggiornamento DB: {data_agg.strftime('%Y-%m-%d %H:%M:%S')}"

def ultima_gara_disponibile(season_2025):
    """
    Trova l'ultima gara del 2025 disponibile nel DB.
    """
    if not season_2025 or "races" not in season_2025:
        return "Nessuna informazione disponibile."

    gare_con_date = [
        race for race in season_2025["races"]
        if race.get("date") is not None
    ]

    if not gare_con_date:
        return "Nessuna gara con data trovata."

    ultima = max(gare_con_date, key=lambda r: r["date"])
    data_gara = datetime.strptime(ultima["date"], "%Y-%m-%d").date()
    return f"📅 Ultima gara nel DB: **{ultima['officialName']}** il **{data_gara}**"
