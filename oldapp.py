import streamlit as st
import pandas as pd
import plotly.express as px
from src.history import create_history_table, save_daily_entry, load_user_history
from src.analytics import compute_overall_score, trend_data
from src.model import train_model
from src.predictor import Predictor
from src.recommendation import generate_recommendations
from src.utils import validate_input
from src.data_loader import load_data
from src.auth import create_user_table, register_user, login_user
from src.history import create_history_table, save_history, load_user_history
from src.report import generate_pdf
from src.chatbot import chatbot_response
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #38bdf8;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 15px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align: center;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

/* Inputs */
.stSlider, .stTextInput {
    background-color: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 5px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* Cards */
.custom-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(56,189,248,0.2);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)
# -------------------------------
# INIT DB
# -------------------------------
create_user_table()
create_history_table()

# -------------------------------
# SESSION STATE
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------
# LOGIN SYSTEM
# -------------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login / Signup")

    choice = st.selectbox("Choose", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if register_user(username, password):
                st.success("Account created!")
            else:
                st.error("User already exists")

    else:
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Student Lifestyle Analyzer", layout="wide")

# -------------------------------
# LOAD MODEL
# -------------------------------
@st.cache_resource
def load_model():
    model, score = train_model()
    return model, score

model, score = load_model()
predictor = Predictor()

# -------------------------------
# LOAD DATA
# -------------------------------
df = load_data()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title(f"👤 {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📊 Analytics", "🤖 Prediction", "📜 History"]
)

# -------------------------------
# HOME
# -------------------------------
if page == "🏠 Home":
    st.title("🚀 Lifestyle Intelligence Dashboard")

    st.markdown("""
    <div class="custom-card">
    <h3>🧠 AI-Powered Academic Optimization</h3>
    <p>
    This system uses machine learning to decode how your lifestyle impacts your academic performance.
    Transform your daily habits into measurable success.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📊 Data Points", len(df))
    col2.metric("📈 Accuracy", f"{round(score,2)}")
    col3.metric("🧬 Features", df.shape[1]-1)
    col4.metric("⚡ Model", "AI Regression")

    st.markdown("""
    <div class="custom-card">
    <h4>⚡ What You Can Do</h4>
    <ul>
        <li>Predict your GPA instantly</li>
        <li>Analyze lifestyle impact</li>
        <li>Track performance history</li>
        <li>Get AI-based recommendations</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.success("👉 Navigate to Prediction to start 🚀")

    # -------------------------------
    # SYSTEM OVERVIEW CARDS
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)

        sleep = st.slider("😴 Sleep Hours", 0.0, 10.0, 6.0)
        study = st.slider("📚 Study Hours", 0.0, 10.0, 4.0)
        screen = st.slider("📱 Screen Time", 0.0, 10.0, 5.0)
        exercise = st.slider("🏋️ Exercise", 0.0, 5.0, 1.0)
        diet = st.slider("🥗 Diet Quality", 1, 5, 3)
        stress = st.slider("😵 Stress Level", 1, 10, 5)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)

        st.success(f"🎯 Predicted GPA: {prediction}")

        fig = px.pie(
             names=["Achieved", "Remaining"],
             values=[prediction, 10 - prediction]
        )
        st.plotly_chart(fig)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------
    # CALL TO ACTION
    # -------------------------------
    st.success("👉 Go to 'Prediction' tab to analyze your performance 🚀")
# -------------------------------
# ANALYTICS
# -------------------------------
elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")

    fig = px.imshow(df.corr(), text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x="sleep_hours", y="gpa",
                      color="stress_level",
                      size="study_hours")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# PREDICTION
# -------------------------------
elif page == "🤖 Prediction":
    st.title("🤖 GPA Prediction")

    col1, col2 = st.columns(2)

    with col1:
        sleep = st.slider("Sleep", 0.0, 10.0, 6.0)
        study = st.slider("Study", 0.0, 10.0, 4.0)
        screen = st.slider("Screen", 0.0, 10.0, 5.0)
        exercise = st.slider("Exercise", 0.0, 5.0, 1.0)
        diet = st.slider("Diet (1-5)", 1, 5, 3)
        stress = st.slider("Stress (1-10)", 1, 10, 5)

    input_data = [sleep, study, screen, exercise, diet, stress]

    if st.button("Predict"):
        try:
            validate_input(input_data)

            prediction = predictor.predict(input_data)
            suggestions = generate_recommendations(input_data)

            # SAVE HISTORY ✅ (FIXED)
            save_history(st.session_state.username, input_data, prediction)

            with col2:
                st.success(f"Predicted GPA: {prediction}")

                fig = px.pie(
                    names=["Achieved", "Remaining"],
                    values=[prediction, 10 - prediction]
                )
                st.plotly_chart(fig)

                st.subheader("Recommendations")
                for s in suggestions:
                    st.warning(s)

                # PDF DOWNLOAD
                if st.button("Generate PDF Report"):
                    file = generate_pdf(st.session_state.username, prediction, suggestions)
                    with open(file, "rb") as f:
                        st.download_button("Download", f, file_name=file)

                # CHATBOT
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)

                st.subheader("🤖 AI Assistant")
                user_q = st.text_input("Ask your AI coach...")

                if user_q:
                    response = chatbot_response(user_q, prediction)
                    st.info(response)

                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(e)

# -------------------------------
# HISTORY
# -------------------------------
elif page == "📜 History":
    st.title("📜 Your History")

    history = load_user_history(st.session_state.username)

    if history:
        df_hist = pd.DataFrame(history, columns=[
            "username","sleep","study","screen","exercise",
            "diet","stress","prediction","time"
        ])
        st.dataframe(df_hist)
    else:
        st.info("No history found")