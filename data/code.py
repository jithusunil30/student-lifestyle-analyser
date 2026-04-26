import pandas as pd
import numpy as np

data = []

for _ in range(200):
    sleep = np.random.uniform(4, 9)
    study = np.random.uniform(1, 8)
    screen = np.random.uniform(2, 9)
    exercise = np.random.uniform(0, 2)
    diet = np.random.randint(1, 6)
    stress = np.random.randint(1, 10)

    # realistic GPA formula
    gpa = (
        0.4 * sleep +
        0.6 * study -
        0.3 * screen +
        0.5 * exercise +
        0.3 * diet -
        0.4 * stress +
        np.random.normal(0, 0.5)
    )

    data.append([sleep, study, screen, exercise, diet, stress, gpa])

df = pd.DataFrame(data, columns=[
    "sleep_hours","study_hours","screen_time",
    "exercise_hours","diet_quality","stress_level","gpa"
])

df.to_csv("data/student_lifestyle_dataset.csv", index=False)