import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar datos
df = pd.read_csv("data/alhambra_sharan_hist.csv")

# Asegurar que la columna 'date' sea datetime
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

st.title("📊 Dashboard - Análisis histórico de precios")

# ===============================
# Gráfico 1: Rango de precios por modelo
# ===============================
st.header("🔹 Rango de precios por modelo")

fig1 = px.box(df, x="title", y="price", title="Distribución de precios por modelo")
st.plotly_chart(fig1)

# ===============================
# Gráfico 2: Histórico por selección de ID
# ===============================
st.header("🔹 Evolución del precio por vehículo (ID)")

ids_disponibles = df["id"].dropna().unique().tolist()
ids_seleccionados = st.multiselect(
    "Selecciona uno o varios ID", ids_disponibles[:50], default=ids_disponibles[:3]
)

if ids_seleccionados:
    df_filtrado = df[df["id"].isin(ids_seleccionados)].sort_values(by="date")
    fig2 = px.line(
        df_filtrado,
        x="date",
        y="price",
        color="id",
        title="Histórico de precios por ID",
    )
    st.plotly_chart(fig2)
else:
    st.warning("Selecciona al menos un ID para visualizar el histórico.")

# ===============================
# Gráfico 3: Histórico de precios por modelo
# ===============================
st.header("🔹 Comparar vehículos de un mismo modelo")

titles_disponibles = df["title"].dropna().unique().tolist()
title_seleccionado = st.selectbox("Selecciona un modelo", titles_disponibles)

df_title = df[df["title"] == title_seleccionado]

if not df_title.empty:
    df_title = df_title.sort_values(by="date")
    fig3 = px.line(
        df_title,
        x="date",
        y="price",
        color="id",
        title=f"Histórico de precios - {title_seleccionado}",
    )
    st.plotly_chart(fig3)
else:
    st.warning("No hay datos disponibles para este modelo.")

# ===============================
# Vista previa
# ===============================
st.header("🔹 Vista previa del dataset")
st.dataframe(df.head())
