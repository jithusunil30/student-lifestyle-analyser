import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future_score(history):
    if len(history) < 3:
        return None

    scores = [h["score"] for h in history]

    X = np.array(range(len(scores))).reshape(-1, 1)
    y = np.array(scores)

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[len(scores)]])[0]
    return round(float(pred), 2)