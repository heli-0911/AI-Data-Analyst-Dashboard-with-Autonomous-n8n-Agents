import streamlit as st
import requests

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)

# =========================
# 🎨 ELITE UI CSS
# =========================
st.markdown("""
<style>

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* TITLE */
.title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
}

/* KPI */
.kpi {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    transition: 0.3s;
}

.kpi:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(56,189,248,0.4);
}

/* CHAT CONTAINER (FIX ALIGNMENT) */
.chat-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* COMMON CHAT */
.chat-user, .chat-bot {
    width: fit-content;
    max-width: 65%;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* USER */
.chat-user {
    align-self: flex-end;
    background: #1e293b;
    text-align: right;
}

/* BOT */
.chat-bot {
    align-self: flex-start;
    background: rgba(14, 165, 233, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(14,165,233,0.3);
    color: #38bdf8;
    animation: fadeIn 0.4s ease-in-out;
}

/* INPUT */
.stTextInput > div > div > input {
    height: 55px;
    font-size: 16px;
    background: #020617;
    color: white;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding-left: 15px;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    color: white;
    border-radius: 14px;
    height: 55px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* CARD */
.card {
    background: rgba(255,255,255,0.03);
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 15px;
}

/* DIVIDER */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #38bdf8, transparent);
}

/* ANIMATION */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* FIX GAP */
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="title">🤖 AI Data Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze your dataset with AI insights</div>', unsafe_allow_html=True)

# =========================
# KPI CARDS
# =========================
col1, col2, col3 = st.columns(3)

col1.markdown('<div class="kpi"><h3>📉 26.5%</h3><p>Churn Rate</p></div>', unsafe_allow_html=True)
col2.markdown('<div class="kpi"><h3>👥 7043</h3><p>Total Customers</p></div>', unsafe_allow_html=True)
col3.markdown('<div class="kpi"><h3>💰 ₹64.76</h3><p>Avg Monthly</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## 📌 Quick Guide")
st.sidebar.markdown("""
- What is churn rate  
- Show top rows  
- Show chart  
- Average monthly charges  
- Why churn is high  
""")

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# EMPTY STATE
# =========================
if not st.session_state.history:
    st.markdown("""
    <div style="text-align:center; color:#94a3b8; margin-top:40px;">
        💬 Ask something like <br><br>
        <b>"What is churn rate?"</b>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CHAT DISPLAY (FIXED ALIGNMENT)
# =========================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, content in st.session_state.history:

    if role == "user":
        st.markdown(f'<div class="chat-user">👤 {content}</div>', unsafe_allow_html=True)

    else:
        if content["type"] == "text":
            st.markdown(f'<div class="chat-bot">🤖 {content["explanation"]}</div>', unsafe_allow_html=True)

        elif content["type"] == "table":
            st.markdown('<div class="card">📋 Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(content["result"], use_container_width=True)

        elif content["type"] == "chart":
            st.markdown('<div class="card">📈 Chart</div>', unsafe_allow_html=True)
            st.image("https://preauditory-marge-subpyriform.ngrok-free.dev/chart", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INPUT AREA
# =========================
col1, col2 = st.columns([5,1])

with col1:
    query = st.text_input("Ask something...", label_visibility="collapsed")

with col2:
    send = st.button("🚀")

if send and query:
    st.session_state.history.append(("user", query))

    try:
        res = requests.post("https://preauditory-marge-subpyriform.ngrok-free.dev/analyze", json={"query": query})
        data = res.json()

        st.session_state.history.append(("bot", data))
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("🚀 Built with Flask + Streamlit")