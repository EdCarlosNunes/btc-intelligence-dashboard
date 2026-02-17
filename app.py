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
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glass Header */
    .glass-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2.5rem;
    }

    .badge-live {
        background: #ecfdf5;
        color: #10b981;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border: 1px solid #d1fae5;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
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

    /* Hero Card Style */
    .hero-glass-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 2.5rem;
        padding: 3.5rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
        margin-bottom: 3rem;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1.05;
        color: #0f172a;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
    }

    .hero-accent {
        color: #f97316;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #475569;
        line-height: 1.6;
        max-width: 550px;
        font-weight: 500;
    }

    /* Countdown Styling - Matching React */
    .countdown-card {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 2rem;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    
    .countdown-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .countdown-item {
        background: white;
        padding: 1.25rem 0.5rem;
        border-radius: 1.25rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid rgba(241, 245, 249, 1);
    }

    .countdown-val {
        font-size: 2.25rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1;
        margin-bottom: 0.25rem;
    }

    .countdown-lab {
        font-size: 0.65rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Metrics Grid */
    .metric-card-premium {
        background: white;
        padding: 1.5rem;
        border-radius: 1.75rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s ease;
    }

    .metric-card-premium:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04);
    }
    
    .m-label { color: #64748b; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; }
    .m-value { color: #0f172a; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em; }
    .m-badge { 
        display: inline-flex; 
        align-items: center; 
        padding: 0.2rem 0.6rem; 
        background: #ecfdf5; 
        color: #059669; 
        border-radius: 0.5rem; 
        font-size: 0.75rem; 
        font-weight: 700; 
        margin-top: 0.75rem;
    }

    /* Buttons */
    .btn-main {
        background: #0f172a;
        color: white;
        padding: 0.85rem 2rem;
        border-radius: 1rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        transition: background 0.2s;
        border: none;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.2);
    }

    .btn-secondary {
        background: white;
        color: #475569;
        padding: 0.85rem 2rem;
        border-radius: 1rem;
        font-weight: 600;
        border: 1px solid #e2e8f0;
        display: inline-flex;
        align-items: center;
    }

    /* Charts Section */
    .chart-container {
        background: white;
        padding: 2.5rem;
        border-radius: 2.5rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        with open('data/btc_data.json', 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        return pd.DataFrame({'date': [datetime.now()], 'price': [0]})

df = load_data()
current_price = df['price'].iloc[-1]
ath = df['price'].max()

# --- Header ---
st.markdown("""
    <div class="glass-header">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="background: linear-gradient(135deg, #f97316, #ea580c); width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 18px; box-shadow: 0 4px 12px rgba(249, 115, 22, 0.25);">B</div>
            <div>
                <h2 style="margin:0; font-size: 1.1rem; font-weight: 800; color: #0f172a;">Inteligência BTC</h2>
                <p style="margin:0; font-size: 0.65rem; color: #94a3b8; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">Rastreador de Halving</p>
            </div>
        </div>
        <div class="badge-live">
            <span class="dot"></span>
            MERCADO ABERTO
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Hero & Countdown Section ---
# Replicating the unified card look from the localhost image
st.markdown("""<div class="hero-glass-container">""", unsafe_allow_html=True)
c1, c2 = st.columns([1.4, 1], gap="large")

with c1:
    st.markdown("""
        <div style="padding-top: 1rem;">
            <h1 class="hero-title">O Caminho para o<br><span class="hero-accent">Halving de 2028</span></h1>
            <p class="hero-subtitle">
                A escassez do Bitcoin é matematicamente garantida. Com a emissão caindo pela metade a cada 4 anos, testemunhamos um evento previsível de aperto monetário.
            </p>
            <div style="display: flex; gap: 1rem; margin-top: 3rem;">
                <div class="btn-main">Ver Projeções ↗</div>
                <div class="btn-secondary">Recompensa: <span style="color: #0f172a; margin-left: 0.5rem; font-weight: 700;">3.125 BTC</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    # Logic for countdown
    next_h = datetime(2028, 4, 1)
    diff = next_h - datetime.now()
    d, h, m, s = diff.days, diff.seconds // 3600, (diff.seconds % 3600) // 60, diff.seconds % 60
    
    st.markdown(f"""
        <div class="countdown-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.7rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">TEMPO RESTANTE</span>
                <span style="font-size: 1.1rem;">⏳</span>
            </div>
            <div class="countdown-grid">
                <div class="countdown-item"><div class="countdown-val">{d}</div><div class="countdown-lab">Dias</div></div>
                <div class="countdown-item"><div class="countdown-val">{h}</div><div class="countdown-lab">Horas</div></div>
                <div class="countdown-item"><div class="countdown-val">{m}</div><div class="countdown-lab">Min</div></div>
                <div class="countdown-item"><div class="countdown-val">{s}</div><div class="countdown-lab">Seg</div></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.65rem; font-weight: 700; color: #94a3b8; padding-top: 1rem; border-top: 1px solid #f1f5f9;">
                <span>ÉPOCA ATUAL: 5</span>
                <span>DATA EST.: ABRIL 2028</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Metrics Grid ---
st.write("")
m1, m2, m3, m4 = st.columns(4)

metrics_list = [
    {"l": "Preço Atual", "v": f"${current_price:,.0f}", "b": "📈 +2.4%", "sub": "Tempo Real"},
    {"l": "Máxima Histórica", "v": f"${ath:,.0f}", "b": f"{((current_price-ath)/ath)*100:.1f}% ATH", "sub": "Base 2024"},
    {"l": "Próximo Halving", "v": "2028", "b": "~773 Dias", "sub": "Abril"},
    {"l": "Taxa de Emissão", "v": "0.84%", "b": "Deflacionário", "sub": "Redução Anual"}
]

for idx, col in enumerate([m1, m2, m3, m4]):
    m = metrics_list[idx]
    with col:
        st.markdown(f"""
            <div class="metric-card-premium">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                    <div class="m-label">{m['l']}</div>
                    <div style="background: #f8fafc; padding: 0.4rem; border-radius: 0.75rem; border: 1px solid #f1f5f9;">
                        {'💰' if idx==0 else '📈' if idx==1 else '📅' if idx==2 else '⚡'}
                    </div>
                </div>
                <div class="m-value">{m['v']}</div>
                <div class="m-badge">{m['b']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- Chart and Bottom Sections ---
st.write("")
st.write("")
st.markdown("""<div class="chart-container">""", unsafe_allow_html=True)
st.markdown("""
    <h3 style="margin:0; font-size: 1.5rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em;">Histórico de Preço</h3>
    <p style="margin:0.25rem 0 1.5rem 0; font-size: 0.85rem; color: #64748b; font-weight: 500;">Fechamento Semanal (USD) • Escala Logarítmica</p>
""", unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['date'], y=df['price'], mode='lines',
    line=dict(color='#f97316', width=3.5),
    fill='tozeroy', fillcolor='rgba(249, 115, 22, 0.04)',
    name='BTC'
))

# Customizing tooltips and layout
fig.update_layout(
    yaxis_type="log", template="plotly_white", hovermode="x unified",
    margin=dict(l=0, r=0, t=0, b=0), height=450,
    xaxis={"showgrid": False, "color": "#94a3b8"},
    yaxis={"gridcolor": "#f1f5f9", "color": "#94a3b8", "tickformat": "$,"},
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
st.markdown("</div>", unsafe_allow_html=True)

# Bottom Info
st.write("")
st.write("")
b1, b2 = st.columns(2, gap="large")

with b1:
    st.markdown("""
        <div class="chart-container" style="padding: 2rem;">
            <h4 style="font-weight: 800; margin-bottom: 1rem;">Retornos Decrescentes</h4>
            <p style="color: #64748b; font-size: 0.85rem; line-height: 1.6; margin-bottom: 1.5rem;">
                A volatilidade e os ganhos percentuais diminuem conforme a adoção institucional cresce e o market cap aumenta.
            </p>
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748b; display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>CICLO 2012</span><span>+7,371%</span>
            </div>
            <div style="height: 6px; background: #f1f5f9; border-radius: 999px; margin-bottom: 1rem;">
                <div style="width: 100%; height: 100%; background: #cbd5e1; border-radius: 999px;"></div>
            </div>
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748b; display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>CICLO 2016</span><span>+2,785%</span>
            </div>
            <div style="height: 6px; background: #f1f5f9; border-radius: 999px; margin-bottom: 1rem;">
                <div style="width: 40%; height: 100%; background: #cbd5e1; border-radius: 999px;"></div>
            </div>
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748b; display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>CICLO 2024 (ATUAL)</span><span>EM PROGRESSO</span>
            </div>
            <div style="height: 6px; background: #f1f5f9; border-radius: 999px;">
                <div style="width: 15%; height: 100%; background: #f97316; border-radius: 999px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with b2:
    st.markdown("""
        <div style="background: #0f172a; padding: 2.5rem; border-radius: 2.5rem; color: white;">
            <div style="background: rgba(255,255,255,0.05); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">💹</div>
            <h4 style="font-weight: 800; margin-bottom: 1rem;">Projeção do Ciclo</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.6; margin-bottom: 2rem;">
                Modelos de regressão indicam o topo deste ciclo em meados de 2025.
            </p>
            <div style="display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 1.5rem;">
                <span style="font-size: 2.5rem; font-weight: 800; color: #10b981;">$120k</span>
                <span style="color: #64748b; font-size: 0.65rem; font-weight: 800; text-transform: uppercase;">Alvo Conservador</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 0.75rem;">
                <span style="font-size: 2.5rem; font-weight: 800; color: #f97316;">$180k</span>
                <span style="color: #64748b; font-size: 0.65rem; font-weight: 800; text-transform: uppercase;">Alvo Otimista</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

