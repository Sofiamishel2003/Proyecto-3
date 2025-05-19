import pandas as pd

# Cargar datos
matrimonios_df = pd.read_csv("Datos\matrimonios_limpio.csv")
divorcios_df = pd.read_csv("Datos\divorcios_limpio.csv")

# Crear una firma con variables comunes
matrimonios_df['firma'] = (
    matrimonios_df['Departamento de Ocurrencia'].astype(str) + '_' +
    matrimonios_df['Edad del Hombre'].astype(str) + '_' +
    matrimonios_df['Edad de la Mujer'].astype(str) + '_' +
    matrimonios_df['Escolaridad del Hombre'].astype(str) + '_' +
    matrimonios_df['Escolaridad de la Mujer'].astype(str)
)

divorcios_df['firma'] = (
    divorcios_df['Departamento de Ocurrencia'].astype(str) + '_' +
    divorcios_df['Edad del Hombre'].astype(str) + '_' +
    divorcios_df['Edad de la Mujer'].astype(str) + '_' +
    divorcios_df['Escolaridad del Hombre'].astype(str) + '_' +
    divorcios_df['Escolaridad de la Mujer'].astype(str)
)

# Extraer firmas únicas de divorcios
firmas_divorcio = set(divorcios_df['firma'].unique())

# Crear la variable objetivo
matrimonios_df['divorcio'] = matrimonios_df['firma'].apply(lambda x: 1 if x in firmas_divorcio else 0)

# Eliminar columna 'firma'
matrimonios_df = matrimonios_df.drop(columns=['firma'])

# Guardar
matrimonios_df.to_csv("Datos\dataset_modelo.csv", index=False)

# Total de registros
print("Total:", len(matrimonios_df))

# Conteo de divorcios == 0 y == 1
print(matrimonios_df['divorcio'].value_counts())

# Obtener una muestra con distribución equitativa entre clases
# Separar las clases
divorciados = matrimonios_df[matrimonios_df['divorcio'] == 1]
no_divorciados = matrimonios_df[matrimonios_df['divorcio'] == 0]

# Muestrear aleatoriamente la misma cantidad que los divorciados
no_divorciados_sample = no_divorciados.sample(n=len(divorciados), random_state=42)

# Unir las dos clases
df_balanceado = pd.concat([divorciados, no_divorciados_sample])

# Mezclar el orden de las filas
df_balanceado = df_balanceado.sample(frac=1, random_state=42).reset_index(drop=True)

# Guardar
df_balanceado.to_csv("Datos\dataset_muestra50.csv", index=False)

# Total de registros
print("Total:", len(matrimonios_df))

# Verificar distribución
print(df_balanceado['divorcio'].value_counts())

# MUESTRA CON MÁS CASOS DE DIVORCIOS
proporcion_divorciados = 0.6
num_divorciados = len(divorciados)
num_no_divorciados = int(num_divorciados * (1 - proporcion_divorciados) / proporcion_divorciados)

# Muestrear los no divorciados
no_divorciados_sample = no_divorciados.sample(n=num_no_divorciados, random_state=42)

# Combinar
df_balanceado = pd.concat([divorciados, no_divorciados_sample])

# Mezclar las filas
df_balanceado = df_balanceado.sample(frac=1, random_state=42).reset_index(drop=True)

# Guardar
df_balanceado.to_csv("Datos/dataset_muestra60.csv", index=False)

# Total de registros
print("Total muestra 60/40:", len(df_balanceado))

# Verificar distribución
print(df_balanceado['divorcio'].value_counts())