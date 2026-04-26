import streamlit as st
import plotly.express as px

from src.scoring import calculate_score
from src.recommendation import generate_recommendations
from src.utils import validate_input

from src.auth import create_user_table, register_user, login_user
from src.history import create_history_table, save_daily_entry, load_user_history
from src.analytics import compute_overall_score, trend_data
from src.chatbot import chatbot_response
from src.predictor import predict_future_score
from src.goals import create_goal_table, set_goal, get_goal

st.set_page_config(page_title="AI Productivity Tracker", layout="wide")

# -------------------------------
# INIT DB
# -------------------------------
create_user_table()
create_history_table()
create_goal_table()

# -------------------------------
# SESSION
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# LOGIN
# -------------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login / Signup")

    choice = st.selectbox("Choose", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if not username or not password:
            st.warning("Enter all fields")

        else:
            if choice == "Signup":
                if register_user(username, password):
                    st.success("Account created!")
                else:
                    st.error("User exists")

            else:
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid login")

    st.stop()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title(f"👤 {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# 🎯 Goal
st.sidebar.subheader("🎯 Goal")
goal = st.sidebar.slider("Target Score", 1.0, 10.0, 7.0)

if st.sidebar.button("Set Goal"):
    set_goal(st.session_state.username, goal)
    st.sidebar.success("Saved!")

current_goal = get_goal(st.session_state.username)
if current_goal:
    st.sidebar.info(f"Goal: {current_goal}")

page = st.sidebar.radio("Navigate", ["Home", "Daily Entry", "Progress"])

# -------------------------------
# HOME
# -------------------------------
if page == "Home":
    st.title("🚀 AI Productivity Tracker")
    st.write("Track, analyze and improve your daily life.")

# -------------------------------
# DAILY ENTRY
# -------------------------------
# -------------------------------
# DAILY ENTRY (FIXED)
# -------------------------------
elif page == "Daily Entry":
    st.title("📅 Enter Data")

    sleep = st.slider("Sleep", 0.0, 10.0, 6.0)
    study = st.slider("Study", 0.0, 10.0, 4.0)
    screen = st.slider("Screen", 0.0, 10.0, 5.0)
    exercise = st.slider("Exercise", 0.0, 5.0, 1.0)
    diet = st.slider("Diet", 1, 5, 3)
    stress = st.slider("Stress", 1, 10, 5)

    data = [sleep, study, screen, exercise, diet, stress]

    # ✅ SESSION STATE INIT
    if "score" not in st.session_state:
        st.session_state.score = None
        st.session_state.suggestions = []

    # ✅ BUTTON CLICK
    if st.button("Analyze"):
        try:
            validate_input(data)

            st.session_state.score = calculate_score(data)
            st.session_state.suggestions = generate_recommendations(data)

            save_daily_entry(
                st.session_state.username,
                data,
                st.session_state.score
            )

        except Exception as e:
            st.error(f"Error: {e}")

    # ✅ ALWAYS DISPLAY RESULT
    if st.session_state.score is not None:
        st.success(f"🎯 Score: {st.session_state.score}/10")

        st.subheader("💡 Suggestions")
        for s in st.session_state.suggestions:
            st.warning(s)

        # 🤖 AI Chat
        st.subheader("🤖 AI Assistant")
        q = st.text_input("Ask AI about your performance")

        if q:
            st.info(chatbot_response(q, st.session_state.score))

# -------------------------------
# PROGRESS
# -------------------------------
elif page == "Progress":
    st.title("📈 Progress")

    history = load_user_history(st.session_state.username)

    if history:
        df = trend_data(history)

        overall = compute_overall_score(history)
        st.metric("Overall Score", overall)

        # Prediction
        pred = predict_future_score(history)
        if pred:
            st.metric("Predicted Tomorrow", pred)

        # Goal
        if current_goal:
            if overall >= current_goal:
                st.success("Goal Achieved!")
            else:
                st.warning("Keep pushing!")

        fig = px.line(df, x="date", y="score")
        st.plotly_chart(fig)

        st.dataframe(df)

    else:
        st.info("No data yet")