import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Cargar datos
matrimonios_df = pd.read_csv("matrimonios_limpio.csv")
divorcios_df = pd.read_csv("divorcios_limpio.csv")

# Seleccion de variables relevantes (según el análisis realizado)
variables_clave = ["edad_promedio", "años_matrimonio", "num_hijos", "nivel_educativo"]  

# Paso 1: selecciona las variables que quieres usar como base para calcular la probabilidad
caracteristicas_clave = ['edad_esposo', 'edad_esposa', 'educacion_esposo', 'educacion_esposa']

# Paso 2: agrupa el dataset de divorcios por esas variables y cuenta ocurrencias
patrones_divorcio = divorcios_df.groupby(caracteristicas_clave).size().reset_index(name='frecuencia_divorcio')

# Paso 3: normaliza la frecuencia para obtener una probabilidad relativa
total_divorcios = patrones_divorcio['frecuencia_divorcio'].sum()
patrones_divorcio['probabilidad_divorcio'] = patrones_divorcio['frecuencia_divorcio'] / total_divorcios

# Paso 4: unir esa info al dataset de matrimonios
matrimonios_df = matrimonios_df.merge(
    patrones_divorcio[caracteristicas_clave + ['probabilidad_divorcio']],
    on=caracteristicas_clave,
    how='left'
)

# Paso 5: si alguna combinación no apareció en divorcios, asumimos baja probabilidad (o cero)
matrimonios_df['probabilidad_divorcio'] = matrimonios_df['probabilidad_divorcio'].fillna(0)

# Guardar nuevo dataset con la variable calculada
divorcios_df.to_csv("datos_con_probabilidad_divorcio.csv", index=False)

print("Variable 'probabilidad_divorcio' creada y guardada en 'datos_con_probabilidad_divorcio.csv'")
