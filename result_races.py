def estrai_risultati_gara(data, grand_prix_id, anno):
    """
    Estrae i risultati della gara per un dato Grand Prix e anno specifici.

    Args:
        data (dict): Il dizionario JSON completo.
        grand_prix_id (str): L'ID del GP (es. 'monaco').
        anno (int): L'anno della stagione (es. 2025).

    Returns:
        dict or None: Dizionario con i dati della gara per l'anno richiesto, oppure None se non trovato.
    """
    for race in data.get("races", []):
        # Controlla che sia la gara giusta e l'anno giusto
        if race.get("grandPrixId") == grand_prix_id and race.get("year") == anno:
            return race
    return None
