import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Météo Dashboard", page_icon="🌤️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Outfit:wght@700;800&display=swap');
    html, body, [class*="css"] { font-family: 'IBM Plex Mono', monospace; background-color: #f0f4f8; color: #1a2332; }
    .main { background-color: #f0f4f8; }
    .block-container { padding: 2rem 3rem; }
    .metric-card { background: white; border: 2px solid #dde8f0; border-radius: 16px; padding: 1.2rem 1.5rem; text-align: center; box-shadow: 0 2px 12px rgba(0,80,180,0.07); }
    .metric-label { font-size: 0.7rem; letter-spacing: 0.15em; color: #2266cc; text-transform: uppercase; margin-bottom: 0.4rem; font-weight: 600; }
    .metric-value { font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; color: #1a2332; }
    .metric-unit { font-size: 0.75rem; color: #2266cc; margin-top: 0.2rem; }
    .section-title { font-family: 'Outfit', sans-serif; font-size: 0.85rem; letter-spacing: 0.2em; color: #2266cc; text-transform: uppercase; margin: 2rem 0 0.5rem 0; border-left: 4px solid #2266cc; padding-left: 0.8rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──
engine = create_engine("sqlite:///meteo.db")
df = pd.read_sql("SELECT * FROM meteo", engine)
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.drop_duplicates(subset=["datetime", "city"]).sort_values("datetime")

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 🌍 Configuration")
    cities = df["city"].unique().tolist()
    city = st.selectbox("Ville", cities)
    st.markdown("---")
    df_city = df[df["city"] == city]
    st.markdown("### 📊 À propos")
    st.markdown(f"**{len(df_city)}** prévisions chargées")
    st.markdown(f"Du **{df_city['datetime'].min().strftime('%d %b')}** au **{df_city['datetime'].max().strftime('%d %b')}**")

# ── FILTRE ──
df = df[df["city"] == city]

# ── HEADER ──
st.markdown(f"""
<div style='margin-bottom:2rem'>
    <div style='font-family:Outfit,sans-serif;font-size:2.4rem;font-weight:800;color:#1a2332;line-height:1'>
        🌤️ Météo Pipeline
    </div>
    <div style='color:#2266cc;font-size:0.85rem;letter-spacing:0.15em;margin-top:0.4rem;font-weight:600'>
        {city.upper()} · PRÉVISIONS 5 JOURS · Mise à jour toutes les 3h
    </div>
</div>
""", unsafe_allow_html=True)

# ── MÉTRIQUES ──
latest = df.iloc[-1]
col1, col2, col3, col4 = st.columns(4)
metrics = [
    (col1, "🌡️ Température", f"{latest['temp']:.1f}", "°C"),
    (col2, "💧 Humidité", f"{latest['humidity']:.0f}", "%"),
    (col3, "💨 Vent", f"{latest['windspeed']:.1f}", "m/s"),
    (col4, "❄️ Temp. min", f"{df['temp_min'].min():.1f}", "°C min"),
]
for col, label, value, unit in metrics:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{value}</div>
            <div class='metric-unit'>{unit}</div>
        </div>
        """, unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor="white", plot_bgcolor="#f8fafd",
    font=dict(family="IBM Plex Mono", color="#1a2332", size=12),
    legend=dict(bgcolor="white", bordercolor="#dde8f0", borderwidth=1, font=dict(size=13, color="#1a2332")),
    margin=dict(l=10, r=10, t=20, b=10),
    xaxis=dict(gridcolor="#dde8f0", showline=True, linecolor="#dde8f0", tickfont=dict(size=12, color="#1a2332")),
    yaxis=dict(gridcolor="#dde8f0", showline=True, linecolor="#dde8f0", tickfont=dict(size=12, color="#1a2332")),
)

# ── TEMPÉRATURES ──
st.markdown("<div class='section-title'>Évolution des températures</div>", unsafe_allow_html=True)
fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=df["datetime"], y=df["temp_max"], name="Max", fill=None, line=dict(color="#e05252", width=2)))
fig_temp.add_trace(go.Scatter(x=df["datetime"], y=df["temp_min"], name="Min", fill="tonexty", fillcolor="rgba(224,82,82,0.08)", line=dict(color="#38b2ac", width=2)))
fig_temp.add_trace(go.Scatter(x=df["datetime"], y=df["temp"], name="Moyenne", line=dict(color="#2266cc", width=3)))
fig_temp.update_layout(**PLOT_LAYOUT, height=320)
fig_temp.update_yaxes(title="°C")
st.plotly_chart(fig_temp, use_container_width=True)

# ── HUMIDITÉ + VENT ──
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='section-title'>Humidité</div>", unsafe_allow_html=True)
    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(x=df["datetime"], y=df["humidity"], fill="tozeroy", fillcolor="rgba(56,178,172,0.12)", line=dict(color="#38b2ac", width=2.5), name="Humidité"))
    fig_hum.update_layout(**PLOT_LAYOUT, height=280, showlegend=False)
    fig_hum.update_yaxes(title="%")
    st.plotly_chart(fig_hum, use_container_width=True)

with col_right:
    st.markdown("<div class='section-title'>Vitesse du vent</div>", unsafe_allow_html=True)
    fig_wind = go.Figure()
    fig_wind.add_trace(go.Bar(x=df["datetime"], y=df["windspeed"], name="Vent",
        marker=dict(color=df["windspeed"], colorscale="Blues", showscale=True,
                    colorbar=dict(title="m/s", tickfont=dict(size=11, color="#1a2332")))))
    fig_wind.update_layout(**PLOT_LAYOUT, height=280, showlegend=False)
    fig_wind.update_yaxes(title="m/s")
    st.plotly_chart(fig_wind, use_container_width=True)