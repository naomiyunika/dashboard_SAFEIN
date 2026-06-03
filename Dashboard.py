import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SAFEIN Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"], p, div, span, h1, h2, h3, h4, h5, h6, label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp { background-color: #0a0e1a; }
.block-container { padding: 1.5rem 2.5rem 3rem 2.5rem !important; }
section[data-testid="stSidebar"] { background: #0f1420 !important; border-right: 1px solid #1e2540; }
section[data-testid="stSidebar"] * { color: #ccd6f6 !important; }

.dash-header {
    background: linear-gradient(135deg, #0f1420 0%, #111827 50%, #0a0e1a 100%);
    border: 1px solid #1e2540;
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.dash-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -10%;
    width: 40%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(100,255,218,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.dash-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #64ffda, #48cae4, #7b6cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
}
.dash-subtitle { color: #8892b0; font-size: 0.95rem; margin-top: 0.3rem; }

.kpi-card {
    background: linear-gradient(135deg, #111827, #1a2035);
    border: 1px solid #1e2540;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.kpi-card:hover { border-color: #64ffda44; }
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 16px 16px;
}
.kpi-income::after  { background: linear-gradient(90deg, #2ecc71, #27ae60); }
.kpi-expense::after { background: linear-gradient(90deg, #e74c3c, #c0392b); }
.kpi-score::after   { background: linear-gradient(90deg, #64ffda, #48cae4); }
.kpi-net::after     { background: linear-gradient(90deg, #7b6cf6, #5a4fcf); }
.kpi-label { font-size: 0.72rem; color: #8892b0; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 1.6rem; font-weight: 700; color: #e6f1ff; margin: 0.4rem 0 0.2rem; line-height: 1; }
.kpi-sub   { font-size: 0.75rem; color: #64ffda; font-weight: 500; }

.section-title {
    font-size: 1rem; font-weight: 700; color: #ccd6f6;
    border-left: 3px solid #64ffda; padding-left: 0.8rem;
    margin: 1.8rem 0 1rem;
    text-transform: uppercase; letter-spacing: 0.5px;
}

.chart-card {
    background: #111827;
    border: 1px solid #1e2540;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.chart-title {
    font-size: 0.85rem; font-weight: 700; color: #8892b0;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.8rem;
}

.result-card {
    border-radius: 16px; padding: 1.5rem; text-align: center; margin: 1rem 0;
}
.result-aman   { background: linear-gradient(135deg,#0d2818,#1a3a28); border: 1.5px solid #2ecc71; }
.result-bahaya { background: linear-gradient(135deg,#2a1f00,#3a2e00); border: 1.5px solid #f39c12; }
.result-rawan  { background: linear-gradient(135deg,#2a0d0d,#3a1515); border: 1.5px solid #e74c3c; }
.result-emoji  { font-size: 2.5rem; }
.result-label  { font-family:'Space Mono',monospace; font-size:1.8rem; font-weight:800; margin: 0.3rem 0; }
.result-score  { font-size:1rem; color:#ccd6f6; margin-bottom:0.3rem; }
.result-desc   { font-size:0.85rem; color:#8892b0; }

.insight-box {
    background: linear-gradient(135deg,#111827,#0f1e30);
    border: 1px solid #1e3a5f;
    border-left: 3px solid #48cae4;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 0.5rem;
    font-size: 0.88rem;
    color: #ccd6f6;
    line-height: 1.6;
}

.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2540, transparent);
    margin: 1.5rem 0;
}

div[data-testid="metric-container"] {
    background: #111827 !important;
    border: 1px solid #1e2540 !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
}
div[data-testid="metric-container"] label { color: #8892b0 !important; font-size: 0.75rem !important; }
div[data-testid="metric-container"] div[data-testid="metric-value"] { color: #e6f1ff !important; font-family: 'Space Mono', monospace !important; }

.stNumberInput input, .stSelectbox select {
    background: #1a2035 !important;
    border: 1px solid #1e2540 !important;
    color: #e6f1ff !important;
    border-radius: 8px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #64ffda, #48cae4) !important;
    color: #0a0e1a !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.95rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Hide default Streamlit header */
header[data-testid="stHeader"] {
    background-color: #0a0e1a !important;
    border-bottom: 1px solid #1e2540 !important;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
div[data-testid="stToolbar"] { display: none; }

/* Selectbox fix */
div[data-baseweb="select"] > div {
    background-color: #1a2035 !important;
    border: 1px solid #2e3a55 !important;
    border-radius: 8px !important;
    color: #e6f1ff !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #e6f1ff !important;
    background-color: transparent !important;
}
div[data-baseweb="popover"] ul {
    background-color: #1a2035 !important;
    border: 1px solid #2e3a55 !important;
}
div[data-baseweb="popover"] li {
    color: #ccd6f6 !important;
    background-color: #1a2035 !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: #2e3a55 !important;
    color: #64ffda !important;
}

.stTabs [data-baseweb="tab-list"] { background: #111827 !important; border-radius: 12px !important; padding: 4px !important; border: 1px solid #1e2540 !important; }
.stTabs [data-baseweb="tab"] { color: #8892b0 !important; font-weight: 600 !important; border-radius: 8px !important; }
.stTabs [aria-selected="true"] { background: #1e2540 !important; color: #64ffda !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly Theme ──────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans', color='#8892b0', size=11),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#ccd6f6')),
)
COLORS = {'AMAN': '#2ecc71', 'BAHAYA': '#f39c12', 'RAWAN': '#e74c3c'}
COLOR_SEQ = ['#64ffda','#7b6cf6','#f39c12','#e74c3c','#48cae4','#2ecc71','#e67e22','#3498db','#9b59b6','#1abc9c']

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "df_model_final.csv"))
    df['year']  = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['date']  = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
    return df

df = load_data()
p33 = df['financial_health_score'].quantile(0.33)
p66 = df['financial_health_score'].quantile(0.66)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 1.5rem;">
        <div style="font-size:2rem;">💰</div>
        <div style="font-size:1.1rem; font-weight:800; color:#64ffda;">SAFEIN</div>
        <div style="font-size:0.75rem; color:#8892b0;">Dashboard Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🗓️ Filter Data**")
    year_opt  = sorted(df['year'].unique())
    month_opt = sorted(df['month'].unique())
    sel_year  = st.selectbox("Tahun", year_opt, index=0)
    sel_month = st.selectbox("Bulan", month_opt, index=0)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("**📌 Info Dataset**")
    st.markdown(f"""
    <div style="font-size:0.8rem; color:#8892b0; line-height:2;">
        Total Rows: <b style="color:#64ffda">{len(df):,}</b><br>
        Total Users: <b style="color:#64ffda">{df['user_id'].nunique():,}</b><br>
        Periode: <b style="color:#64ffda">2023 – 2024</b>
    </div>
    """, unsafe_allow_html=True)

df_f = df[(df['year'] == sel_year) & (df['month'] == sel_month)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <div class="dash-title">📊 SAFEIN Financial Health Dashboard</div>
    <div class="dash-subtitle">Analisis Kesehatan Finansial Pengguna · {sel_year} / Bulan {sel_month}</div>
</div>
""", unsafe_allow_html=True)

# ── KPI ───────────────────────────────────────────────────────────────────────
total_income  = df_f['income'].sum()
total_expense = df_f['expense'].sum()
avg_score     = df_f['financial_health_score'].mean()
net_total     = total_income - total_expense

def fmt_rp(val):
    if val >= 1e9:  return f"Rp {val/1e9:.1f}M"
    if val >= 1e6:  return f"Rp {val/1e6:.1f}Jt"
    if val >= 1e3:  return f"Rp {val/1e3:.1f}Rb"
    return f"Rp {val:,.0f}"

k1, k2, k3, k4 = st.columns(4)
n_users = df_f['user_id'].nunique()
avg_income  = df_f['income'].mean()
avg_expense = df_f['expense'].mean()

with k1:
    st.markdown(f"""<div class="kpi-card kpi-income">
        <div class="kpi-label">Rata-rata Income / User</div>
        <div class="kpi-value">{fmt_rp(avg_income)}</div>
        <div class="kpi-sub">↑ Dari {n_users:,} user bulan ini</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card kpi-expense">
        <div class="kpi-label">Rata-rata Expense / User</div>
        <div class="kpi-value">{fmt_rp(avg_expense)}</div>
        <div class="kpi-sub">↓ Pengeluaran rata-rata</div>
    </div>""", unsafe_allow_html=True)
with k3:
    score_color = '#2ecc71' if avg_score >= p66 else '#f39c12' if avg_score >= p33 else '#e74c3c'
    st.markdown(f"""<div class="kpi-card kpi-score">
        <div class="kpi-label">Avg Health Score</div>
        <div class="kpi-value" style="color:{score_color}">{avg_score:.1f}</div>
        <div class="kpi-sub">Skala 0 – 100</div>
    </div>""", unsafe_allow_html=True)
with k4:
    avg_net = avg_income - avg_expense
    net_color = '#2ecc71' if avg_net >= 0 else '#e74c3c'
    st.markdown(f"""<div class="kpi-card kpi-net">
        <div class="kpi-label">Rata-rata Net / User</div>
        <div class="kpi-value" style="color:{net_color}">{fmt_rp(avg_net)}</div>
        <div class="kpi-sub">{'Surplus ✓' if avg_net >= 0 else 'Defisit ✗'}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊  Analisis Pertanyaan Bisnis", "🧮  Simulasi Keuangan Pribadi"])

# ════════════════════════════════════════════════════════════════════════
# TAB 1: VISUALISASI Q1–Q6
# ════════════════════════════════════════════════════════════════════════
with tab1:

    # ── Q1 ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Q1 · Distribusi Kategori Kesehatan Finansial</div>', unsafe_allow_html=True)
    user_label   = df_f.groupby('user_id')['label'].agg(lambda x: x.value_counts().index[0]).reset_index()
    label_counts = user_label['label'].value_counts().reindex(['AMAN','BAHAYA','RAWAN']).fillna(0).reset_index()
    label_counts.columns = ['label','count']

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(label_counts, x='label', y='count', color='label',
                     color_discrete_map=COLORS, text='count',
                     labels={'count':'Jumlah User','label':'Kategori'})
        fig.update_traces(texttemplate='<b>%{text:,}</b>', textposition='outside', marker_line_width=0)
        fig.update_layout(**PLOTLY_LAYOUT, title='Jumlah User per Kategori', showlegend=False,
                          yaxis=dict(gridcolor='#1e2540', showticklabels=False))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(label_counts, names='label', values='count', hole=0.5,
                     color='label', color_discrete_map=COLORS)
        fig.update_traces(textinfo='percent+label', textfont_size=12,
                          marker=dict(line=dict(color='#0a0e1a', width=3)))
        fig.update_layout(**PLOTLY_LAYOUT, title='Proporsi Kategori Kesehatan Finansial')
        st.plotly_chart(fig, use_container_width=True)

    total_u    = label_counts['count'].sum()
    pct_aman   = label_counts[label_counts['label']=='AMAN']['count'].sum() / total_u * 100 if total_u > 0 else 0
    pct_rawan  = label_counts[label_counts['label']=='RAWAN']['count'].sum() / total_u * 100 if total_u > 0 else 0
    pct_bahaya = label_counts[label_counts['label']=='BAHAYA']['count'].sum() / total_u * 100 if total_u > 0 else 0
    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Pada periode ini, <b>{pct_aman:.1f}%</b> user berada di kondisi <b style="color:#2ecc71">AMAN</b>,
        <b>{pct_bahaya:.1f}%</b> <b style="color:#f39c12">BAHAYA</b>, dan
        <b>{pct_rawan:.1f}%</b> <b style="color:#e74c3c">RAWAN</b>.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Q2 ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Q2 · Expense Ratio: Seberapa Besar Pengeluaran vs Income?</div>', unsafe_allow_html=True)
    er       = df_f['expense_ratio'].clip(0, 2)
    above_90 = (df_f['expense_ratio'] > 0.9).sum()
    pct_above = above_90 / len(df_f) * 100 if len(df_f) > 0 else 0

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df_f, x=er, nbins=50, color_discrete_sequence=['#48cae4'],
                           labels={'x':'Expense Ratio'})
        fig.add_vline(x=er.mean(), line_dash='dash', line_color='#e74c3c',
                      annotation_text=f'Rata-rata: {er.mean():.2f}', annotation_font_color='#e74c3c')
        fig.add_vline(x=0.9, line_dash='dash', line_color='#f39c12',
                      annotation_text='Batas 90%', annotation_font_color='#f39c12')
        fig.update_layout(**PLOTLY_LAYOUT, title='Distribusi Expense Ratio', bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        pie_df = pd.DataFrame({'Kategori':['≤ 90% income','>90% income'],
                               'Jumlah':[len(df_f)-above_90, above_90]})
        fig = px.pie(pie_df, names='Kategori', values='Jumlah', hole=0.5,
                     color='Kategori',
                     color_discrete_map={'≤ 90% income':'#2ecc71','>90% income':'#e74c3c'})
        fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#0a0e1a',width=3)))
        fig.update_layout(**PLOTLY_LAYOUT, title=f'User dgn Expense >90% Income ({pct_above:.1f}%)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Rata-rata expense ratio <b>{er.mean():.2%}</b> — user rata-rata menggunakan
        <b>{er.mean():.0%}</b> income untuk pengeluaran. Hanya <b>{pct_above:.1f}%</b> yang menghabiskan lebih dari 90% income.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Q3 ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Q3 · Hubungan Savings Rate & Financial Health Score</div>', unsafe_allow_html=True)
    corr_val = df_f['savings_rate'].clip(-1,2).corr(df_f['financial_health_score'])
    sample   = df_f.sample(min(2000, len(df_f)), random_state=42)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(sample, x=sample['savings_rate'].clip(-1,1), y='financial_health_score',
                         color='label', color_discrete_map=COLORS, opacity=0.5,
                         labels={'x':'Savings Rate','financial_health_score':'Health Score'},
                         title=f'Savings Rate vs Health Score (Korelasi: {corr_val:.3f})')
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        box_df = df_f[df_f['label'].isin(['AMAN','BAHAYA','RAWAN'])].copy()
        box_df['savings_rate_c'] = box_df['savings_rate'].clip(-1,1)
        fig = px.box(box_df, x='label', y='savings_rate_c', color='label',
                     color_discrete_map=COLORS,
                     labels={'savings_rate_c':'Savings Rate','label':'Kategori'},
                     title='Distribusi Savings Rate per Kategori',
                     category_orders={'label':['AMAN','BAHAYA','RAWAN']})
        fig.add_hline(y=0, line_dash='dash', line_color='#8892b0', line_width=1)
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    strength = "sangat kuat" if abs(corr_val) > 0.7 else "kuat" if abs(corr_val) > 0.5 else "sedang" if abs(corr_val) > 0.3 else "lemah"
    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Korelasi <b>{corr_val:.3f}</b> menunjukkan hubungan <b>positif {strength}</b> —
        semakin tinggi savings rate, semakin baik kondisi finansial user.
        User AMAN cenderung memiliki savings rate positif, sementara RAWAN banyak yang negatif.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Q4 ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Q4 · Proporsi Pengeluaran Essential vs Non-Essential</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df_f, x=df_f['essential_ratio'].clip(0,1), nbins=50,
                           color_discrete_sequence=['#7b6cf6'],
                           labels={'x':'Essential Ratio'})
        fig.add_vline(x=df_f['essential_ratio'].mean(), line_dash='dash', line_color='#e74c3c',
                      annotation_text=f"Rata-rata: {df_f['essential_ratio'].mean():.2%}",
                      annotation_font_color='#e74c3c')
        fig.add_vline(x=0.5, line_dash='dash', line_color='#f39c12',
                      annotation_text='Batas 50%', annotation_font_color='#f39c12')
        fig.update_layout(**PLOTLY_LAYOUT, title='Distribusi Essential Ratio', bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ess_by = df_f.groupby('label')['essential_ratio'].mean().reindex(['AMAN','BAHAYA','RAWAN']).fillna(0)
        bar_df = pd.DataFrame({
            'Kategori': ['AMAN','BAHAYA','RAWAN','AMAN','BAHAYA','RAWAN'],
            'Tipe': ['Essential']*3 + ['Non-Essential']*3,
            'Proporsi': list(ess_by*100) + list((1-ess_by)*100)
        })
        fig = px.bar(bar_df, x='Kategori', y='Proporsi', color='Tipe', barmode='group',
                     color_discrete_map={'Essential':'#3498db','Non-Essential':'#e67e22'},
                     labels={'Proporsi':'Proporsi (%)'},
                     title='Essential vs Non-Essential per Kategori',
                     category_orders={'Kategori':['AMAN','BAHAYA','RAWAN']})
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Rata-rata <b>{df_f['essential_ratio'].mean():.1%}</b> pengeluaran dialokasikan untuk kebutuhan pokok.
        User RAWAN cenderung mengalokasikan lebih besar untuk essential,
        mengindikasikan keterbatasan finansial dan minimnya ruang untuk pengeluaran non-esensial.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Q5 ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Q5 · Income Fluktuatif vs Financial Health Score</div>', unsafe_allow_html=True)
    corr_cv = df_f['income_cv'].clip(0,5).corr(df_f['financial_health_score'])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(sample, x=sample['income_cv'].clip(0,1.5), y='financial_health_score',
                         color='label', color_discrete_map=COLORS, opacity=0.5,
                         labels={'x':'Income CV (fluktuasi)','financial_health_score':'Health Score'},
                         title=f'Income CV vs Health Score (Korelasi: {corr_cv:.3f})')
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.box(df_f, x='label', y=df_f['income_cv'].clip(0,1.5), color='label',
                     color_discrete_map=COLORS,
                     labels={'y':'Income CV','label':'Kategori'},
                     title='Distribusi Income CV per Kategori',
                     category_orders={'label':['AMAN','BAHAYA','RAWAN']})
        fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Korelasi income CV dengan health score sebesar <b>{corr_cv:.3f}</b> —
        fluktuasi income berpengaruh negatif terhadap kesehatan finansial.
        User dengan income lebih stabil cenderung berada di kategori AMAN.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Q6 ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Q6 · Kategori Pengeluaran dengan Kontribusi Terbesar</div>', unsafe_allow_html=True)

    cat_cols  = [c for c in df_f.columns if c.startswith('cat_')]
    cat_total = df_f[cat_cols].sum().sort_values(ascending=False)
    cat_total.index = [c.replace('cat_','') for c in cat_total.index]
    top10 = cat_total.head(10).reset_index()
    top10.columns = ['Kategori','Total']

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(top10.sort_values('Total'), x='Total', y='Kategori', orientation='h',
                     color='Total', color_continuous_scale=['#1e3a5f','#64ffda'],
                     text=top10.sort_values('Total')['Total'].apply(fmt_rp),
                     labels={'Total':'Total Amount (Rp)','Kategori':''},
                     title='Top 10 Kategori Pengeluaran')
        fig.update_traces(textposition='outside')
        fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                          xaxis=dict(gridcolor='#1e2540', tickformat='.0s'))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        top5    = cat_total.head(5)
        other   = cat_total.iloc[5:].sum()
        pie_cat = pd.concat([top5, pd.Series({'Lainnya': other})]).reset_index()
        pie_cat.columns = ['Kategori','Total']
        fig = px.pie(pie_cat, names='Kategori', values='Total', hole=0.5,
                     color_discrete_sequence=COLOR_SEQ,
                     title='Proporsi Top 5 Kategori')
        fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#0a0e1a',width=3)))
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> <b>{top10.iloc[-1]['Kategori']}</b> mendominasi pengeluaran dengan total
        <b>{fmt_rp(top10.iloc[-1]['Total'])}</b>, diikuti <b>{top10.iloc[-2]['Kategori']}</b>.
        Top 5 kategori menyumbang <b>{top5.sum()/cat_total.sum():.1%}</b> dari total pengeluaran.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Bonus: Income vs Expense scatter & Top 10 Score ───────────────
    st.markdown('<div class="section-title">📌 Analisis Tambahan</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(df_f, x='income', y='expense', color='label',
                         color_discrete_map=COLORS, opacity=0.5,
                         size='financial_health_score', hover_data=['user_id'],
                         labels={'income':'Income','expense':'Expense'},
                         title='Income vs Expense per User')
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        top10_score = df_f.sort_values('financial_health_score', ascending=False).head(10)
        fig = px.bar(top10_score, x='user_id', y='financial_health_score',
                     color='financial_health_score',
                     color_continuous_scale=['#e74c3c','#f39c12','#2ecc71'],
                     labels={'financial_health_score':'Health Score','user_id':'User'},
                     title='Top 10 User Financial Score')
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    show_table = st.checkbox("Tampilkan Data Detail")
    if show_table:
        st.dataframe(
            df_f[['user_id','year','month','income','expense','net','savings_rate',
                  'expense_ratio','financial_health_score','label']].style.background_gradient(
                  subset=['financial_health_score'], cmap='RdYlGn'),
            use_container_width=True
        )

# ════════════════════════════════════════════════════════════════════════
# TAB 2: SIMULASI
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#111827,#1a2035); border:1px solid #1e2540;
                border-radius:16px; padding:1.5rem; margin-bottom:1.5rem;">
        <div style="font-size:1.1rem; font-weight:800; color:#64ffda;">🧮 Simulasi Kesehatan Keuangan</div>
        <div style="color:#8892b0; font-size:0.85rem; margin-top:0.3rem;">
            Masukkan data keuangan bulananmu untuk mengetahui kondisi finansialmu
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_res = st.columns([1,1], gap="large")

    with col_form:
        st.markdown('<div class="section-title">💼 Income & Expense</div>', unsafe_allow_html=True)
        user_income  = st.number_input("Total Income Bulan Ini (Rp)", min_value=0, value=5000000, step=100000, format="%d")
        user_expense = st.number_input("Total Expense Bulan Ini (Rp)", min_value=0, value=3000000, step=100000, format="%d")

        st.markdown('<div class="section-title">🛒 Pengeluaran per Kategori (Rp)</div>', unsafe_allow_html=True)
        cat_list = [("Food","🍱"),("Transport","🚌"),("Health","🏥"),("Rent","🏠"),
                    ("Utilities","💡"),("Shopping","🛍️"),("Entertainment","🎬"),
                    ("Cafe","☕"),("Education","📚"),("Travel","✈️"),
                    ("Subscription","📱"),("Personal Care","💆"),("Gifts","🎁")]
        cat_inputs = {}
        c1, c2 = st.columns(2)
        for i, (cat, icon) in enumerate(cat_list):
            with (c1 if i%2==0 else c2):
                cat_inputs[cat] = st.number_input(f"{icon} {cat}", min_value=0, value=0, step=10000, format="%d", key=f"s_{cat}")

        st.markdown('<div class="section-title">📊 Stabilitas Keuangan</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: income_cv_in  = st.slider("Income CV (fluktuasi)", 0.0, 2.0, 0.5, 0.01)
        with c2: expense_cv_in = st.slider("Expense CV (fluktuasi)", 0.0, 2.0, 0.5, 0.01)

        btn = st.button("🔮 Analisis Sekarang", use_container_width=True, type="primary")

    with col_res:
        if btn:
            if user_income == 0:
                st.error("⚠️ Income tidak boleh 0!")
            else:
                net_u           = user_income - user_expense
                savings_rate_u  = net_u / user_income
                expense_ratio_u = user_expense / user_income
                ess_cats        = ['Food','Transport','Health','Rent','Utilities']
                ess_exp         = sum(cat_inputs.get(c,0) for c in ess_cats)
                ess_ratio_u     = ess_exp / user_expense if user_expense > 0 else 0

                sr  = np.clip(savings_rate_u * 100, 0, 100)
                er  = np.clip((1 - expense_ratio_u) * 100, 0, 100)
                ess = np.clip((1 - ess_ratio_u) * 100, 0, 100)
                ins = np.clip((1 - income_cv_in) * 100, 0, 100)
                evs = np.clip((1 - expense_cv_in) * 100, 0, 100)
                fhs = np.clip(sr*0.3 + er*0.2 + ess*0.2 + ins*0.15 + evs*0.15, 0, 100)

                if fhs >= p66:
                    lbl, emoji, desc = "AMAN", "✅", "Kondisi keuanganmu sehat! Savings rate baik dan pengeluaran terkontrol."
                elif fhs >= p33:
                    lbl, emoji, desc = "BAHAYA", "⚠️", "Perlu perhatian. Coba kurangi pengeluaran non-esensial."
                else:
                    lbl, emoji, desc = "RAWAN", "🚨", "Kondisi keuanganmu rawan! Pengeluaran terlalu besar vs income."

                st.markdown(f"""
                <div class="result-card result-{lbl.lower()}">
                    <div class="result-emoji">{emoji}</div>
                    <div class="result-label" style="color:{COLORS[lbl]}">{lbl}</div>
                    <div class="result-score">Health Score: <b style="font-family:'Space Mono',monospace">{fhs:.1f} / 100</b></div>
                    <div class="result-desc">{desc}</div>
                </div>""", unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                m1.metric("Savings Rate", f"{savings_rate_u:.1%}", delta="Baik ✓" if savings_rate_u>0.2 else "Perlu naik")
                m2.metric("Expense Ratio", f"{expense_ratio_u:.1%}", delta="Aman ✓" if expense_ratio_u<0.7 else "Terlalu tinggi", delta_color="inverse")
                m3.metric("Net Bulanan", fmt_rp(net_u), delta="Surplus ✓" if net_u>=0 else "Defisit", delta_color="normal" if net_u>=0 else "inverse")

                # Score breakdown
                st.markdown('<div class="section-title">📊 Breakdown Score</div>', unsafe_allow_html=True)
                sc_labels = ['Savings Rate','Expense Ratio','Essential Ratio','Income Stability','Expense Stability']
                sc_vals   = [sr, er, ess, ins, evs]
                sc_colors = ['#2ecc71' if v>=60 else '#f39c12' if v>=40 else '#e74c3c' for v in sc_vals]

                fig = go.Figure(go.Bar(
                    x=sc_labels, y=sc_vals, marker_color=sc_colors,
                    text=[f'{v:.0f}' for v in sc_vals], textposition='outside'
                ))
                fig.add_hline(y=60, line_dash='dash', line_color='#2ecc71', line_width=1, opacity=0.4)
                fig.add_hline(y=40, line_dash='dash', line_color='#e74c3c', line_width=1, opacity=0.4)
                fig.update_layout(**PLOTLY_LAYOUT, yaxis=dict(range=[0,115], gridcolor='#1e2540'),
                                  showlegend=False, height=280)
                st.plotly_chart(fig, use_container_width=True)

                # Pie pengeluaran
                cat_user = {k:v for k,v in cat_inputs.items() if v>0}
                if cat_user:
                    st.markdown('<div class="section-title">🥧 Komposisi Pengeluaranmu</div>', unsafe_allow_html=True)
                    pie_u = pd.DataFrame({'Kategori':list(cat_user.keys()),'Amount':list(cat_user.values())})
                    fig = px.pie(pie_u, names='Kategori', values='Amount', hole=0.4,
                                 color_discrete_sequence=COLOR_SEQ)
                    fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#0a0e1a',width=2)))
                    fig.update_layout(**PLOTLY_LAYOUT, height=280)
                    st.plotly_chart(fig, use_container_width=True)

                # Rekomendasi
                st.markdown('<div class="section-title">💡 Rekomendasi</div>', unsafe_allow_html=True)
                recs = []

                if lbl == "RAWAN":
                    recs.append(("🚨", "Kondisi keuangan RAWAN — prioritaskan mengurangi pengeluaran segera"))
                elif lbl == "BAHAYA":
                    recs.append(("⚠️", "Kondisi keuangan BAHAYA — perlu perbaikan di beberapa aspek keuangan"))

                if savings_rate_u < 0.1:
                    recs.append(("📌", "Tingkatkan tabungan — idealnya minimal 10-20% dari income"))
                if expense_ratio_u > 0.8:
                    recs.append(("📌", "Kurangi total pengeluaran — sudah melebihi 80% income"))
                if ess_ratio_u > 0.7:
                    recs.append(("📌", "Pengeluaran esensial dominan — pertimbangkan efisiensi biaya pokok"))
                if income_cv_in > 0.5:
                    recs.append(("📌", "Income cukup fluktuatif — pertimbangkan membangun passive income atau dana darurat"))
                if expense_cv_in > 0.5:
                    recs.append(("📌", "Pengeluaran tidak stabil — coba buat anggaran bulanan yang konsisten"))

                if lbl == "AMAN" and not recs:
                    recs.append(("✅", "Kondisi keuanganmu sudah baik! Pertahankan pola ini."))

                for icon, rec in recs:
                    st.markdown(f'<div class="insight-box">{icon} {rec}</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="height:420px; display:flex; align-items:center; justify-content:center;
                        background:linear-gradient(135deg,#111827,#1a2035); border-radius:16px;
                        border:1px dashed #1e2540;">
                <div style="text-align:center; color:#8892b0;">
                    <div style="font-size:4rem; margin-bottom:1rem;">🧮</div>
                    <div style="font-size:1rem; font-weight:600;">Isi form di sebelah kiri</div>
                    <div style="font-size:0.85rem; margin-top:0.3rem;">lalu klik
                        <b style="color:#64ffda">Analisis Sekarang</b>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 0.5rem; color:#3a4466; font-size:0.78rem;">
    FinHealth Dashboard · Capstone Project Data Science · 2024
</div>
""", unsafe_allow_html=True)