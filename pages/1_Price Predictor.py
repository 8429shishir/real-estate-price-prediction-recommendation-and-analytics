import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

st.set_page_config(
    page_title="Price Predictor — Real Estate AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060b14 !important;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

[data-testid="stSidebar"] {
    background: #0d1525 !important;
    border-right: 1px solid #1e2d45 !important;
}

/* ── Top Nav Bar ── */
.topnav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid #1e2d45;
}
.topnav-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #38bdf8;
    display: flex;
    align-items: center;
    gap: 8px;
}
.topnav-crumb {
    font-size: 13px;
    color: #475569;
}
.topnav-crumb span { color: #94a3b8; }


/* ── Page Header ── */
.page-header {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 36px;
    padding: 32px 36px;
    background: linear-gradient(135deg, #0d1525, #0f1e35);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(56,189,248,0.10) 0%, transparent 70%);
    pointer-events: none;
}
.header-icon {
    font-size: 52px;
    line-height: 1;
    flex-shrink: 0;
}
.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 6px;
}
.header-sub {
    font-size: 15px;
    color: #64748b;
    line-height: 1.6;
    max-width: 560px;
}

/* ── Form Section ── */
.form-section-label {
    font-size: 11px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d45;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] > div > div {
    background: #0d1525 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: #3b82f6 !important;
}

/* Label style */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
}

/* ── Predict button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    padding: 14px 28px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #2563eb, #38bdf8) !important;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(37,99,235,0.35) !important;
    letter-spacing: 0.3px;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(56,189,248,0.45) !important;
}

/* ── Result Card ── */
.result-outer {
    margin-top: 28px;
    animation: fadeUp 0.5s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-card {
    background: linear-gradient(135deg, #0d1f38 0%, #0f2444 100%);
    border: 1px solid #1e4a7a;
    border-radius: 20px;
    padding: 36px 40px;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(56,189,248,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.result-tag {
    font-size: 11px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.result-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    color: #64748b;
    margin-bottom: 18px;
}
.price-range {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
.price-low, .price-high {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    font-size: 42px;
    line-height: 1;
}
.price-low { color: #34d399; }
.price-high { color: #f87171; }
.price-dash { font-size: 28px; color: #475569; font-weight: 300; }
.price-unit { font-size: 14px; color: #64748b; font-weight: 500; margin-top: 4px; }
.price-mid-label {
    font-size: 13px;
    color: #64748b;
    margin-left: 4px;
    margin-top: 2px;
}
.result-divider {
    height: 1px;
    background: #1e3a5f;
    margin: 20px 0;
}
.result-meta {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
}
.meta-item {
    display: flex;
    flex-direction: column;
    gap: 3px;
}
.meta-key {
    font-size: 11px;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.meta-val {
    font-size: 15px;
    font-weight: 600;
    color: #e2e8f0;
}

/* ── Summary table ── */
.summary-wrap {
    margin-top: 24px;
    background: #0a1220;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 20px;
}
.summary-title {
    font-size: 13px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden;
}

/* Info / tip boxes */
div[data-testid="stInfo"] {
    background: rgba(56,189,248,0.08) !important;
    border-left: 3px solid #38bdf8 !important;
    border-radius: 10px !important;
    color: #7dd3fc !important;
}

/* ── Note box ── */
.note-box {
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 13px;
    color: #fbbf24;
    margin-top: 18px;
    line-height: 1.6;
}

/* Header transparent — stays in DOM so sidebar toggle works */
[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
    box-shadow: none !important;
}
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stDeployButton { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }

/* ★ Sidebar collapsed toggle — make it VERY visible */
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #1e3a5f !important;
    border-right: 3px solid #38bdf8 !important;
    z-index: 9999 !important;
}
[data-testid="stSidebarCollapsedControl"] button {
    color: #38bdf8 !important;
    font-size: 1.4rem !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ── Top Navigation Bar ──────────────────────────────────────────────────────
col_back, col_mid, col_right = st.columns([1, 4, 1])
with col_back:
    st.page_link("Home.py", label="← Home", icon="🏠")
with col_right:
    st.page_link("pages/2_Analysis App.py", label="Analysis App", icon="📊")

st.markdown("""
<div class="topnav">
    <div class="topnav-brand">🏠 Real Estate AI</div>
    <div class="topnav-crumb">Home &nbsp;/&nbsp; <span>Price Predictor</span></div>
</div>
""", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="header-icon">🏠</div>
    <div>
        <div class="header-title">Property Price Predictor</div>
        <div class="header-sub">
            Enter the property specifications below to get an AI-powered price estimate 
            with a ±0.25 Cr confidence range. The model is trained on 13,000+ Gurgaon 
            property listings using a tuned ML pipeline.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource(show_spinner="Loading AI model...")
def load_model():
    df_path = os.path.join(BASE_DIR, 'model', 'df.pkl')
    pipeline_path = os.path.join(BASE_DIR, 'model', 'pipeline.pkl')
    with open(df_path, 'rb') as f:
        df = pickle.load(f)
    with open(pipeline_path, 'rb') as f:
        pipeline = pickle.load(f)
    return df, pipeline

try:
    df, pipeline = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"❌ Could not load model: {e}")
    model_loaded = False
    st.stop()

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("prediction_form"):

    # — Section 1: Property Basics —
    st.markdown('<div class="form-section-label">🏡 &nbsp;Property Details</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox("Property Type", ["Flat", "House"],
                                     help="Apartment/Flat or Independent House")
    with col2:
        sector = st.selectbox("Sector / Location", sorted(df['sector'].unique().tolist()),
                              help="Residential sector in Gurgaon")

    st.markdown("<br>", unsafe_allow_html=True)

    # — Section 2: Room Configuration —
    st.markdown('<div class="form-section-label">🛏️ &nbsp;Room Configuration</div>', unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3)
    with col3:
        bedrooms = float(st.selectbox("Bedrooms", sorted(df['bedRoom'].unique().tolist())))
    with col4:
        bathroom = float(st.selectbox("Bathrooms", sorted(df['bathroom'].unique().tolist())))
    with col5:
        balcony = st.selectbox("Balconies", sorted(df['balcony'].unique().tolist()))

    col6, col7 = st.columns(2)
    with col6:
        servant_room = float(st.selectbox("Servant Room", sorted(df['servant room'].unique().tolist()),
                                          help="0 = None, 1 = Available"))
    with col7:
        store_room = float(st.selectbox("Store Room", sorted(df['store room'].unique().tolist()),
                                        help="0 = None, 1 = Available"))

    st.markdown("<br>", unsafe_allow_html=True)

    # — Section 3: Property Specifications —
    st.markdown('<div class="form-section-label">📐 &nbsp;Property Specifications</div>', unsafe_allow_html=True)
    col8, col9 = st.columns(2)
    with col8:
        built_up_area = float(st.selectbox("Built-up Area (sq. ft.)",
                                           sorted(df['built_up_area'].unique().tolist())))
    with col9:
        age_possession = st.selectbox("Age / Possession Status",
                                      sorted(df['agePossession'].unique().tolist()))

    col10, col11, col12 = st.columns(3)
    with col10:
        furnishing_type = st.selectbox("Furnishing Type",
                                       sorted(df['furnishing_type'].unique().tolist()))
    with col11:
        luxury_category = st.selectbox("Luxury Category",
                                       sorted(df['luxury_category'].unique().tolist()))
    with col12:
        floor_category = st.selectbox("Floor Category",
                                      sorted(df['floor_category'].unique().tolist()))

    st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🔮 &nbsp; Predict Price")

# ── Prediction ────────────────────────────────────────────────────────────────
if submitted:
    input_data = [[
        property_type, sector, bedrooms, bathroom, balcony,
        age_possession, built_up_area, servant_room, store_room,
        furnishing_type, luxury_category, floor_category
    ]]
    columns = [
        'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
        'agePossession', 'built_up_area', 'servant room', 'store room',
        'furnishing_type', 'luxury_category', 'floor_category'
    ]
    input_df = pd.DataFrame(input_data, columns=columns)

    with st.spinner("Running AI prediction..."):
        raw_price = float(np.expm1(pipeline.predict(input_df))[0])
        base_price = round(raw_price, 2)
        low = round(raw_price - 0.25, 2)
        high = round(raw_price + 0.25, 2)
        mid = base_price

    # ── Result Card ──
    st.markdown(f"""
    <div class="result-outer">
        <div class="result-card">
            <div class="result-tag">✅ Prediction Complete</div>
            <div class="result-label">Estimated property value in Gurgaon</div>
            <div class="price-range">
                <div>
                    <div class="price-low">₹ {low} Cr</div>
                    <div class="price-unit">Lower Estimate</div>
                </div>
                <div class="price-dash">—</div>
                <div>
                    <div class="price-high">₹ {high} Cr</div>
                    <div class="price-unit">Upper Estimate</div>
                </div>
            </div>
            <div class="result-divider"></div>
            <div class="result-meta">
                <div class="meta-item">
                    <div class="meta-key">Base Prediction</div>
                    <div class="meta-val">₹ {mid} Cr</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Confidence Band</div>
                    <div class="meta-val">± 0.25 Cr</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Property Type</div>
                    <div class="meta-val">{property_type}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Sector</div>
                    <div class="meta-val">{sector}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Built-up Area</div>
                    <div class="meta-val">{int(built_up_area):,} sq.ft.</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Bedrooms</div>
                    <div class="meta-val">{int(bedrooms)} BHK</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Summary ──
    with st.expander("📋 View Full Input Summary", expanded=False):
        st.markdown('<div class="summary-title">Submitted Property Details</div>', unsafe_allow_html=True)
        display_df = input_df.copy()
        display_df.columns = [
            'Property Type', 'Sector', 'Bedrooms', 'Bathrooms', 'Balconies',
            'Age/Possession', 'Built-up Area (sqft)', 'Servant Room', 'Store Room',
            'Furnishing Type', 'Luxury Category', 'Floor Category'
        ]
        st.dataframe(display_df, use_container_width=True)

    # ── Disclaimer ──
    st.markdown("""
    <div class="note-box">
        ⚠️ <strong>Note:</strong> This prediction is based on historical Gurgaon property listings 
        and is intended for reference purposes only. Actual market prices may vary based on 
        current market conditions, negotiation, and legal factors. Always consult a registered 
        real estate agent for accurate valuation.
    </div>
    """, unsafe_allow_html=True)
