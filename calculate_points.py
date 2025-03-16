def calculate_points(predictions):
    """Calculates total points based on prediction accuracy."""
    total_points = 0

    for round_num, pred in predictions.items():
        # Assume actual results (for now, placeholders)
        actual_pole = "Max Verstappen"
        actual_quali_top3 = ["Max Verstappen", "Charles Leclerc", "Lando Norris"]
        actual_race_top5 = ["Max Verstappen", "Lewis Hamilton", "Carlos Sainz", "George Russell", "Sergio Perez"]
        actual_dnf = "Kevin Magnussen"

        # Qualifying Points
        if pred["pole"] == actual_pole:
            total_points += 1

        for i, driver in enumerate(pred["quali_top3"]):
            if driver in actual_quali_top3:
                total_points += 1  # Driver in Top 3
                if driver == actual_quali_top3[i]:
                    total_points += 1  # Driver in Correct Position

        if pred["quali_top3"] == actual_quali_top3:
            total_points += 2  # Full Top 3 Correct

        # Race Points
        for i, driver in enumerate(pred["race_top5"]):
            if driver in actual_race_top5:
                total_points += 1  # Driver in Top 5
                if driver in actual_race_top5[:3]:  
                    total_points += 1  # Driver in Top 3
                if driver == actual_race_top5[i]:
                    total_points += 1  # Driver in Correct Position

        if pred["race_top5"][0] == actual_race_top5[0]:
            total_points += 1  # Winner Correct

        if pred["race_top5"][:3] == actual_race_top5[:3]:
            total_points += 2  # Full Top 3 Correct

        if pred["race_top5"] == actual_race_top5:
            total_points += 2  # Full Top 5 Correct

        # DNF Points
        if pred["dnf"] == actual_dnf:
            total_points += 1
        elif pred["dnf"] != "None":
            total_points -= 1  # Wrong DNF Prediction

    return total_points