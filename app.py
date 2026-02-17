import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from datetime import datetime
import time

# --- Page Config ---
st.set_page_config(
    page_title="Inteligência BTC | Rastreador de Halving",
    page_icon="₿",
    layout="wide",
)

# --- Custom CSS for Premium Look ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    /* Metrics Card Styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-title {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }
    
    /* Countdown Styling */
    .countdown-container {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.6);
        text-align: center;
    }
    
    .countdown-unit {
        background: white;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .countdown-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1e293b;
    }
    
    .countdown-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
    }
    
    /* Hero Section */
    .hero-text {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        color: #0f172a;
    }
    
    .hero-accent {
        background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Section containers */
    .content-section {
        background: white;
        padding: 2rem;
        border-radius: 2rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    with open('data/btc_data.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_data()
    current_price = df['price'].iloc[-1]
    ath = df['price'].max()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# --- Helpers ---
def get_countdown():
    next_halving = datetime(2028, 4, 1)
    diff = next_halving - datetime.now()
    return {
        "Dias": diff.days,
        "Horas": diff.seconds // 3600,
        "Minutos": (diff.seconds % 3600) // 60,
        "Segundos": diff.seconds % 60
    }

# --- Sidebar / Header ---
st.markdown("""
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
        <div style="background: linear-gradient(135deg, #f97316, #ea580c); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">B</div>
        <div>
            <h1 style="margin:0; font-size: 24px; color: #1e293b;">Inteligência BTC</h1>
            <p style="margin:0; font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">Rastreador de Halving</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Hero Section ---
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown(f"""
        <div style="margin-top: 2rem;">
            <p class="hero-text">O Caminho para o <br><span class="hero-accent">Halving de 2028</span></p>
            <p style="font-size: 1.125rem; color: #475569; margin-top: 1.5rem; max-width: 500px; line-height: 1.6;">
                A escassez do Bitcoin é matematicamente garantida. Com a emissão caindo pela metade a cada 4 anos, estamos testemunhando o desenrolar de um evento previsível de aperto monetário.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="display: flex; gap: 1rem; margin-top: 2rem;">
            <div style="padding: 0.75rem 2rem; background: #0f172a; color: white; border-radius: 1rem; font-weight: 600;">Ver Projeções</div>
            <div style="padding: 0.75rem 2rem; background: white; border: 1px solid #e2e8f0; color: #64748b; border-radius: 1rem; font-weight: 600;">Recompensa: <span style="color: #0f172a;">3.125 BTC</span></div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    countdown = get_countdown()
    st.markdown("""
        <div class="countdown-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <span style="font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Tempo Restante</span>
                <span style="color: #f97316;">⏱️</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, (label, val) in enumerate(countdown.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="countdown-unit">
                    <div class="countdown-value">{val}</div>
                    <div class="countdown-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("""
            </div>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 600; color: #94a3b8;">
                <span>ÉPOCA ATUAL: 5</span>
                <span>DATA EST.: ABRIL 2028</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer
st.write("")

# --- Metrics Grid ---
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

metrics = [
    {"label": "Preço Atual", "value": f"${current_price:,.2f}", "trend": "📈 +2.4%", "color": "#f97316"},
    {"label": "Máxima Histórica", "value": f"${ath:,.2f}", "trend": f"{((current_price-ath)/ath)*100:.1f}% da Máxima", "color": "#f97316"},
    {"label": "Próximo Halving", "value": "2028", "trend": "~780 Dias", "color": "#f97316"},
    {"label": "Taxa de Emissão", "value": "0.84%", "trend": "Caindo anualmente", "color": "#f97316"}
]

for idx, col in enumerate([m_col1, m_col2, m_col3, m_col4]):
    m = metrics[idx]
    with col:
        st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div class="metric-title">{m['label']}</div>
                        <div class="metric-value">{m['value']}</div>
                    </div>
                </div>
                <div style="margin-top: 1rem; font-size: 0.875rem; font-weight: 600; color: #10b981; background: #ecfdf5; padding: 0.25rem 0.75rem; border-radius: 1rem; display: inline-block;">
                    {m['trend']}
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("")
st.write("")

# --- Chart Section ---
st.markdown("""
    <div class="content-section">
        <h3 style="margin:0; font-size: 1.5rem; font-weight: 700; color: #1e293b;">Histórico de Preço</h3>
        <p style="margin:0; font-size: 0.875rem; color: #64748b; font-weight: 500;">Fechamento Semanal (USD) • Selecione o modo de escala abaixo</p>
""", unsafe_allow_html=True)

scale_mode = st.radio("Escala do Gráfico", ["Logarítmica", "Linear"], horizontal=True, label_visibility="collapsed")

fig = go.Figure()

# Halving Dates
halvings = [
    {"date": "2012-11-28", "label": "2012"},
    {"date": "2016-07-09", "label": "2016"},
    {"date": "2020-05-11", "label": "2020"},
    {"date": "2024-04-19", "label": "2024"}
]

for h in halvings:
    fig.add_vline(x=h['date'], line_dash="dash", line_color="#f97316", opacity=0.3)
    fig.add_annotation(x=h['date'], y=1, yref="paper", text=h['label'], showarrow=False, font=dict(color="#f97316", size=10))

fig.add_trace(go.Scatter(
    x=df['date'], 
    y=df['price'],
    mode='lines',
    line=dict(color='#f97316', width=3),
    fill='tozeroy',
    fillcolor='rgba(249, 115, 22, 0.05)',
    name='Preço BTC'
))

fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    yaxis_type="log" if scale_mode == "Logarítmica" else "linear",
    template="plotly_white",
    hovermode="x unified",
    margin=dict(l=0, r=0, t=20, b=0),
    height=500,
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.write("")

# --- Info Section ---
i_col1, i_col2 = st.columns(2, gap="large")

with i_col1:
    st.markdown("""
        <div class="content-section">
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #1e293b; margin-bottom: 1rem;">Retornos Decrescentes</h3>
            <p style="color: #64748b; font-size: 0.875rem; line-height: 1.6; margin-bottom: 1.5rem;">
                À medida que o Bitcoin amadurece, os ganhos percentuais explosivos diminuem. Saímos de ciclos de 7000% para ciclos mais maduros de 700%.
            </p>
    """, unsafe_allow_html=True)
    
    data = [
        {"Ciclo": "Ciclo 2012", "Crescimento": "7,371%", "Progress": 100},
        {"Ciclo": "Ciclo 2016", "Crescimento": "2,785%", "Progress": 40},
        {"Ciclo": "Ciclo 2020", "Crescimento": "734%", "Progress": 15},
        {"Ciclo": "Ciclo 2024", "Crescimento": "Em Progresso", "Progress": 5}
    ]
    
    for item in data:
        st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700; color: #64748b; margin-bottom: 0.25rem;">
                    <span>{item['Ciclo']}</span>
                    <span>{item['Crescimento']}</span>
                </div>
                <div style="height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden;">
                    <div style="width: {item['Progress']}%; height: 100%; background: {'#f97316' if item['Crescimento'] == 'Em Progresso' else '#cbd5e1'}; border-radius: 4px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with i_col2:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 2rem; border-radius: 2rem; color: white;">
            <div style="background: rgba(255,255,255,0.1); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">💹</div>
            <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem;">Projeção do Modelo (2025-2028)</h3>
            <p style="color: #94a3b8; font-size: 0.875rem; line-height: 1.6; margin-bottom: 2rem;">
                Com base em dados históricos e regressão logarítmica, projeta-se que o ciclo atual atinja o pico entre o final de 2025 e 2026.
            </p>
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div style="font-size: 2.5rem; font-weight: 800; color: #10b981;">$120k</div>
                <div style="font-size: 0.75rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; line-height: 1.2;">Alvo<br>Conservador</div>
            </div>
            <div style="height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 1.5rem;"></div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2.5rem; font-weight: 800; color: #f97316;">$180k</div>
                <div style="font-size: 0.75rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; line-height: 1.2;">Alvo<br>Otimista</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
