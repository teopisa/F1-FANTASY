import pandas as pd
# ---------------------- DATA EXTRACTION ---------------------- #
def extract_f1_data(season_2025):
    """Extracts driver & constructor information from the 2025 season."""
    drivers_list = []
    constructors_list = []

    for entrant in season_2025.get('entrants', []):
        entrant_name = entrant.get('entrantId', '').replace('-', ' ').title()

        for constructor in entrant.get('constructors', []):
            constructor_name = constructor.get('constructorId', '').replace('-', ' ').title()
            constructors_list.append({"Constructor": constructor_name, "Entrant": entrant_name})

            for driver in constructor.get('drivers', []):
                driver_name = driver.get('driverId', '').replace('-', ' ').title()
                drivers_list.append({"Driver": driver_name, "Constructor": constructor_name})

    return pd.DataFrame(drivers_list), pd.DataFrame(constructors_list)