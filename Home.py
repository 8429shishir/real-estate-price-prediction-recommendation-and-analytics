import streamlit as st

st.set_page_config(
    page_title="Real Estate AI — Shishir Singh",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060b14 !important;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

.block-container { padding: 2rem 3rem !important; max-width: 1200px !important; }

[data-testid="stSidebar"] {
    background: #0d1525 !important;
    border-right: 1px solid #1e2d45 !important;
}

/* ── Hero ── */
.hero-wrapper {
    background: linear-gradient(135deg, #0f1f35 0%, #0d1525 50%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 24px;
    padding: 60px 50px;
    position: relative;
    overflow: hidden;
    margin-bottom: 40px;
}
.hero-wrapper::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-wrapper::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(139,92,246,0.10) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.35);
    color: #38bdf8;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 999px;
    margin-bottom: 22px;
}
.hero-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(42px, 5vw, 64px);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 20px;
    font-weight: 500;
    color: #64748b;
    margin-bottom: 20px;
}
.hero-title span { color: #7dd3fc; font-weight: 600; }
.hero-desc {
    font-size: 16px;
    color: #94a3b8;
    line-height: 1.75;
    max-width: 620px;
    margin-bottom: 32px;
}
.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 36px;
}
.chip {
    background: rgba(255,255,255,0.05);
    border: 1px solid #1e3a5f;
    color: #cbd5e1;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
}
.hero-links {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}
.btn-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #3b82f6, #38bdf8);
    color: #ffffff !important;
    font-size: 14px;
    font-weight: 600;
    padding: 11px 24px;
    border-radius: 10px;
    text-decoration: none !important;
    box-shadow: 0 4px 20px rgba(56,189,248,0.3);
}
.btn-link-sec {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.06);
    border: 1px solid #2d4a6b;
    color: #94a3b8 !important;
    font-size: 14px;
    font-weight: 600;
    padding: 11px 24px;
    border-radius: 10px;
    text-decoration: none !important;
}

/* ── Stats ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 40px;
}
.stat-card {
    background: #0d1525;
    border: 1px solid #1e2d45;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.25s ease;
}
.stat-card:hover {
    border-color: #38bdf8;
    box-shadow: 0 0 20px rgba(56,189,248,0.12);
    transform: translateY(-3px);
}
.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 12px;
    color: #64748b;
    font-weight: 500;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Section ── */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 6px;
}
.section-sub {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 20px;
}

/* ── Nav module cards ── */
.nav-module-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-bottom: 12px;
}
.nav-module-card {
    background: linear-gradient(135deg, #0d1525, #111927);
    border: 1px solid #1e2d45;
    border-radius: 20px;
    padding: 32px 28px 24px;
    position: relative;
    overflow: hidden;
}
.nav-module-icon { font-size: 36px; margin-bottom: 14px; }
.nav-module-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 8px;
}
.nav-module-desc { font-size: 14px; color: #64748b; line-height: 1.6; margin-bottom: 20px; }
.nav-module-accent {
    position: absolute;
    bottom: 0; right: 0;
    width: 120px; height: 120px;
    border-radius: 50%;
    pointer-events: none;
}

/* ── About steps ── */
.about-box {
    background: linear-gradient(135deg, #0d1525, #101a2c);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #38bdf8;
    border-radius: 16px;
    padding: 30px 28px;
    margin-bottom: 40px;
}
.about-intro {
    font-size: 15px;
    color: #94a3b8;
    line-height: 1.8;
    margin-bottom: 24px;
}
.about-intro strong { color: #e2e8f0; }
.about-steps { display: flex; flex-direction: column; gap: 16px; }
.about-step {
    display: flex;
    gap: 16px;
    align-items: flex-start;
}
.step-num {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    color: #38bdf8;
    margin-top: 2px;
}
.step-content { font-size: 14px; color: #94a3b8; line-height: 1.7; }
.step-content strong { color: #e2e8f0; }

/* ── Tech ── */
.tech-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
    margin-bottom: 40px;
}
.tech-item {
    background: #0d1525;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 16px 14px;
    text-align: center;
    transition: all 0.25s ease;
}
.tech-item:hover { border-color: #38bdf8; background: #111f38; }
.tech-icon { font-size: 24px; margin-bottom: 8px; }
.tech-name { font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── Footer ── */
.footer-wrap {
    border-top: 1px solid #1e2d45;
    padding-top: 30px;
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.footer-left { font-size: 13px; color: #475569; }
.footer-left span { color: #38bdf8; font-weight: 600; }
.footer-right { font-size: 13px; color: #475569; }

/* Streamlit page_link button styling */
div[data-testid="stPageLink"] a {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 14px 22px !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    text-decoration: none !important;
    transition: all 0.2s ease !important;
    border: 1px solid !important;
}
div[data-testid="stPageLink"]:first-child a {
    background: linear-gradient(135deg, rgba(37,99,235,0.2), rgba(56,189,248,0.15)) !important;
    border-color: #2563eb !important;
    color: #7dd3fc !important;
}
div[data-testid="stPageLink"]:first-child a:hover {
    background: linear-gradient(135deg, rgba(37,99,235,0.35), rgba(56,189,248,0.25)) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(56,189,248,0.2) !important;
}
div[data-testid="stPageLink"]:last-child a {
    background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(129,140,248,0.15)) !important;
    border-color: #7c3aed !important;
    color: #c4b5fd !important;
}
div[data-testid="stPageLink"]:last-child a:hover {
    background: linear-gradient(135deg, rgba(139,92,246,0.35), rgba(129,140,248,0.25)) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(139,92,246,0.2) !important;
}

/* Header transparent — stays in DOM so sidebar toggle works */
[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
    box-shadow: none !important;
}
# [data-testid="stToolbar"] { display: none !important; }
# [data-testid="stDecoration"] { display: none !important; }
# .stDeployButton { display: none !important; }
MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏠 Real Estate AI")
    st.markdown("---")
    st.page_link("Home.py", label="🏠 Home", icon=None)
    st.page_link("pages/1_Price Predictor.py", label="💰 Price Predictor", icon=None)
    st.page_link("pages/2_Analysis App.py", label="📊 Analysis App", icon=None)
    st.markdown("---")
    st.markdown(
        "<small style='color:#475569'>Built by **Shishir Singh**<br>IIT Bhubaneswar · 2025</small>",
        unsafe_allow_html=True
    )

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">📊 ML Portfolio Project</div>
    <div class="hero-name">Real Estate Price<br>Intelligence System</div>
    <div class="hero-title">Built by <span>Shishir Singh</span> &nbsp;·&nbsp; AI/ML Engineer</div>
    <div class="hero-desc">
        An end-to-end machine learning system for predicting residential property prices in
        <strong style="color:#7dd3fc">Gurgaon, India</strong>. From raw data scraping and
        rigorous feature engineering to a production-grade ML pipeline — built entirely from scratch.
    </div>
    <div class="hero-chips">
        <span class="chip">🎓 IIT Bhubaneswar</span>
        <span class="chip">🤖 Machine Learning</span>
        <span class="chip">📈 Data Science</span>
        <span class="chip">🏘️ Real Estate Domain</span>
        <span class="chip">🐍 Python</span>
    </div>
    <div class="hero-links">
        <a class="btn-link" href="https://github.com/8429shishir" target="_blank">⭐ GitHub</a>
        <a class="btn-link-sec" href="https://www.linkedin.com/in/shishir-singh" target="_blank">🔗 LinkedIn</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-value">13K+</div>
        <div class="stat-label">Properties Analysed</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">12</div>
        <div class="stat-label">Feature Variables</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">~90%</div>
        <div class="stat-label">Model Accuracy (R²)</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">13</div>
        <div class="stat-label">ML Notebooks</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🚀 Explore the App</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Click a module below to jump straight in.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="nav-module-card">
        <div class="nav-module-icon">🏠</div>
        <div class="nav-module-title">Price Predictor</div>
        <div class="nav-module-desc">
            Enter property specs and get an instant AI-powered price estimate
            with a confidence range — powered by a tuned ML pipeline.
        </div>
        <div class="nav-module-accent" style="background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);"></div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Price Predictor.py", label="Open Price Predictor →", icon="🏠")

with col2:
    st.markdown("""
    <div class="nav-module-card">
        <div class="nav-module-icon">📊</div>
        <div class="nav-module-title">Analysis App</div>
        <div class="nav-module-desc">
            Dive deep into the Gurgaon real estate market — interactive charts,
            sector heatmaps, feature correlations, and more.
        </div>
        <div class="nav-module-accent" style="background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);"></div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Analysis App.py", label="Open Analysis App →", icon="📊")

st.markdown("<br>", unsafe_allow_html=True)

# ── About Project ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 About This Project</div>', unsafe_allow_html=True)

st.markdown("""
<div class="about-box">
    <div class="about-intro">
        This project implements a <strong>full-stack data science pipeline</strong> for real estate
        price prediction in the Gurgaon residential market — covering every stage from data collection to deployment.
    </div>
    <div class="about-steps">
        <div class="about-step">
            <div class="step-num">1</div>
            <div class="step-content">
                <strong>Data Collection &amp; Preprocessing</strong> — Merged and cleaned over 13,000 property listings
                (flats + independent houses) across Gurgaon sectors, handling duplicates, outliers, and missing values.
            </div>
        </div>
        <div class="about-step">
            <div class="step-num">2</div>
            <div class="step-content">
                <strong>Feature Engineering</strong> — Engineered 12 key features including built-up area,
                bedroom/bathroom count, luxury category, floor tier, furnishing status, balcony count,
                age of possession, servant/store rooms, and sector encoding.
            </div>
        </div>
        <div class="about-step">
            <div class="step-num">3</div>
            <div class="step-content">
                <strong>Model Selection</strong> — Benchmarked Linear Regression, Ridge, Lasso, Decision Tree,
                Random Forest, Gradient Boosting, and XGBoost. Selected the best-performing pipeline
                using cross-validated R&sup2; scores.
            </div>
        </div>
        <div class="about-step">
            <div class="step-num">4</div>
            <div class="step-content">
                <strong>Deployment</strong> — Packaged the final model as a scikit-learn Pipeline
                (preprocessing + model) and deployed as an interactive Streamlit web application.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tech Stack ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🛠️ Tech Stack</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Technologies and libraries used to build this project end-to-end.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="tech-grid">
    <div class="tech-item"><div class="tech-icon">🐍</div><div class="tech-name">Python</div></div>
    <div class="tech-item"><div class="tech-icon">🤖</div><div class="tech-name">Scikit-learn</div></div>
    <div class="tech-item"><div class="tech-icon">🐼</div><div class="tech-name">Pandas</div></div>
    <div class="tech-item"><div class="tech-icon">🔢</div><div class="tech-name">NumPy</div></div>
    <div class="tech-item"><div class="tech-icon">📊</div><div class="tech-name">Plotly</div></div>
    <div class="tech-item"><div class="tech-icon">📓</div><div class="tech-name">Jupyter</div></div>
    <div class="tech-item"><div class="tech-icon">🌐</div><div class="tech-name">Streamlit</div></div>
    <div class="tech-item"><div class="tech-icon">📦</div><div class="tech-name">Pickle</div></div>
    <div class="tech-item"><div class="tech-icon">📈</div><div class="tech-name">Matplotlib</div></div>
    <div class="tech-item"><div class="tech-icon">🔥</div><div class="tech-name">XGBoost</div></div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-wrap">
    <div class="footer-left">
        Built by <span>Shishir Singh</span> &nbsp;·&nbsp;
        AI/ML Researcher &nbsp;·&nbsp; IIT Bhubaneswar
    </div>
    <div class="footer-right">
        School of Electrical &amp; Computer Sciences &nbsp;·&nbsp; 2025
    </div>
</div>
""", unsafe_allow_html=True)