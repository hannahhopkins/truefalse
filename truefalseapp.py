import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="True/False Quiz", layout="wide")

# ---- LOAD CSV ----
@st.cache_data
def load_data():
    df = pd.read_csv("truefalse.csv")
    df.columns = [c.lower().strip() for c in df.columns]
    return df

df = load_data()

# ---- INITIALIZE SESSION STATE ----
if "order" not in st.session_state:
    st.session_state.order = list(range(len(df)))
    random.shuffle(st.session_state.order)

if "index" not in st.session_state:
    st.session_state.index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_correct" not in st.session_state:
    st.session_state.last_correct = False

# ---- RESET FUNCTION ----
def restart_quiz():
    st.session_state.order = list(range(len(df)))
    random.shuffle(st.session_state.order)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_correct = False


# ---- UI HEADER ----
st.title("True or False?")

# ---- FLOATING SCORE BADGE ----
# ---- FLOATING SCORE BADGE ----
score_html = """
<div style="position:fixed; bottom:20px; right:20px; 
            background:#f0f0f0; padding:12px 18px; 
            border-radius:10px; font-size:18px; 
            box-shadow: 0 0 5px rgba(0,0,0,0.3);">
    Score: <strong>{}</strong>
</div>
""".format(st.session_state.score)

st.markdown(score_html, unsafe_allow_html=True)

