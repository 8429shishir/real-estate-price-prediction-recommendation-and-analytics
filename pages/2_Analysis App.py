import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Analysis App — Real Estate AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060b14 !important;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}
.block-container { padding: 2rem 3rem !important; max-width: 1300px !important; }

[data-testid="stSidebar"] {
    background: #0d1525 !important;
    border-right: 1px solid #1e2d45 !important;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stMarkdown h3 { color: #38bdf8 !important; }

/* ── Page Header ── */
.page-header {
    padding: 32px 36px;
    background: linear-gradient(135deg, #0d1525, #0f1e35);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 6px;
}
.header-sub { font-size: 15px; color: #64748b; line-height: 1.6; }

/* ── KPI Cards ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 32px;
}
.kpi-card {
    background: #0d1525;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    transition: all 0.25s ease;
}
.kpi-card:hover {
    border-color: #38bdf8;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(56,189,248,0.12);
}
.kpi-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.kpi-label { font-size: 11px; color: #64748b; font-weight: 500; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.8px; }

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    margin-top: 10px;
}
.section-header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f1f5f9;
}
.section-header-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, #1e2d45, transparent);
}

/* ── Chart card ── */
.chart-card {
    background: #0d1525;
    border: 1px solid #1e2d45;
    border-radius: 16px;
    padding: 6px;
    margin-bottom: 20px;
    overflow: hidden;
}

/* ── Filter label ── */
.filter-label {
    font-size: 11px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d45;
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
}
.topnav-crumb { font-size: 13px; color: #475569; }
.topnav-crumb span { color: #94a3b8; }

/* ── Plotly chart background ── */
.js-plotly-plot { border-radius: 12px; }

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

# ── Plotly dark theme defaults ─────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='#0d1525',
    plot_bgcolor='#0a1220',
    font=dict(family='Inter', color='#94a3b8', size=12),
    title_font=dict(family='Space Grotesk', color='#f1f5f9', size=16),
    legend=dict(
        bgcolor='rgba(13,21,37,0.9)', bordercolor='#1e2d45', borderwidth=1,
        font=dict(size=12, color='#94a3b8')
    ),
    colorway=['#38bdf8', '#818cf8', '#34d399', '#fb923c', '#f472b6', '#facc15', '#a78bfa'],
    margin=dict(l=40, r=20, t=50, b=40)
)

AXIS_STYLE = dict(gridcolor='#1e2d45', linecolor='#1e2d45', tickcolor='#475569')


def apply_theme(fig, height=None, extra_layout=None):
    """Apply consistent dark theme to a plotly figure."""
    layout_kwargs = dict(**PLOT_LAYOUT)
    if height:
        layout_kwargs['height'] = height
    if extra_layout:
        layout_kwargs.update(extra_layout)
    fig.update_layout(**layout_kwargs)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig

COLORS = {
    'blue': '#38bdf8', 'purple': '#818cf8', 'green': '#34d399',
    'orange': '#fb923c', 'pink': '#f472b6', 'yellow': '#facc15',
    'violet': '#a78bfa', 'teal': '#2dd4bf', 'red': '#f87171'
}

# ── Load Data ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data(show_spinner="Loading dataset...")
def load_data():
    path = os.path.join(BASE_DIR, 'Data_Clean', 'flats_and_house_missing_value_immputation.csv')
    df = pd.read_csv(path)
    # Ensure price column is numeric
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df

try:
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"❌ Could not load dataset: {e}")
    data_loaded = False
    st.stop()

# ── Top Navigation Bar ──────────────────────────────────────────────────────
col_back, col_mid, col_right = st.columns([1, 4, 1])
with col_back:
    st.page_link("Home.py", label="← Home", icon="🏠")
with col_right:
    st.page_link("pages/1_Price Predictor.py", label="Price Predictor", icon="🏠")

st.markdown("""
<div class="topnav">
    <div class="topnav-brand">🏠 Real Estate AI</div>
    <div class="topnav-crumb">Home &nbsp;/&nbsp; <span>Analysis App</span></div>
</div>
""", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="header-title">📊 Real Estate Market Analysis</div>
    <div class="header-sub">
        Interactive analytics dashboard for the Gurgaon residential real estate market. 
        Explore price distributions, sector trends, and feature correlations across 13,000+ properties.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 Dashboard Filters")
    st.markdown("---")

    # Property type
    prop_types = ['All'] + sorted(df['property_type'].dropna().unique().tolist()) if 'property_type' in df.columns else ['All']
    selected_type = st.selectbox("Property Type", prop_types)

    # Bedroom filter
    if 'bedRoom' in df.columns:
        bed_options = ['All'] + [str(int(x)) for x in sorted(df['bedRoom'].dropna().unique().tolist())]
        selected_beds = st.selectbox("Bedrooms (BHK)", bed_options)
    else:
        selected_beds = 'All'

    # Sector filter
    if 'sector' in df.columns:
        sectors = ['All'] + sorted(df['sector'].dropna().unique().tolist())
        selected_sector = st.selectbox("Sector", sectors)
    else:
        selected_sector = 'All'

    # Price range
    if 'price' in df.columns:
        p_min = float(df['price'].min())
        p_max = float(df['price'].max())
        price_range = st.slider(
            "Price Range (Cr)",
            min_value=round(p_min, 1),
            max_value=round(p_max, 1),
            value=(round(p_min, 1), min(round(p_max, 1), 20.0)),
            step=0.5
        )
    else:
        price_range = (0, 100)

    st.markdown("---")
    st.markdown("**Dataset:** Gurgaon, India")
    st.markdown(f"**Total records:** {len(df):,}")

# ── Apply Filters ─────────────────────────────────────────────────────────────
fdf = df.copy()
if selected_type != 'All' and 'property_type' in fdf.columns:
    fdf = fdf[fdf['property_type'] == selected_type]
if selected_beds != 'All' and 'bedRoom' in fdf.columns:
    fdf = fdf[fdf['bedRoom'] == float(selected_beds)]
if selected_sector != 'All' and 'sector' in fdf.columns:
    fdf = fdf[fdf['sector'] == selected_sector]
if 'price' in fdf.columns:
    fdf = fdf[(fdf['price'] >= price_range[0]) & (fdf['price'] <= price_range[1])]

# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_props = len(fdf)
avg_price = fdf['price'].mean() if 'price' in fdf.columns else 0
med_price = fdf['price'].median() if 'price' in fdf.columns else 0
n_sectors = fdf['sector'].nunique() if 'sector' in fdf.columns else 0
avg_area = fdf['built_up_area'].mean() if 'built_up_area' in fdf.columns else 0

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-val">{total_props:,}</div>
        <div class="kpi-label">Properties</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-val">₹ {avg_price:.2f} Cr</div>
        <div class="kpi-label">Avg. Price</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-val">₹ {med_price:.2f} Cr</div>
        <div class="kpi-label">Median Price</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-val">{n_sectors}</div>
        <div class="kpi-label">Sectors</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-val">{avg_area:,.0f}</div>
        <div class="kpi-label">Avg. Area (sqft)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — Price Distribution
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">📈 Price Distribution</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    if 'price' in fdf.columns and len(fdf) > 0:
        fig1 = px.histogram(
            fdf, x='price', nbins=50,
            labels={'price': 'Price (Cr)', 'count': 'Count'},
            title="Price Distribution",
            color_discrete_sequence=[COLORS['blue']],
            template='plotly_dark'
        )
        apply_theme(fig1)
        fig1.update_traces(marker_line_width=0, opacity=0.85)
        fig1.add_vline(x=avg_price, line_dash='dash', line_color=COLORS['orange'],
                       annotation_text=f"Avg ₹{avg_price:.1f}Cr",
                       annotation_font_color=COLORS['orange'])
        st.plotly_chart(fig1, use_container_width=True)

with col_b:
    if 'price' in fdf.columns and 'property_type' in fdf.columns and len(fdf) > 0:
        fig2 = px.box(
            fdf, x='property_type', y='price',
            color='property_type',
            title="Price by Property Type",
            labels={'property_type': 'Property Type', 'price': 'Price (Cr)'},
            color_discrete_map={'Flat': COLORS['blue'], 'House': COLORS['purple']},
            template='plotly_dark'
        )
        apply_theme(fig2)
        fig2.update_traces(boxmean='sd')
        st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — Price vs Area
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">📐 Price vs Built-up Area</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

if 'built_up_area' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
    scatter_df = fdf[fdf['built_up_area'] < fdf['built_up_area'].quantile(0.99)].copy()

    color_col = 'property_type' if 'property_type' in scatter_df.columns else None
    hover_cols = {c: True for c in ['bedRoom', 'sector', 'furnishing_type'] if c in scatter_df.columns}

    fig3 = px.scatter(
        scatter_df, x='built_up_area', y='price',
        color=color_col,
        title="Price vs. Built-up Area (sqft)",
        labels={'built_up_area': 'Built-up Area (sqft)', 'price': 'Price (Cr)'},
        opacity=0.55,
        trendline='ols',
        trendline_scope='overall',
        color_discrete_map={'Flat': COLORS['blue'], 'House': COLORS['purple']},
        template='plotly_dark',
        hover_data=hover_cols if hover_cols else None
    )
    apply_theme(fig3)
    fig3.update_traces(marker=dict(size=5))
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — Bedroom Analysis
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">🛏️ Bedroom-wise Analysis</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    if 'bedRoom' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
        bed_grp = fdf.groupby('bedRoom')['price'].agg(['mean', 'median', 'count']).reset_index()
        bed_grp.columns = ['Bedrooms', 'Mean Price', 'Median Price', 'Count']

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=bed_grp['Bedrooms'].astype(str),
            y=bed_grp['Mean Price'],
            name='Mean Price', marker_color=COLORS['blue'],
            text=bed_grp['Mean Price'].round(2),
            texttemplate='₹%{text}Cr', textposition='outside'
        ))
        fig4.add_trace(go.Bar(
            x=bed_grp['Bedrooms'].astype(str),
            y=bed_grp['Median Price'],
            name='Median Price', marker_color=COLORS['purple'],
            text=bed_grp['Median Price'].round(2),
            texttemplate='₹%{text}Cr', textposition='outside'
        ))
        apply_theme(fig4, extra_layout={
            'title': {'text': 'Avg & Median Price by Bedrooms'},
            'xaxis_title': 'Bedrooms (BHK)',
            'yaxis_title': 'Price (Cr)',
            'barmode': 'group'
        })
        st.plotly_chart(fig4, use_container_width=True)

with col_d:
    if 'bedRoom' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
        fig5 = px.violin(
            fdf[fdf['bedRoom'] <= 6], x='bedRoom', y='price',
            color='bedRoom',
            title='Price Distribution per BHK',
            labels={'bedRoom': 'Bedrooms', 'price': 'Price (Cr)'},
            box=True, points=False,
            template='plotly_dark',
            color_discrete_sequence=list(COLORS.values())
        )
        apply_theme(fig5)
        st.plotly_chart(fig5, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — Sector Analysis
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">🗺️ Sector-wise Price Analysis</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

if 'sector' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
    sector_grp = (
        fdf.groupby('sector')['price']
        .agg(['mean', 'count'])
        .reset_index()
        .rename(columns={'mean': 'Avg Price', 'count': 'Count'})
        .sort_values('Avg Price', ascending=False)
    )
    top_sectors = sector_grp.head(20)

    fig6 = px.bar(
        top_sectors, x='Avg Price', y='sector',
        orientation='h',
        title='Top 20 Sectors by Average Price (₹ Cr)',
        labels={'Avg Price': 'Average Price (Cr)', 'sector': 'Sector'},
        color='Avg Price',
        color_continuous_scale=[[0, '#0d1f38'], [0.5, '#2563eb'], [1.0, '#38bdf8']],
        template='plotly_dark',
        text='Avg Price'
    )
    fig6.update_traces(texttemplate='₹%{text:.2f}Cr', textposition='outside')
    apply_theme(fig6, height=520, extra_layout={'coloraxis_showscale': False})
    fig6.update_yaxes(categoryorder='total ascending')
    st.plotly_chart(fig6, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — Categorical Breakdowns
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">🏷️ Categorical Feature Analysis</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    if 'luxury_category' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
        lux_grp = fdf.groupby('luxury_category')['price'].mean().reset_index()
        lux_grp.columns = ['Luxury Category', 'Avg Price']

        fig7 = px.pie(
            lux_grp, names='Luxury Category', values='Avg Price',
            title='Avg Price Share by Luxury Category',
            color_discrete_sequence=list(COLORS.values()),
            hole=0.45,
            template='plotly_dark'
        )
        apply_theme(fig7)
        fig7.update_traces(textposition='outside', textinfo='label+percent',
                           pull=[0.05] * len(lux_grp))
        st.plotly_chart(fig7, use_container_width=True)

with col_f:
    if 'furnishing_type' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
        furn_grp = fdf.groupby('furnishing_type')['price'].agg(['mean', 'count']).reset_index()
        furn_grp.columns = ['Furnishing', 'Avg Price', 'Count']

        fig8 = px.bar(
            furn_grp.sort_values('Avg Price', ascending=True),
            x='Avg Price', y='Furnishing', orientation='h',
            title='Avg Price by Furnishing Type',
            labels={'Avg Price': 'Avg Price (Cr)', 'Furnishing': ''},
            color='Avg Price',
            color_continuous_scale=[[0, '#0d1f38'], [1.0, '#818cf8']],
            text='Avg Price',
            template='plotly_dark'
        )
        fig8.update_traces(texttemplate='₹%{text:.2f}Cr', textposition='outside')
        apply_theme(fig8, extra_layout={'coloraxis_showscale': False})
        st.plotly_chart(fig8, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — Floor Category & Age Possession
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">🏢 Floor & Possession Analysis</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    if 'floor_category' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
        floor_grp = fdf.groupby('floor_category')['price'].mean().reset_index()
        floor_grp.columns = ['Floor Category', 'Avg Price']

        fig9 = px.bar(
            floor_grp.sort_values('Avg Price', ascending=False),
            x='Floor Category', y='Avg Price',
            title='Avg Price by Floor Category',
            color='Floor Category',
            labels={'Avg Price': 'Avg Price (Cr)'},
            color_discrete_sequence=list(COLORS.values()),
            template='plotly_dark',
            text='Avg Price'
        )
        fig9.update_traces(texttemplate='₹%{text:.2f}Cr', textposition='outside')
        apply_theme(fig9)
        st.plotly_chart(fig9, use_container_width=True)

with col_h:
    if 'agePossession' in fdf.columns and 'price' in fdf.columns and len(fdf) > 0:
        age_grp = fdf.groupby('agePossession')['price'].agg(['mean', 'count']).reset_index()
        age_grp.columns = ['Age/Possession', 'Avg Price', 'Count']
        age_grp = age_grp.sort_values('Avg Price', ascending=False)

        fig10 = px.bar(
            age_grp,
            x='Age/Possession', y='Avg Price',
            title='Avg Price by Possession Status',
            color='Avg Price',
            labels={'Avg Price': 'Avg Price (Cr)', 'Age/Possession': ''},
            color_continuous_scale=[[0, '#0d1f38'], [1.0, '#34d399']],
            template='plotly_dark',
            text='Avg Price'
        )
        fig10.update_traces(texttemplate='₹%{text:.2f}Cr', textposition='outside')
        apply_theme(fig10, extra_layout={'coloraxis_showscale': False})
        fig10.update_xaxes(tickangle=-30)
        st.plotly_chart(fig10, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — Correlation Heatmap
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">🔥 Feature Correlation Heatmap</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

num_cols = [c for c in ['price', 'bedRoom', 'bathroom', 'built_up_area', 'servant room', 'store room']
            if c in fdf.columns]

if len(num_cols) >= 2 and len(fdf) > 0:
    corr = fdf[num_cols].dropna().corr().round(3)
    labels = {
        'price': 'Price (Cr)', 'bedRoom': 'Bedrooms',
        'bathroom': 'Bathrooms', 'built_up_area': 'Built-up Area',
        'servant room': 'Servant Room', 'store room': 'Store Room'
    }
    display_labels = [labels.get(c, c) for c in num_cols]

    fig11 = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=display_labels,
        y=display_labels,
        colorscale=[[0, '#0d1f38'], [0.5, '#2563eb'], [1.0, '#38bdf8']],
        text=corr.values,
        texttemplate='%{text:.2f}',
        textfont=dict(size=13, color='white'),
        showscale=True,
        zmin=-1, zmax=1
    ))
    apply_theme(fig11, height=420, extra_layout={
        'title': {'text': 'Feature Correlation Matrix'}
    })
    st.plotly_chart(fig11, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — Raw Data Explorer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-header-title">🗃️ Raw Data Explorer</div>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

with st.expander(f"📋 Browse Dataset ({len(fdf):,} records after filters)", expanded=False):
    display_cols = [c for c in
        ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
         'built_up_area', 'price', 'furnishing_type', 'luxury_category',
         'floor_category', 'agePossession']
        if c in fdf.columns]
    st.dataframe(
        fdf[display_cols].rename(columns={
            'property_type': 'Type', 'sector': 'Sector',
            'bedRoom': 'BHK', 'bathroom': 'Bath', 'balcony': 'Balcony',
            'built_up_area': 'Area (sqft)', 'price': 'Price (Cr)',
            'furnishing_type': 'Furnishing', 'luxury_category': 'Luxury',
            'floor_category': 'Floor', 'agePossession': 'Possession'
        }).head(500),
        use_container_width=True, height=350
    )
    st.caption("Showing first 500 rows of filtered data.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #1e2d45; padding-top:24px; margin-top:24px;
            font-size:13px; color:#475569; text-align:center;">
    Real Estate Market Analysis Dashboard &nbsp;·&nbsp; 
    Built by <span style="color:#38bdf8; font-weight:600;">Shishir Singh</span> &nbsp;·&nbsp; 
    IIT Bhubaneswar &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)
