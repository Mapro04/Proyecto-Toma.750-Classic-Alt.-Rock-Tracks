import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Leer los datos desde una URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS1mWfrFogi-NQa0h1h6GrG71R0t3jAbHpjh90VWMBVPaNJINcTdt4t2Fm2tKni2PFRAUWixAhod6EV/pub?gid=1390347138&single=true&output=csv"

# Cargar los datos en un DataFrame
@st.cache
def load_data():
    df = pd.read_csv(url)
    return df

data = load_data()

# Conexión a SQLite
conn = sqlite3.connect("database.db")
data.to_sql("data_table", conn, if_exists="replace", index=False)
df_from_db = pd.read_sql_query("SELECT * FROM data_table", conn)

# Interfaz de Streamlit
st.title("Análisis de Datos 750 Classic Alt. Rock Tracks con Gráficos")

# Mostrar la tabla de datos
st.subheader("Tabla de Datos presentada por Martin Acosta, Diego Triana y Andres Jacome")
st.dataframe(df_from_db)

# Mostrar estadísticas descriptivas
st.subheader("Estadísticas Descriptivas")
st.table(df_from_db.describe())

# Filtros
st.sidebar.header("Filtros")
artista_seleccionado = st.sidebar.multiselect(
    "Seleccionar Artista(s):",
    options=df_from_db["Artist"].unique(),
    default=df_from_db["Artist"].unique()
)
df_filtrado = df_from_db[df_from_db["Artist"].isin(artista_seleccionado)]

# Gráfico 1: Popularidad promedio por Artista
st.subheader("Popularidad Promedio por Artista")
fig1, ax1 = plt.subplots(figsize=(10, 6))
grouped_data = df_filtrado.groupby("Artist")["Popularity"].mean()
grouped_data.plot(kind="bar", ax=ax1, color="#4682B4")
ax1.set_title("Popularidad Promedio por Artista", fontsize=14, color="navy")
ax1.set_xlabel("Artista", fontsize=12)
ax1.set_ylabel("Popularidad Promedio", fontsize=12)
st.pyplot(fig1)

# Gráfico 2: Popularidad vs. Track
st.subheader("Relación entre Track y Popularidad")
fig2, ax2 = plt.subplots(figsize=(12, 6))
df_filtrado.plot.scatter(x="Track", y="Popularity", c="blue", alpha=0.7, ax=ax2)
ax2.set_title("Popularidad vs. Track", fontsize=14, color="navy")
ax2.set_xlabel("Track", fontsize=12)
ax2.set_ylabel("Popularidad", fontsize=12)
st.pyplot(fig2)

# Gráfico 3: Distribución de Popularidad por Artista
st.subheader("Distribución de Popularidad por Artista")
fig3, ax3 = plt.subplots(figsize=(12, 6))
df_filtrado.boxplot(column="Popularity", by="Artist", grid=False, ax=ax3, patch_artist=True)
ax3.set_title("Distribución de Popularidad por Artista", fontsize=14, color="navy")
ax3.set_xlabel("Artista", fontsize=12)
ax3.set_ylabel("Popularidad", fontsize=12)
plt.suptitle("")  # Elimina el título adicional del boxplot
st.pyplot(fig3)
