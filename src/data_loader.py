import pandas as pd
from src.config import DATA_PATH

def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {e}")