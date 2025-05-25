import pandas as pd
from datetime import datetime

def filtra_dati_stagione(data, anno):
    # Estrai la stagione specifica
    stagione = next((s for s in data['seasons'] if s['year'] == anno), None)

    # Filtra le gare di quell'anno
    all_races = [r for r in data.get("races", []) if r["year"] == anno]
    races_df = pd.DataFrame(all_races)[[
        "grandPrixId", "round", "date", "time", 
        "qualifyingFormat", "sprintQualifyingFormat", 
        "turns", "laps"
    ]]

    # Ottieni gli ID dei piloti presenti in almeno una gara della stagione
    driver_ids = set()
    constructor_ids = set()
    for race in all_races:
        if race.get("raceResults"):
            for result in race["raceResults"]:
                driver_ids.add(result["driverId"])
                constructor_ids.add(result["constructorId"])
    
    # Filtra i piloti
    all_drivers = pd.DataFrame(data["drivers"])
    drivers_df = all_drivers[all_drivers["id"].isin(driver_ids)][
        ["name", "permanentNumber", "nationalityCountryId"]
    ]

    # Filtra i costruttori
    all_constructors = pd.DataFrame(data["constructors"])
    constructors_df = all_constructors[all_constructors["id"].isin(constructor_ids)][
        ["name", "countryId"]
    ]

    return stagione, races_df.reset_index(drop=True), drivers_df.reset_index(drop=True), constructors_df.reset_index(drop=True)

def trova_prossima_gara(races_df):
    oggi = datetime.now().date()
    future_races = races_df[races_df["date"].apply(lambda d: datetime.strptime(d, "%Y-%m-%d").date() >= oggi)]
    return future_races.sort_values("date").iloc[0].to_dict() if not future_races.empty else None

