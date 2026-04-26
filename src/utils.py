def validate_input(data):
    if any(x < 0 for x in data):
        raise ValueError("Inputs must be non-negative")

    return True