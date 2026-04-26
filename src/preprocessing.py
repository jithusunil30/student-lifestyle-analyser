from src.config import FEATURE_COLUMNS, TARGET_COLUMN

def preprocess_data(df):
    # Drop missing values
    df = df.dropna()

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y