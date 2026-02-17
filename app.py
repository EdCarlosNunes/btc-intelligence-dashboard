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

# --- Custom CSS for Premium Look ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: #f8fafc;
    }
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 1. White Navbar - Fixed full width */
    .nav-bar-outer {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: white;
        height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px solid #e2e8f0;
        z-index: 1000;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    
    .nav-bar-inner {
        width: 100%;
        max-width: 1200px;
        padding: 0 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .badge-live {
        background: #ecfdf5;
        color: #10b981;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border: 1px solid #d1fae5;
    }
    
    .dot {
        height: 8px;
        width: 8px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* 2. Hero Card (The white block) */
    .hero-container {
        margin-top: 100px; /* Space for navbar */
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 2.5rem;
        padding: 4rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 3rem;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        color: #0f172a;
        margin-bottom: 1.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-accent {
        color: #f97316;
    }

    .hero-p {
        font-size: 1.125rem;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 3rem;
        max-width: 500px;
    }

    /* Buttons */
    .btn-group { display: flex; gap: 1rem; align-items: center; }
    .btn-dark { background: #0f172a; color: white; padding: 1rem 2.5rem; border-radius: 1rem; font-weight: 700; box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.2); }
    .btn-light { background: white; border: 1px solid #e2e8f0; color: #64748b; padding: 1rem 2rem; border-radius: 1rem; font-weight: 600; }

    /* Countdown Styling */
    .countdown-card {
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 2rem;
        padding: 2.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    }

    .c-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0; }
    .c-item { background: white; padding: 1.5rem 0.5rem; border-radius: 1.25rem; text-align: center; border: 1px solid #f1f5f9; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .c-val { font-size: 2.5rem; font-weight: 800; color: #1e293b; line-height: 1; margin-bottom: 0.25rem; }
    .c-lab { font-size: 0.65rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }

    /* 3. Metrics Grid */
    .metric-box {
        background: white;
        padding: 1.75rem;
        border-radius: 2rem;
        border: 1px solid #f1f5f9;
        transition: all 0.2s ease;
    }
    .metric-box:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); }

    /* 4. Chart Section */
    .chart-box {
        background: white;
        padding: 3rem;
        border-radius: 2.5rem;
        border: 1px solid #f1f5f9;
        margin-top: 3rem;
    }
    
    /* Toggle styling */
    .stRadio [role="radiogroup"] {
        flex-direction: row !important;
        gap: 20px !important;
    }
    .stRadio label {
        background: #f1f5f9;
        padding: 5px 15px;
        border-radius: 8px;
        font-weight: 700 !important;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# --- Data ---
@st.cache_data
def load_data():
    try:
        with open('data/btc_data.json', 'r') as f:
            df = pd.DataFrame(json.load(f))
        df['date'] = pd.to_datetime(df['date'])
        return df
    except: return pd.DataFrame({'date': [datetime.now()], 'price': [0]})

df = load_data()
curr_p = df['price'].iloc[-1]
max_p = df['price'].max()

# --- Navbar ---
st.markdown("""
<div class="nav-bar-outer">
    <div class="nav-bar-inner">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="background: linear-gradient(135deg, #f97316, #ea580c); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 20px; box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);">B</div>
            <div>
                <h2 style="margin:0; font-size: 1.25rem; font-weight: 800; color: #0f172a;">Inteligência BTC</h2>
                <p style="margin:0; font-size: 0.65rem; color: #94a3b8; font-weight: 800; text-transform: uppercase;">Rastreador de Halving</p>
            </div>
        </div>
        <div class="badge-live"><span class="dot"></span> MERCADO ABERTO</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Hero Content ---
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
c1, c2 = st.columns([1.5, 1], gap="large")

with c1:
    st.markdown("""
        <div style="padding-top: 1rem;">
            <h1 class="hero-title">O Caminho para o<br><span class="hero-accent">Halving de 2028</span></h1>
            <p class="hero-p">
                A escassez do Bitcoin é matematicamente garantida. Com a emissão caindo pela metade a cada 4 anos, testemunhamos um evento previsível de aperto monetário.
            </p>
            <div class="btn-group">
                <div class="btn-dark">Ver Projeções ↗</div>
                <div class="btn-light">Recompensa: <span style="color:#0f172a; font-weight:700;">3.125 BTC</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    nh = datetime(2028, 4, 1)
    diff = nh - datetime.now()
    d, h, m, s = diff.days, diff.seconds // 3600, (diff.seconds % 3600) // 60, diff.seconds % 60
    st.markdown(f"""
        <div class="countdown-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.7rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">TEMPO RESTANTE</span>
                <span style="color:#f97316; font-size:1.2rem;">⏱️</span>
            </div>
            <div class="c-grid">
                <div class="c-item"><div class="c-val">{d}</div><div class="c-lab">Dias</div></div>
                <div class="c-item"><div class="c-val">{h}</div><div class="c-lab">Horas</div></div>
                <div class="c-item"><div class="c-val">{m}</div><div class="c-lab">Minutos</div></div>
                <div class="c-item"><div class="c-val">{s}</div><div class="c-lab">Segundos</div></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.65rem; font-weight: 700; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 1.5rem;">
                <span>ÉPOCA ATUAL: 5</span>
                <span>DATA EST.: ABRIL 2028</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Metrics Grid ---
m_cols = st.columns(4)
metrics = [
    {"tit": "Preço Atual", "val": f"${curr_p:,.0f}", "bdg": "📈 +2.4%", "ico": "💰"},
    {"tit": "Máxima Histórica", "val": f"${max_p:,.0f}", "bdg": f"{((curr_p-max_p)/max_p)*100:.1f}% ATH", "ico": "🚀"},
    {"tit": "Próximo Halving", "val": "2028", "bdg": "~773 Dias", "ico": "📅"},
    {"tit": "Taxa de Emissão", "val": "0.84%", "bdg": "Deflacionário", "ico": "⚡"}
]

for idx, col in enumerate(m_cols):
    m = metrics[idx]
    with col:
        st.markdown(f"""
            <div class="metric-box">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                    <div style="color: #64748b; font-size: 0.85rem; font-weight: 600;">{m['tit']}</div>
                    <div style="background: #f8fafc; padding: 0.5rem; border-radius: 0.75rem; border: 1px solid #f1f5f9;">{m['ico']}</div>
                </div>
                <div style="color: #0f172a; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em;">{m['val']}</div>
                <div style="display: inline-block; padding: 0.2rem 0.6rem; background: #ecfdf5; color: #059669; border-radius: 0.5rem; font-size: 0.7rem; font-weight: 700; margin-top: 0.75rem;">{m['bdg']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- Chart Section ---
st.markdown('<div class="chart-box">', unsafe_allow_html=True)
hdr_c1, hdr_c2 = st.columns([2, 1])

with hdr_c1:
    st.markdown("""
        <h3 style="margin:0; font-size: 1.5rem; font-weight: 800; color: #0f172a;">Histórico de Preço</h3>
        <p style="margin:0; color: #64748b; font-size: 0.85rem; font-weight: 500;">Fechamento Semanal (USD) • Selecione a escala abaixo</p>
    """, unsafe_allow_html=True)

with hdr_c2:
    scale_type = st.radio("Escala", ["LOGARÍTMICA", "LINEAR"], horizontal=True, label_visibility="collapsed")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['date'], y=df['price'], mode='lines',
    line=dict(color='#f97316', width=4),
    fill='tozeroy', fillcolor='rgba(249, 115, 22, 0.05)',
    name='Bitcoin'
))

fig.update_layout(
    yaxis_type="log" if scale_type == "LOGARÍTMICA" else "linear",
    template="plotly_white",
    hovermode="x unified",
    margin=dict(l=0, r=0, t=20, b=0),
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis={"showgrid": False, "color": "#94a3b8", "zeroline": False},
    yaxis={"gridcolor": "#f1f5f9", "color": "#94a3b8", "tickformat": "$,", "zeroline": False}
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div style="text-align: center; margin-top: 5rem; color: #cbd5e1; font-size: 0.8rem; font-weight: 500;">BTC Intelligence Dashboard • © 2026 • Dados via API Pública</div>', unsafe_allow_html=True)
