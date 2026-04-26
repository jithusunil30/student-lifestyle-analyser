def generate_recommendations(data):
    sleep, study, screen, exercise, diet, stress = data

    suggestions = []

    if sleep < 6:
        suggestions.append("Increase sleep to at least 7 hours")

    if screen > 5:
        suggestions.append("Reduce screen time to improve focus")

    if exercise < 1:
        suggestions.append("Add at least 30 mins of exercise daily")

    if diet < 3:
        suggestions.append("Improve diet quality (more fruits & protein)")

    if stress > 7:
        suggestions.append("Practice stress management (meditation, breaks)")

    if study < 3:
        suggestions.append("Increase focused study hours")

    return suggestions