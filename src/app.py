import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import json
import dash
from dash import dcc, html, dash_table 
from pathlib import Path

colores_paleta = [
    '#113250', '#F7A800', '#002D72', '#FF8200', '#5C068C', '#00B388', 
    '#717C7D', '#2D95B8', '#FF4C00', '#00A3E0', '#FFDC00', '#1F3A68', 
    '#FF9D00', '#3C6A94', '#FF6A13', '#004B6F', '#E10B0B', '#7B87A1', 
    '#F0A400', '#4286F4', '#FF5800', '#1C8D9B', '#008B3E', '#E6B100', 
    '#B1495C', '#7A96D9', '#6E74B0', '#F1B31C', '#D93E40', '#6C89B5', 
    '#A59C16', '#5E66A5', '#0F2D4A', '#D27A00', '#FF7F4F'
]

#------------------------------------------------------------
# 1. CARGAR DATA
#------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent      # carpeta donde está backend_dashboard.py
DATA_DIR = BASE_DIR / "Data"

# Cargar el GeoJSON de Colombia desde el archivo proporcionado
with open(DATA_DIR / "geojson_colombia.json", encoding="utf-8") as f:
    geojson_data = json.load(f)

# Cargar los datos de muertes y coordenadas
no_fetal_data = pd.read_excel(DATA_DIR / "Anexo1.NoFetal2019_CE_15-03-23.xlsx")
divipola_data = pd.read_excel(DATA_DIR / "Anexo3.Divipola_CE_15-03-23.xlsx")
divipola_departamentos_data = pd.read_excel(DATA_DIR / "DIVIPOLA_Departamentos.xlsx")

#------------------------------------------------------------
# 2. FUNCIONES
#------------------------------------------------------------

# Función para contar muertes por columnas y renombrar
def contar_muertes(df, group_columns, count_column, new_name):
    result = df.groupby(group_columns)[count_column].count().reset_index()
    result.rename(columns={count_column: new_name}, inplace=True)
    return result

#------------------------------------------------------------
# 2. TRANSFORMACIÓN DE LA DATA
#------------------------------------------------------------

# Agrupar los datos de muertes por COD_DEPARTAMENTO y MES
muertes_departamento_mes = contar_muertes(no_fetal_data, ['COD_DEPARTAMENTO', 'MES'], 'COD_MUERTE', 'TOTAL_MUERTES_POR_MES_Y_DPTO')
muertes_departamento_mes = muertes_departamento_mes.sort_values(by=['COD_DEPARTAMENTO', 'MES'])

# Contar las muertes por departamento (sin considerar el mes)
muertes_departamento = contar_muertes(no_fetal_data, ['COD_DEPARTAMENTO'], 'COD_MUERTE', 'TOTAL_MUERTES_POR_DPTO')

# Contar las muertes por municipio y manera de muerte
muertes_municipio = contar_muertes(no_fetal_data, ['COD_DEPARTAMENTO','COD_MUNICIPIO', 'MANERA_MUERTE'], 'COD_MUERTE', 'TOTAL_MANERA_DE_MUERTE')

# Contar las muertes por municipio

total_muertes_municipio = contar_muertes(no_fetal_data, ['COD_DEPARTAMENTO','COD_MUNICIPIO'], 'COD_MUERTE', 'TOTAL_MUERTES_POR_MUNICIPIO')

# Crear un mapeo único entre COD_DEPARTAMENTO y COD_MUNICIPIO a MUNICIPIO
divipola_data['COD_DEPARTAMENTO_COD_MUNICIPIO'] = divipola_data['COD_DEPARTAMENTO'].astype(str) + divipola_data['COD_MUNICIPIO'].astype(str)
muertes_municipio['COD_DEPARTAMENTO_COD_MUNICIPIO'] = muertes_municipio['COD_DEPARTAMENTO'].astype(str) + muertes_municipio['COD_MUNICIPIO'].astype(str)
total_muertes_municipio['COD_DEPARTAMENTO_COD_MUNICIPIO'] = total_muertes_municipio['COD_DEPARTAMENTO'].astype(str) + total_muertes_municipio['COD_MUNICIPIO'].astype(str)

# Ahora, mapeamos correctamente MUNICIPIO usando ambos códigos
divipola_data['MUNICIPIO'] = divipola_data['COD_DEPARTAMENTO_COD_MUNICIPIO'].map(lambda x: divipola_data[divipola_data['COD_DEPARTAMENTO_COD_MUNICIPIO'] == x]['MUNICIPIO'].values[0])

# Unir los datos de muertes con la información de departamentos
divipola_data = divipola_data.merge(divipola_departamentos_data, on='DEPARTAMENTO', how='inner').drop('COD_DEPARTAMENTO_y', axis=1)
divipola_data.rename(columns={'COD_DEPARTAMENTO_x': 'COD_DEPARTAMENTO'}, inplace=True)


# Unir los datos de muertes por mes y por departamento
data_final = muertes_departamento_mes.merge(muertes_departamento, on='COD_DEPARTAMENTO', how='inner')\
                                     .merge(divipola_data, on='COD_DEPARTAMENTO', how='inner')\
                                     .merge(muertes_municipio, on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'], how='inner')\
                                     .merge(total_muertes_municipio, on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'], how='inner')

# Eliminar columnas innecesarias después del merge
data_final = data_final.drop(columns=['FECHA1erFIS','COD_DANE'])

# Asegurarnos de que las coordenadas estén en formato numérico correcto
data_final[['LATITUD', 'LONGITUD']] = data_final[['LATITUD', 'LONGITUD']].apply(lambda x: pd.to_numeric(x.str.replace(',', '.', regex=False), errors='coerce'))

# Crear un diccionario de depcodigo a nombre de departamento
geojson_depcodigo = {feature['properties']['DPTO']: feature['properties']['NOMBRE_DPT'] for feature in geojson_data['features']}

# Asegurarse de que 'COD_DEPARTAMENTO' esté en formato cadena con ceros a la izquierda si es necesario
data_final['COD_DEPARTAMENTO'] = data_final['COD_DEPARTAMENTO'].astype(str).str.zfill(2)

# Realizar el mapeo entre 'COD_DEPARTAMENTO' y 'geojson_depcodigo'
data_final['DEPARTAMENTO'] = data_final['COD_DEPARTAMENTO'].map(geojson_depcodigo)

# Eliminar duplicados
data_final = data_final.drop_duplicates(subset=['MUNICIPIO', 'MANERA_MUERTE', 'COD_MUNICIPIO','MES'])

# Se elimina la columna mes con el fin de evitanr la duplicación de los mismos municipios y maneras de muerte por cada mes
data_final_sin_mes = data_final.drop_duplicates(subset=['MUNICIPIO', 'MANERA_MUERTE', 'COD_MUNICIPIO'])
muertes_por_municipio = data_final_sin_mes.groupby(['DEPARTAMENTO', 'MUNICIPIO'], as_index=False)['TOTAL_MANERA_DE_MUERTE'].sum()

# Filtrar las 5 ciudades con más muertes
top_5_municipios = muertes_por_municipio.sort_values(by='TOTAL_MANERA_DE_MUERTE', ascending=False).head(5)

# Filtrar los datos de muertes por municipio y manera para las 5 ciudades más violentas
top_5_data = data_final_sin_mes[data_final_sin_mes['MUNICIPIO'].isin(top_5_municipios['MUNICIPIO'])]

# Ahora agrupar por MUNICIPIO y MANERA_MUERTE para obtener el total de muertes por manera de muerte
top_5_data_agrupada = top_5_data.groupby(['MUNICIPIO', 'MANERA_MUERTE'], as_index=False)['TOTAL_MANERA_DE_MUERTE'].sum()

# Ordenar para obtener las 10 ciudades con menos muertes
top_10_municipios_menor_muerte = muertes_por_municipio.sort_values(by='TOTAL_MANERA_DE_MUERTE', ascending=False).tail(10)

#------------------------------------------------------------
# 3. GRAFICOS
#------------------------------------------------------------
#------------------------------------------------------------
# 3.1 Gráfico de barras apiladas
#------------------------------------------------------------
fig_top5 = go.Figure()

# Añadir una traza por cada MANERA_MUERTE
for i, manera_muerte in enumerate(top_5_data_agrupada['MANERA_MUERTE'].unique()):
    filtered_data = top_5_data_agrupada[top_5_data_agrupada['MANERA_MUERTE'] == manera_muerte]
    fig_top5.add_trace(go.Bar(
        y=filtered_data['MUNICIPIO'],  # Los municipios estarán en el eje Y
        x=filtered_data['TOTAL_MANERA_DE_MUERTE'],  # El total de muertes estará en el eje X
        name=manera_muerte,  # El nombre de la manera de muerte será la categoría de las barras
        orientation='h',  # Barra horizontal
        marker=dict(color=colores_paleta[i])  # Asignar colores personalizados
    ))

# Calcular el total de muertes por municipio (suma de todas las maneras de muerte)
total_muertes_por_municipio = top_5_data_agrupada.groupby('MUNICIPIO')['TOTAL_MANERA_DE_MUERTE'].sum().reset_index()

# Añadir los totales de muertes al final de las barras (en el eje X)
for municipio in total_muertes_por_municipio['MUNICIPIO']:
    total_muerte = total_muertes_por_municipio.loc[total_muertes_por_municipio['MUNICIPIO'] == municipio, 'TOTAL_MANERA_DE_MUERTE'].values[0]
    
    # Formatear el total de muertes a miles (K) para mostrarlo de manera más legible
    total_muerte_formateado = '{:.1f}K'.format(total_muerte / 1000)

    # Añadir el texto con el total de muertes al final de las barras
    fig_top5.add_trace(go.Scatter(
        x=[total_muerte],  # Total de muertes
        y=[municipio],  # Municipio
        mode='text',  # Mostrar texto
        text=[f'{total_muerte_formateado}'],  # El texto a mostrar con formato
        showlegend=False,
        textposition='top right',  # Mostrar el texto fuera de la barra
        hoverinfo='none'  # No mostrar información al pasar el mouse
    ))

# Configurar el layout
fig_top5.update_layout(
    title='Top 5 Ciudades Más Violentas',
    xaxis_title='Total Muertes por Manera de Muerte',
    yaxis_title='Municipio',
    barmode='stack',  # Apilar las barras
    showlegend=True,
    yaxis=dict(
        categoryorder='array',  # Ordenar categorías en el eje Y
        categoryarray=top_5_municipios['MUNICIPIO'].iloc[::-1].tolist()  # Invertir el orden de los municipios
    ),
    xaxis=dict(
        range=[0, total_muertes_por_municipio['TOTAL_MANERA_DE_MUERTE'].max() * 1.1]  # Aumentar el rango del eje X
    ),
    legend=dict(
        yanchor='bottom',
        y=-0.4,
        xanchor='left',
        x=0,
        orientation='h',            # Leyenda horizontal para ahorrar espacio
        title_text='Manera de Muerte:'   # Título del legend
    )
)

#------------------------------------------------------------
# 3.2 Gráfico de torta
#------------------------------------------------------------
fig_pie = go.Figure(data=[go.Pie(
    labels=top_10_municipios_menor_muerte['MUNICIPIO'],  # Los municipios estarán en las etiquetas
    values=top_10_municipios_menor_muerte['TOTAL_MANERA_DE_MUERTE'],  # Los valores serán el total de muertes
    marker=dict(colors=colores_paleta),  # Asignar la paleta de colores personalizada
)])

# Configurar el layout del gráfico
fig_pie.update_layout(
    title='Top 10 Ciudades con menor índice de mortalidad',
    showlegend=False
)

#------------------------------------------------------------
# 3.3 Gráfico de líneas
#------------------------------------------------------------
fig_line = go.Figure()

# Crear las trazas para cada departamento con colores personalizados
departamentos = data_final['DEPARTAMENTO'].unique()

# Diccionario para almacenar las visibilidades de las trazas
visibilidad_trazas = []

for i, dept in enumerate(departamentos):
    dept_data = data_final[data_final['DEPARTAMENTO'] == dept]
    fig_line.add_trace(go.Scatter(
        x=dept_data['MES'].astype(str),
        y=dept_data['TOTAL_MUERTES_POR_MES_Y_DPTO'],
        mode='lines+markers',
        name=dept,
        line=dict(color=colores_paleta[i % len(colores_paleta)]),  # Asignar un color único
        marker=dict(color=colores_paleta[i % len(colores_paleta)]),  # También para los marcadores
    ))
    # Inicialmente todas las trazas son visibles
    visibilidad_trazas.append(True)

# Agregar un dropdown menu para seleccionar el departamento
fig_line.update_layout(
    updatemenus=[dict(
        type='dropdown',
        x=0.9,
        y=1.15,
        buttons=[
            dict(label='Todos',
                 method='update',
                 args=[{'visible': visibilidad_trazas},
                       {'title': 'Total de Muertes por Mes'}]),
            *[
                dict(label=dept,
                     method='update',
                     args=[{'visible': [True if d == dept else False for d in departamentos]},
                           {'title': f'Total de Muertes por Mes'}])
                for dept in departamentos
            ]
        ]
    )],
    title='Total de Muertes por Mes',
    xaxis_title='Mes',
    yaxis_title='Total Muertes',
)

#------------------------------------------------------------
# 3.3 Gráfico de mapa
#------------------------------------------------------------

# Crear figura vacía
fig_map_colombia = go.Figure()

# Añadir los puntos
fig_map_colombia.add_trace(go.Scattergeo(
    lat=data_final['LATITUD'],
    lon=data_final['LONGITUD'],
    text=(data_final['DEPARTAMENTO'] + ': ' +
          data_final['TOTAL_MUERTES_POR_DPTO'].astype(str) + ' muertes'),
    mode='markers',
    marker=dict(
        size=data_final['TOTAL_MUERTES_POR_DPTO'] / 1000,
        color=data_final['TOTAL_MUERTES_POR_DPTO'],
        colorscale='Magma',
        showscale=True,                # deja una sola barra de color
        colorbar=dict(                 # posición de la barra
            title='Total de Muertes',
            x=0.88, xanchor='left',
            y=0.5, len=0.75
        )
    )
))

# Ajustar el mapa y la disposición
fig_map_colombia.update_geos(
    visible=True,
    resolution=50,
    projection_type='mercator',
    center=dict(lon=-74.2973, lat=4.5709),
    showland=True,
    showsubunits=True,         # las fronteras departamentales siguen visibles
    landcolor='rgb(204,209,209)',
    lakecolor='rgb(204,209,209)'
)

fig_map_colombia.update_layout(
    title_text='Distribución Total de Muertes por Departamento',
    geo=dict(
        scope='south america',
        projection_scale=5,
        domain=dict(x=[0, 0.80], y=[0, 1])   # deja 20 % de ancho para la barra
    ),
    margin=dict(l=30, r=0, t=80, b=0)
)

#------------------------------------------------------------
# 3.4 Tabla: Listado de las 10 principales causas de muerte
#------------------------------------------------------------

# Cargar los archivos
df_muertes = pd.read_excel(DATA_DIR / "Anexo1.NoFetal2019_CE_15-03-23.xlsx")
df_codigos = pd.read_excel(DATA_DIR / "Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx", skiprows=8)
df_divipola = pd.read_excel(DATA_DIR / "Anexo3.Divipola_CE_15-03-23.xlsx")

# Filtrar las muertes por COD_MUERTE
df_muertes = df_muertes[df_muertes["COD_MUERTE"].notnull()]
df_muertes = df_muertes[df_muertes["COD_MUERTE"].astype(str).str.match(r'^[A-Z0-9]+X?$')]  # Permitir un sufijo opcional "X"
df_muertes = df_muertes[df_muertes["COD_MUERTE"].str.len() <= 7]

# Agregar el sufijo 'X' solo a los valores 'C61' e 'I10' en la columna COD_MUERTE
df_muertes["COD_MUERTE"] = df_muertes["COD_MUERTE"].apply(
    lambda x: f"{x}X" if x in ["C61", "I10"] else x
)

# Convertir COD_MUERTE a string
df_muertes["COD_MUERTE"] = df_muertes["COD_MUERTE"].astype(str)

# Agrupar por COD_MUERTE para obtener el total de muertes
df_top = df_muertes.groupby("COD_MUERTE").size().reset_index(name="TOTAL")

# Asegurarse de que df_codigos tiene las columnas necesarias
if "Código de la CIE-10 cuatro caracteres" in df_codigos.columns and "Descripcion  de códigos mortalidad a cuatro caracteres" in df_codigos.columns:
    # Realizar el merge para agregar la descripción
    df_top = df_top.merge(df_codigos, left_on="COD_MUERTE", right_on="Código de la CIE-10 cuatro caracteres", how="left")
else:
    raise ValueError("El archivo de códigos no contiene las columnas 'Código de la CIE-10 cuatro caracteres' y 'Descripcion  de códigos mortalidad a cuatro caracteres'.")

# Seleccionar las 10 principales causas de muerte
df_top10 = df_top.sort_values("TOTAL", ascending=False).head(10)[["COD_MUERTE", "Descripcion  de códigos mortalidad a cuatro caracteres", "TOTAL"]]

#------------------------------------------------------------
# 3.5 Histograma: Distribución por grupo de edad
#------------------------------------------------------------

# Histograma por rango quinquenal
df_muertes = df_muertes[df_muertes["GRUPO_EDAD1"] >= 0]
bins = list(range(0, 90, 5)) + [150]
labels = [f"{i}-{i+4}" for i in range(0, 85, 5)] + ["85+"]
df_muertes["RANGO_EDAD"] = pd.cut(df_muertes["GRUPO_EDAD1"], bins=bins, labels=labels, right=False)
df_histograma = df_muertes["RANGO_EDAD"].value_counts().sort_index().reset_index()
df_histograma.columns = ["RANGO_EDAD", "TOTAL"]

#------------------------------------------------------------
# 3.6 Barras apiladas: Muertes por sexo y departamento
#------------------------------------------------------------

# Crear df_sexo_dpto agrupando las muertes por departamento y sexo
df_muertes["SEXO"] = df_muertes["SEXO"].map({1: "Hombre", 2: "Mujer"})
df_muertes["COD_DEPARTAMENTO"] = df_muertes["COD_DEPARTAMENTO"].astype(str).str[:2]

# Agrupar por departamento y sexo para obtener el total de muertes
df_sexo_dpto = df_muertes.groupby(["COD_DEPARTAMENTO", "SEXO"]).size().reset_index(name="TOTAL")

# Definir df_departamentos a partir de divipola_departamentos_data
df_departamentos = divipola_departamentos_data

# Asegurarse de que 'COD_DEPARTAMENTO' sea de tipo string en ambos DataFrames
df_sexo_dpto["COD_DEPARTAMENTO"] = df_sexo_dpto["COD_DEPARTAMENTO"].astype(str)
df_departamentos["COD_DEPARTAMENTO"] = df_departamentos["COD_DEPARTAMENTO"].astype(str)

# Realizar el merge para agregar los nombres de los departamentos
df_sexo_dpto = df_sexo_dpto.merge(df_departamentos, on="COD_DEPARTAMENTO", how="left")

# Agrupar nuevamente para asegurarse de que no haya duplicados
df_sexo_dpto = df_sexo_dpto.groupby(["DEPARTAMENTO", "SEXO"], as_index=False)["TOTAL"].sum()

# Crear el DataFrame para las barras apiladas
df_barras_apiladas = df_sexo_dpto.pivot(index="DEPARTAMENTO", columns="SEXO", values="TOTAL").fillna(0).reset_index()

#------------------------------------------------------------
# 4. DASH
#------------------------------------------------------------

TITLE = 'Análisis de mortalidad en Colombia para el año 2019'
app = dash.Dash(__name__)
app.title = 'Análisis de mortalidad en Colombia para el año 2019'

# Definir Layout
app.layout = html.Div(
    style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9'},
    children=[
        # Título principal
        html.H1(
            TITLE,
            style={
                'textAlign': 'center',
                'marginBottom': '25px',
                'color': '#113250',
                'fontSize': '32px',
                'fontWeight': 'bold',
            },
        ),

        # Pestañas para organizar los gráficos y la tabla
        dcc.Tabs(
            id='tabs',
            children=[
                # Pestaña 1: Gráfico de líneas
                dcc.Tab(
                    label='Gráfico de Líneas',
                    style={'backgroundColor': '#e6e6e6', 'border': '1px solid #ccc'},
                    selected_style={'backgroundColor': '#ffffff', 'border': '1px solid #113250', 'fontWeight': 'bold'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'padding': '10px'},
                            children=[
                                html.H3(
                                    "Tendencia de muertes por mes",
                                    style={'textAlign': 'center', 'color': '#113250'},
                                ),
                                dcc.Graph(id='line_chart', figure=fig_line),
                            ],
                        ),
                    ],
                ),
                # Pestaña 2: Gráfico de barras apiladas (Top 5)
                dcc.Tab(
                    label='Top 5 Ciudades Más Violentas',
                    style={'backgroundColor': '#e6e6e6', 'border': '1px solid #ccc'},
                    selected_style={'backgroundColor': '#ffffff', 'border': '1px solid #113250', 'fontWeight': 'bold'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'padding': '10px'},
                            children=[
                                html.H3(
                                    "Ciudades con mayor índice de violencia",
                                    style={'textAlign': 'center', 'color': '#113250'},
                                ),
                                dcc.Graph(id='top5_bar', figure=fig_top5),
                            ],
                        ),
                    ],
                ),
                # Pestaña 3: Gráfico de torta
                dcc.Tab(
                    label='Top 10 Ciudades con Menor Mortalidad',
                    style={'backgroundColor': '#e6e6e6', 'border': '1px solid #ccc'},
                    selected_style={'backgroundColor': '#ffffff', 'border': '1px solid #113250', 'fontWeight': 'bold'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'padding': '10px'},
                            children=[
                                html.H3(
                                    "Ciudades con menor índice de mortalidad",
                                    style={'textAlign': 'center', 'color': '#113250'},
                                ),
                                dcc.Graph(id='pie_chart', figure=fig_pie),
                            ],
                        ),
                    ],
                ),
                # Pestaña 4: Gráfico de mapa
                dcc.Tab(
                    label='Mapa de Mortalidad por Departamento',
                    style={'backgroundColor': '#e6e6e6', 'border': '1px solid #ccc'},
                    selected_style={'backgroundColor': '#ffffff', 'border': '1px solid #113250', 'fontWeight': 'bold'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'padding': '10px'},
                            children=[
                                html.H3(
                                    "Distribución geográfica de muertes",
                                    style={'textAlign': 'center', 'color': '#113250'},
                                ),
                                dcc.Graph(id='mapa_colombia', figure=fig_map_colombia),
                            ],
                        ),
                    ],
                ),
                # Pestaña 5: Tabla de causas de muerte
                dcc.Tab(
                    label='Top 10 Causas de Muerte',
                    style={'backgroundColor': '#e6e6e6', 'border': '1px solid #ccc'},
                    selected_style={'backgroundColor': '#ffffff', 'border': '1px solid #113250', 'fontWeight': 'bold'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'padding': '10px'},
                            children=[
                                html.H3(
                                    "Principales causas de muerte en Colombia",
                                    style={'textAlign': 'center', 'color': '#113250'},
                                ),
                                dash_table.DataTable(
                                    columns=[{"name": i, "id": i} for i in df_top10.columns],
                                    data=df_top10.to_dict("records"),
                                    style_table={'overflowX': 'auto'},
                                    style_cell={
                                        'textAlign': 'left',
                                        'padding': '10px',
                                        'fontFamily': 'Arial, sans-serif',
                                    },
                                    style_header={
                                        'backgroundColor': '#113250',
                                        'color': 'white',
                                        'fontWeight': 'bold',
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                # Pestaña 6: Histograma de distribución por rangos de edad
                dcc.Tab(
                    label='Histograma por Edad',
                    style={'backgroundColor': '#e6e6e6', 'border': '1px solid #ccc'},
                    selected_style={'backgroundColor': '#ffffff', 'border': '1px solid #113250', 'fontWeight': 'bold'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'padding': '10px'},
                            children=[
                                html.H3(
                                    "Distribución de muertes por rangos de edad",
                                    style={'textAlign': 'center', 'color': '#113250'},
                                ),
                                dcc.Graph(
                                    figure=px.bar(
                                        df_histograma,
                                        x="RANGO_EDAD",
                                        y="TOTAL",
                                        title="Muertes por grupo quinquenal de edad",
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                # Pestaña 7: Muertes por sexo y departamento
                dcc.Tab(
                    label='Muertes por Sexo y Departamento',
                    style={'backgroundColor': '#e6e6e6', 'border': '1px solid #ccc'},
                    selected_style={'backgroundColor': '#ffffff', 'border': '1px solid #113250', 'fontWeight': 'bold'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'padding': '10px'},
                            children=[
                                html.H3(
                                    "Distribución de muertes por sexo y departamento",
                                    style={'textAlign': 'center', 'color': '#113250'},
                                ),
                                dcc.Graph(
                                    figure=px.bar(
                                        df_barras_apiladas,
                                        x="DEPARTAMENTO",
                                        y=["Hombre", "Mujer"],
                                        title="Total de muertes por sexo en cada departamento",
                                        labels={"value": "Muertes", "variable": "Sexo"},
                                        barmode="stack",
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # Pie de página
        html.Footer(
            style={'textAlign': 'center', 'marginTop': '50px', 'color': '#717C7D', 'fontSize': '14px'},
            children=[
                html.P("Análisis de Mortalidad en Colombia - 2019"),
                html.P("Fuente: Datos oficiales del gobierno de Colombia"),
            ],
        ),
    ],
)

server = app.server  # Necesario para Render

# SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)
