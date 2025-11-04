def compute_weighted_average(days):
    """
    Calcola la media ponderata degli ultimi 7 giorni
    usando average e sample_size.
    Esclude i giorni con sample_size == 0 o average == None.
    """
    if not days:
        return None

    # prendiamo solo gli ultimi 7 giorni (o meno se non ci sono)
    last7 = days[-7:] if len(days) >= 7 else days

    total_weighted = 0
    total_samples = 0

    for d in last7:
        avg = d.get("average")
        samples = d.get("sample_size", 0)
        if samples > 0 and avg is not None:
            total_weighted += avg * samples
            total_samples += samples

    if total_samples == 0:
        return None

    return total_weighted / total_samples
