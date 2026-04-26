from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import joblib

from src.config import TEST_SIZE, RANDOM_STATE
from src.preprocessing import preprocess_data
from src.data_loader import load_data

MODEL_PATH = "model.pkl"

def train_model():
    df = load_data()
    X, y = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)

    # Save model
    joblib.dump(model, MODEL_PATH)

    return model, score