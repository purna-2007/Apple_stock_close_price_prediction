import streamlit as st
import numpy as np
import joblib
import time
import base64

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Apple Stock Price Predictor",
    page_icon="🍎",
    layout="centered"
)

# ==============================
# BACKGROUND IMAGE
# ==============================
def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

bg_base64 = get_base64("apple_bg.jpg")

if bg_base64:
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)),
        url('https://w0.peakpx.com/wallpaper/694/82/HD-wallpaper-apple-red-logo-red-brickwall-apple-logo-red-neon-apple-brands-apple-neon-logo-apple-thumbnail.jpg');
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# GLOBAL STYLES (REMOVES WHITE BAR)
# ==============================
st.markdown("""
<style>
/* HIDE TOP BAR AND HEADER ELEMENTS */
header {visibility: hidden;}
.stAppDeployButton {display:none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* REMOVE TOP PADDING GAP */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
}

/* TEXT AND INPUT COLORS */
html, body, [class*="css"] {
    color: #ffffff !important;
}
label {
    color: #ffffff !important;
}
input {
    color: #000000 !important;
    background-color: rgba(255,255,255,0.95) !important;
    border-radius: 10px !important;
}
h1, h2, h3 {
    color: #ffffff !important;
    text-shadow: 3px 3px 8px rgba(0,0,0,1);
}
p, span, div {
    color: #ffffff !important;
}

/* ❄️ SNOW ANIMATION */
@keyframes snowfall {
    0% { transform: translateY(-10vh); opacity: 0; }
    10% { opacity: 1; }
    100% { transform: translateY(110vh); opacity: 0; }
}

.snow {
    position: fixed;
    top: -10px;
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: snowfall linear infinite;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD MODEL & SCALER
# ==============================
@st.cache_resource
def load_assets():
    # Make sure these files exist in your directory
    model = joblib.load("random_forest_apple_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

try:
    model, scaler = load_assets()
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# ==============================
# INR FORMAT
# ==============================
def format_inr(usd):
    return f"₹ {usd * 83:,.2f}"

# ==============================
# HEADER
# ==============================
st.markdown("""
<div style="text-align:center; position:relative; z-index:2;">
<img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
 width="60" style="filter:invert(1); margin-bottom:15px;">
<h1>Apple Stock Close Price Prediction</h1>
</div>
<hr>
""", unsafe_allow_html=True)

# ==============================
# INPUT SECTION
# ==============================
st.subheader("📊 Enter Stock Details (₹ INR)")

conversion = 83
c1, c2 = st.columns(2)

with c1:
    open_inr = st.number_input("Open Price (₹)", value=14981.5)
    high_inr = st.number_input("High Price (₹)", value=15130.9)

with c2:
    low_inr = st.number_input("Low Price (₹)", value=14923.4)
    volume = st.number_input("Volume", value=45000000)

# ==============================
# PREDICTION
# ==============================
if st.button("🚀 Predict Closing Price", use_container_width=True):

    with st.spinner("Analyzing market patterns..."):
        time.sleep(1.2)

    open_usd = open_inr / conversion
    high_usd = high_inr / conversion
    low_usd = low_inr / conversion

    X = np.array([[open_usd, high_usd, low_usd, volume]])
    X_scaled = scaler.transform(X)

    pred_usd = model.predict(X_scaled)[0]
    pred_inr = format_inr(pred_usd)

    if pred_usd >= open_usd:
        status = "📈 PROFIT"
        res_bg = "rgba(20, 90, 50, 0.9)"
        border = "#00e676"
        glow = "rgba(0,230,118,0.6)"
    else:
        status = "📉 LOSS"
        res_bg = "rgba(90, 20, 20, 0.9)"
        border = "#ff5252"
        glow = "rgba(255,82,82,0.6)"

    # RESULT CARD
    st.markdown(f"""
    <div style="
        background:{res_bg};
        padding:40px;
        border-radius:25px;
        text-align:center;
        border:4px solid {border};
        box-shadow:0 0 50px {glow};
        margin-top:25px;
        position:relative;
        z-index:2;
    ">
        <h2>{status}</h2>
        <h1 style="font-size:72px;">{pred_inr}</h1>
        <p>Predicted Close Price for Apple Inc. (AAPL)</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ Successfully Completed Prediction Close Price")

    # ==============================
    # ❄️ SNOW APPEARS AFTER SUCCESS
    # ==============================
    snow_html = ""
    for _ in range(80):
        snow_html += f"""
        <div class="snow"
             style="
             left:{np.random.randint(0,100)}%;
             animation-duration:{np.random.uniform(6,14)}s;
             animation-delay:{np.random.uniform(0,6)}s;
             width:{np.random.randint(3,6)}px;
             height:{np.random.randint(3,6)}px;
             opacity:{np.random.uniform(0.4,0.9)};
             ">
        </div>
        """
    st.markdown(snow_html, unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<hr>
<p style="text-align:center; font-size:11px; position:relative; z-index:2;">
Developed by Purna ✨
</p>
""", unsafe_allow_html=True)