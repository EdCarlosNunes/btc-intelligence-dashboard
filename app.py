import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="Inteligência BTC | Rastreador de Halving",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Data ---
@st.cache_data
def load_data():
    try:
        with open('data/btc_data.json', 'r') as f:
            df = pd.DataFrame(json.load(f))
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        return pd.DataFrame({'date': [datetime.now()], 'price': [0]})

df = load_data()
curr_p = df['price'].iloc[-1]
max_p = df['price'].max()

# Countdown
nh = datetime(2028, 4, 1)
diff = nh - datetime.now()
days = diff.days
hours = diff.seconds // 3600
mins = (diff.seconds % 3600) // 60
secs = diff.seconds % 60

# ============================
# CSS - All styling via classes
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {background: #f8fafc;}
.block-container {padding-top: 0 !important; padding-bottom: 2rem !important; max-width: 1200px !important; margin-top: -2rem !important;}
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}

/* NAV */
.top-nav {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 1rem 3rem; display: flex; justify-content: space-between; align-items: center; border-radius: 0 0 1.5rem 1.5rem; margin: 0 -2rem; box-shadow: 0 4px 30px rgba(15, 23, 42, 0.15); margin-bottom: 3rem;}
.nav-left {display: flex; align-items: center; gap: 0.75rem;}
.nav-logo {background: linear-gradient(135deg, #f97316, #ea580c); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 20px; box-shadow: 0 4px 15px rgba(249, 115, 22, 0.4);}
.nav-title {color: white; font-size: 1.25rem; font-weight: 800; margin: 0;}
.nav-sub {color: #94a3b8; font-size: 0.6rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin: 0;}
.badge-live {background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #10b981; padding: 0.4rem 1rem; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;}
.dot {height: 8px; width: 8px; background-color: #10b981; border-radius: 50%; display: inline-block; animation: pulse 2s infinite;}
@keyframes pulse {0% {transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16,185,129,0.7);} 70% {transform: scale(1); box-shadow: 0 0 0 8px rgba(16,185,129,0);} 100% {transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16,185,129,0);}}

/* HERO */
.hero-card {background: rgba(255,255,255,0.7); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.6); border-radius: 2.5rem; padding: 4rem; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.05); display: flex; gap: 4rem; align-items: center; margin-bottom: 3rem;}
.hero-left {flex: 1.5;}
.hero-right {flex: 1;}
.hero-title {font-size: 3.5rem; font-weight: 800; line-height: 1.08; color: #0f172a !important; margin: 0 0 1.5rem 0; letter-spacing: -0.02em;}
.hero-accent {color: #f97316;}
.hero-p {font-size: 1.1rem; color: #475569; line-height: 1.7; margin: 0 0 3rem 0; max-width: 520px;}
.btn-row {display: flex; gap: 1rem; align-items: center;}
.btn-dark {background: #0f172a; color: white; padding: 0.9rem 2.5rem; border-radius: 1rem; font-weight: 700; font-size: 0.95rem; box-shadow: 0 10px 20px -5px rgba(15,23,42,0.3);}
.btn-light {background: white; border: 1px solid #e2e8f0; color: #64748b; padding: 0.9rem 2rem; border-radius: 1rem; font-weight: 600; font-size: 0.95rem;}

/* COUNTDOWN */
.cd-box {background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.8); border-radius: 2rem; padding: 2rem;}
.cd-header {display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;}
.cd-label {font-size: 0.65rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;}
.cd-grid {display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.5rem;}
.cd-cell {background: white; padding: 1.25rem 0.5rem; border-radius: 1.25rem; text-align: center; border: 1px solid #f1f5f9; box-shadow: 0 1px 2px rgba(0,0,0,0.04);}
.cd-val {font-size: 2.25rem; font-weight: 800; color: #1e293b; line-height: 1; margin-bottom: 0.25rem;}
.cd-unit {font-size: 0.6rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;}
.cd-footer {display: flex; justify-content: space-between; font-size: 0.6rem; font-weight: 700; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 1rem;}

/* METRICS */
.metrics-row {display: grid; grid-template-columns: repeat(4,1fr); gap: 1.5rem; margin-bottom: 3rem;}
.m-card {background: white; padding: 1.75rem; border-radius: 2rem; border: 1px solid #f1f5f9; transition: transform 0.2s;}
.m-card:hover {transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.04);}
.m-top {display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;}
.m-label {color: #64748b; font-size: 0.85rem; font-weight: 600;}
.m-icon {background: #f8fafc; padding: 0.5rem; border-radius: 0.75rem; border: 1px solid #f1f5f9; font-size: 1rem;}
.m-val {color: #0f172a; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em;}
.m-badge {display: inline-block; padding: 0.25rem 0.75rem; background: #ecfdf5; color: #059669; border-radius: 0.75rem; font-size: 0.7rem; font-weight: 700; margin-top: 0.75rem;}

/* RADIO */
div[data-testid="stRadio"] > div {flex-direction: row !important; gap: 8px !important;}
div[data-testid="stRadio"] label {background: #f1f5f9 !important; padding: 6px 18px !important; border-radius: 10px !important; font-weight: 500 !important; font-size: 0.85rem !important; color: #000000 !important;}
div[data-testid="stRadio"] label p, div[data-testid="stRadio"] label span, div[data-testid="stRadio"] label div {color: #000000 !important;}
div[data-testid="stRadio"] label[data-checked="true"] {background: #0f172a !important; color: white !important;}
div[data-testid="stRadio"] label[data-checked="true"] p, div[data-testid="stRadio"] label[data-checked="true"] span, div[data-testid="stRadio"] label[data-checked="true"] div {color: white !important;}

/* BOTTOM CARDS */
.bottom-white {background: white; padding: 2.5rem; border-radius: 2.5rem; border: 1px solid #f1f5f9; height: 100%;}
.bottom-dark {background: linear-gradient(135deg, #0f172a, #1e293b); padding: 2.5rem; border-radius: 2.5rem; color: white; height: 100%;}
.bar-track {height: 6px; background: #f1f5f9; border-radius: 999px; margin-bottom: 1.25rem; overflow: hidden;}
.bar-fill-gray {height: 100%; background: #cbd5e1; border-radius: 999px;}
.bar-fill-orange {height: 100%; background: #f97316; border-radius: 999px;}
.cycle-row {display: flex; justify-content: space-between; font-size: 0.7rem; font-weight: 700; color: #64748b; margin-bottom: 0.5rem;}
</style>
""", unsafe_allow_html=True)

# ============================
# NAVBAR + HERO (single block)
# ============================
pct_ath = ((curr_p - max_p) / max_p) * 100

st.markdown(f"""
<div class="top-nav">
    <div class="nav-left">
        <div class="nav-logo">B</div>
        <div>
            <p class="nav-title">Inteligência BTC</p>
            <p class="nav-sub">Rastreador de Halving</p>
        </div>
    </div>
    <div class="badge-live"><span class="dot"></span> Mercado Aberto</div>
</div>

<div class="hero-card">
    <div class="hero-left">
        <h1 class="hero-title">O Caminho para o<br><span class="hero-accent">Halving de 2028</span></h1>
        <p class="hero-p">A escassez do Bitcoin é matematicamente garantida. Com a emissão caindo pela metade a cada 4 anos, estamos testemunhando o desenrolar de um evento previsível de aperto monetário.</p>
        <div class="btn-row">
            <div class="btn-dark">Ver Projeções ↗</div>
            <div class="btn-light">Recompensa: <strong style="color:#0f172a">3.125 BTC</strong></div>
        </div>
    </div>
    <div class="hero-right">
        <div class="cd-box">
            <div class="cd-header">
                <span class="cd-label">TEMPO RESTANTE</span>
                <span style="color:#f97316; font-size:1.1rem;">⏱️</span>
            </div>
            <div class="cd-grid">
                <div class="cd-cell"><div class="cd-val">{days}</div><div class="cd-unit">Dias</div></div>
                <div class="cd-cell"><div class="cd-val">{hours}</div><div class="cd-unit">Horas</div></div>
                <div class="cd-cell"><div class="cd-val">{mins}</div><div class="cd-unit">Minutos</div></div>
                <div class="cd-cell"><div class="cd-val">{secs}</div><div class="cd-unit">Segundos</div></div>
            </div>
            <div class="cd-footer">
                <span>Época Atual: 5</span>
                <span>Data Est.: Abril 2028</span>
            </div>
        </div>
    </div>
</div>

<div class="metrics-row">
    <div class="m-card">
        <div class="m-top"><div class="m-label">Preço Atual</div><div class="m-icon">💰</div></div>
        <div class="m-val">${curr_p:,.0f}</div>
        <div class="m-badge">📈 Dados em Tempo Real</div>
    </div>
    <div class="m-card">
        <div class="m-top"><div class="m-label">Máxima Histórica</div><div class="m-icon">🚀</div></div>
        <div class="m-val">${max_p:,.0f}</div>
        <div class="m-badge">{pct_ath:.1f}% da Máxima</div>
    </div>
    <div class="m-card">
        <div class="m-top"><div class="m-label">Próximo Halving</div><div class="m-icon">📅</div></div>
        <div class="m-val">2028</div>
        <div class="m-badge">~{days} Dias</div>
    </div>
    <div class="m-card">
        <div class="m-top"><div class="m-label">Taxa de Emissão</div><div class="m-icon">⚡</div></div>
        <div class="m-val">0.84%</div>
        <div class="m-badge">Caindo anualmente</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================
# CHART (uses Streamlit widgets)
# ============================
st.markdown("""
<h3 style="margin:0; font-size:1.5rem; font-weight:800; color:#0f172a;">Histórico de Preço</h3>
<p style="margin:0 0 0.5rem 0; color:#64748b; font-size:0.85rem;">Fechamento Semanal (USD)</p>
""", unsafe_allow_html=True)

scale = st.radio("Escala do Gráfico", ["Logarítmica", "Linear"], horizontal=True, label_visibility="collapsed")

fig = go.Figure()

halvings = [
    {"date": "2012-11-28", "label": "Halving 2012"},
    {"date": "2016-07-09", "label": "Halving 2016"},
    {"date": "2020-05-11", "label": "Halving 2020"},
    {"date": "2024-04-19", "label": "Halving 2024"}
]
for hv in halvings:
    fig.add_vline(x=hv['date'], line_dash="dash", line_color="#f97316", opacity=0.3)
    fig.add_annotation(x=hv['date'], y=1, yref="paper", text=hv['label'],
                       showarrow=False, font={"color": "#f97316", "size": 10}, yshift=10)

fig.add_trace(go.Scatter(
    x=df['date'], y=df['price'], mode='lines',
    line={"color": '#f97316', "width": 3},
    fill='tozeroy', fillcolor='rgba(249, 115, 22, 0.06)',
    name='Bitcoin', hovertemplate='$%{y:,.0f}<extra></extra>'
))

fig.update_layout(
    yaxis_type="log" if scale == "Logarítmica" else "linear",
    template="plotly_white",
    hovermode="x unified",
    margin={"l": 0, "r": 0, "t": 20, "b": 0},
    height=500,
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis={"showgrid": False, "color": "#000000", "zeroline": False, "tickfont": {"color": "#000000", "size": 12}},
    yaxis={"gridcolor": "#f1f5f9", "color": "#000000", "tickformat": "$,", "zeroline": False, "tickfont": {"color": "#000000", "size": 12}},
    font={"color": "#000000", "family": "Inter", "size": 12}
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================
# BOTTOM INFO (using st.columns)
# ============================
st.write("")
st.write("")
b1, b2 = st.columns(2, gap="large")

with b1:
    st.markdown("""
    <div class="bottom-white">
        <h4 style="font-weight:800; color:#0f172a; margin:0 0 1rem 0; font-size:1.25rem;">Retornos Decrescentes</h4>
        <p style="color:#64748b; font-size:0.85rem; line-height:1.7; margin-bottom:1.5rem;">À medida que o Bitcoin amadurece, os ganhos percentuais explosivos diminuem. Saímos de ciclos de 7000% para ciclos mais maduros.</p>
        <div class="cycle-row"><span>CICLO 2012</span><span>+7,371%</span></div>
        <div class="bar-track"><div class="bar-fill-gray" style="width:100%"></div></div>
        <div class="cycle-row"><span>CICLO 2016</span><span>+2,785%</span></div>
        <div class="bar-track"><div class="bar-fill-gray" style="width:40%"></div></div>
        <div class="cycle-row"><span>CICLO 2020</span><span>+734%</span></div>
        <div class="bar-track"><div class="bar-fill-gray" style="width:15%"></div></div>
        <div class="cycle-row"><span>CICLO 2024 (ATUAL)</span><span>EM PROGRESSO</span></div>
        <div class="bar-track" style="margin-bottom:0"><div class="bar-fill-orange" style="width:8%"></div></div>
    </div>
    """, unsafe_allow_html=True)

with b2:
    st.markdown("""
    <div class="bottom-dark">
        <div style="background:rgba(255,255,255,0.05); width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; margin-bottom:1.5rem; font-size:1.25rem;">💹</div>
        <h4 style="font-weight:800; margin:0 0 1rem 0; font-size:1.25rem;">Projeção do Modelo (2025-2028)</h4>
        <p style="color:#94a3b8; font-size:0.85rem; line-height:1.7; margin-bottom:2.5rem;">Com base em dados históricos e regressão logarítmica, projeta-se que o ciclo atual atinja o pico entre o final de 2025 e 2026.</p>
        <div style="display:flex; align-items:baseline; gap:0.75rem; margin-bottom:2rem;">
            <span style="font-size:2.5rem; font-weight:800; color:#10b981;">$120k</span>
            <span style="color:#64748b; font-size:0.65rem; font-weight:800; text-transform:uppercase;">Alvo Conservador</span>
        </div>
        <div style="height:1px; background:rgba(255,255,255,0.08); margin-bottom:2rem;"></div>
        <div style="display:flex; align-items:baseline; gap:0.75rem;">
            <span style="font-size:2.5rem; font-weight:800; color:#f97316;">$180k</span>
            <span style="color:#64748b; font-size:0.65rem; font-weight:800; text-transform:uppercase;">Alvo Otimista</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#cbd5e1; font-size:0.75rem; font-weight:500; padding:3rem 0 1rem 0;">BTC Intelligence Dashboard © 2026</div>', unsafe_allow_html=True)
