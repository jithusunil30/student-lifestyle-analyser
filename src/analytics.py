import pandas as pd

def compute_overall_score(history):
    if not history:
        return 0

    df = pd.DataFrame(history, columns=[
        "username","sleep","study","screen","exercise",
        "diet","stress","score","date"
    ])

    return round(df["score"].mean(), 2)

def trend_data(history):
    df = pd.DataFrame(history, columns=[
        "username","sleep","study","screen","exercise",
        "diet","stress","score","date"
    ])
    return df