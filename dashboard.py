from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st
import yagmail


@st.cache_data
def obtener_fecha_ultimo_envio():
    return None  # Por defecto no hay nada almacenado


@st.cache_data
def registrar_envio(fecha_actual: str):
    return fecha_actual


def enviar_alerta_email(alertas_precio, destinatario=None):
    if not alertas:
        return

    hoy = datetime.today().strftime("%Y-%m-%d")
    ultima_fecha = obtener_fecha_ultimo_envio()

    if ultima_fecha == hoy:
        return  # Ya se envió hoy

    user = st.secrets["email"]["user"]
    password = st.secrets["email"]["password"]
    destinatario = destinatario or user  # si no se especifica, se envía a uno mismo

    yag = yagmail.SMTP(user=user, password=password)

    cuerpo = "🚨 Alerta de bajada de precios:\n\n"
    for alerta_precio in alertas_precio:
        cuerpo += (
            f"- ID {alerta_precio['id']} ({alerta_precio['title']}): "
            f"de {alerta_precio['precio_inicial']:.0f} € a {alerta_precio['precio_final']:.0f} € "
            f"({abs(alerta_precio['variacion'])}%)\n"
        )

    yag.send(to=destinatario, subject="🚨 Bajada de precio detectada", contents=cuerpo)
    # Guardar la fecha actual como último envío
    registrar_envio(hoy)


# Manejo de actualización
if "actualizado" not in st.session_state:
    st.session_state.actualizado = False

if st.button("🔄 Actualizar datos"):
    st.session_state.actualizado = True
    st.rerun()

# Mostrar mensaje si se ha actualizado
if st.session_state.actualizado:
    st.success("✅ Datos actualizados correctamente")
    st.session_state.actualizado = False  # reset tras mostrar

# Cargar datos
df = pd.read_csv("data/alhambra_sharan_hist.csv")

# Asegurar que la columna 'date' sea datetime
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

st.header("🔔 Alertas de bajadas de precio")

# Filtrar para tener solo registros válidos por ID con fecha
df_valid = df.dropna(subset=["id", "date", "price"])

# Asegurarnos de que está ordenado por fecha
df_valid = df_valid.sort_values(by=["id", "date"])

# Agrupar por ID y obtener precios iniciales y finales
alertas = []
for veh_id, group in df_valid.groupby("id"):
    if len(group) < 2:
        continue  # Necesitamos al menos 2 precios para comparar
    precio_inicial = group.iloc[0]["price"]
    precio_final = group.iloc[-1]["price"]

    if precio_inicial > 0:
        variacion = (precio_final - precio_inicial) / precio_inicial
        if variacion <= -0.10:
            alerta = {
                "id": veh_id,
                "title": group.iloc[-1]["title"],
                "precio_inicial": precio_inicial,
                "precio_final": precio_final,
                "variacion": round(variacion * 100, 2),
            }
            alertas.append(alerta)

# ===============================
# Nuevos vehículos añadidos esta semana
# ===============================
last_week = datetime.today() - timedelta(days=7)

new_car_ids = []  # Initialize with an empty list in case 'date' column is missing
# Filter new cars added since last week and keep only the most recent row for each car
if "date" in df.columns:
    new_cars = df[df["date"] >= last_week]
    new_cars = new_cars.sort_values(by="date", ascending=False).drop_duplicates(
        subset="id", keep="first"
    )
    new_car_ids = new_cars["id"].unique()

# Display new cars added since last week
st.header("🆕 Nuevos vehículos añadidos esta semana")
if len(new_car_ids) > 0:
    st.write(f"Se han añadido {len(new_car_ids)} nuevos vehículos al dataset:")
    st.dataframe(new_cars)
else:
    st.success("✅ No se han añadido nuevos vehículos al dataset esta semana.")

# Mostrar alertas
if alertas:
    for a in alertas:
        st.warning(
            f"🚨 El vehículo ID `{a['id']}` ({a['title']}) ha bajado un **{abs(a['variacion'])}%**: "
            f"de {a['precio_inicial']:.0f} € a {a['precio_final']:.0f} €"
        )
    # enviar_alerta_email(alertas)
else:
    st.success("✅ No hay bajadas de precio significativas (≥10%) en este momento.")

st.title("📊 Dashboard - Análisis histórico de precios")

# ===============================
# Gráfico 1: Rango de precios por modelo
# ===============================
st.header("🔹 Rango de precios por modelo")

fig1 = px.box(df, x="title", y="price", title="Distribución de precios por modelo")
st.plotly_chart(fig1)

# ===============================
# Gráfico 2: Histórico de precios por modelo
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
# Gráfico 3: Histórico por selección de ID
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
# Vista previa
# ===============================
st.header("🔹 Vista previa del dataset")
st.dataframe(df.head())
