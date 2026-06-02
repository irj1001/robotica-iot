import streamlit as st
import pandas as pd

st.title("📊 IoT Temperature Dashboard")

data = pd.read_csv("data.csv")

st.line_chart(data.set_index("timestamp")["temperature"])

st.dataframe(data.tail(20))