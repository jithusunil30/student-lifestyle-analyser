def calculate_score(data):
    sleep, study, screen, exercise, diet, stress = data

    score = (
        0.3 * sleep +
        0.5 * study -
        0.3 * screen +
        0.4 * exercise +
        0.3 * diet -
        0.4 * stress
    )

    # normalize to 0–10 range
    score = max(0, min(10, score))

    return round(score, 2)