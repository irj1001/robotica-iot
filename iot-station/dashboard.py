import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="IoT Smart Desk Station",
    layout="wide"
)

st.title("📊 IoT Smart Desk Station")

# =========================
# CARGAR DATOS
# =========================

if not os.path.exists("data.csv"):
    st.warning("No existe data.csv todavía")
    st.stop()

data = pd.read_csv("data.csv")

if len(data) == 0:
    st.warning("No hay datos")
    st.stop()

# convertir timestamp
try:
    data["timestamp"] = pd.to_datetime(data["timestamp"])
except:
    pass

# =========================
# MÉTRICAS
# =========================

latest = data.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌡 Temperatura",
        f"{latest['temperature']:.2f} °C"
    )

with col2:
    st.metric(
        "📄 Muestras",
        len(data)
    )

with col3:
    st.metric(
        "⏰ Última lectura",
        str(latest["timestamp"])
    )

with col4:
    st.metric(
        "📡 Estado",
        "ONLINE"
    )

st.divider()

# =========================
# GRÁFICO PRINCIPAL
# =========================

st.subheader("🌡 Historial de temperatura")

chart_data = data.set_index("timestamp")

st.line_chart(chart_data["temperature"])

# =========================
# ESTADÍSTICAS
# =========================

st.subheader("📈 Estadísticas")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Mínima",
        f"{data['temperature'].min():.2f} °C"
    )

with c2:
    st.metric(
        "Media",
        f"{data['temperature'].mean():.2f} °C"
    )

with c3:
    st.metric(
        "Máxima",
        f"{data['temperature'].max():.2f} °C"
    )

st.divider()

# =========================
# ÚLTIMAS LECTURAS
# =========================

st.subheader("🧾 Últimas lecturas")

st.dataframe(
    data.tail(20),
    use_container_width=True
)

# =========================
# FUTUROS SENSORES
# =========================

st.subheader("🚀 Sensores futuros")

future_cols = st.columns(3)

with future_cols[0]:
    st.info("💧 Humedad (DHT22)")

with future_cols[1]:
    st.info("☀️ Luz (BH1750)")

with future_cols[2]:
    st.info("📺 OLED SSD1306")