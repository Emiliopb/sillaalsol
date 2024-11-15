import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import time
# import geopandas as gpd
import openpyxl

st.title('Una silla al sol 🪑 ☀️')
st.subheader('Encuentra una terraza en Madrid que le esté dando el Sol.')


# Leer el archivo Excel
df_resultado_sol = pd.read_excel("./data/solysombra.xlsx")  # Suponiendo que el archivo está en el mismo directorio
gdf = pd.read_excel("./data/gdf_terraza.xlsx")
df_resultado_sol = pd.merge(df_resultado_sol, gdf[['ID_ESTABLECIMIENTO', 'lat', 'lon', 'Nombre']], on='ID_ESTABLECIMIENTO', how='left')


hora = st.slider(
    "Hora:", value=(time(11, 30), time(12, 45))
)

# Convertir la hora seleccionada en un formato adecuado
hora_inicio = hora[0].strftime("%H:%M")
hora_fin = hora[1].strftime("%H:%M")

# Filtrar las terrazas que coincidan con la hora seleccionada
df_filtrado = df_resultado_sol[(df_resultado_sol['Hora'] >= hora_inicio) & (df_resultado_sol['Hora'] <= hora_fin)]
df_filtrado = df_filtrado[df_filtrado['Soleado']==1]

chart_data_grouped = df_filtrado.groupby(['lat', 'lon', 'Nombre'])['N_MESA'].nunique().reset_index()

# Paso 2: Escalar la altura (el número de mesas distintas)
chart_data_grouped['mesas'] = chart_data_grouped['N_MESA'] 


st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=40.44, 
            longitude=-3.694968,
            zoom=13,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=chart_data_grouped,
                get_position="[lon, lat]",
                get_color="[255, 211, 0, 255]",
                get_radius=35,
                pickable=True,  # Permite seleccionar puntos en el mapa
            ),
        ],
        tooltip={
            "html": "<b>Establecimiento:</b> {Nombre} <br/> <b>Mesas:</b> {mesas}",
            "style": {
                "backgroundColor": "yellow",
                "color": "black",
                "fontSize": "14px",
                "padding": "10px",
            }
        },
    )
)
