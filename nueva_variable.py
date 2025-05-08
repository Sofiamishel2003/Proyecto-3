import pandas as pd

# Cargar datos
matrimonios_df = pd.read_csv("matrimonios_limpio.csv")
divorcios_df = pd.read_csv("divorcios_limpio.csv")

# Crear una firma con variables comunes
matrimonios_df['firma'] = (
    matrimonios_df['Ano Ocurrencia'].astype(str) + '_' +
    matrimonios_df['Departamento de Ocurrencia'].astype(str) + '_' +
    matrimonios_df['Edad del Hombre'].astype(str) + '_' +
    matrimonios_df['Edad de la Mujer'].astype(str) + '_' +
    matrimonios_df['Escolaridad del Hombre'].astype(str) + '_' +
    matrimonios_df['Escolaridad de la Mujer'].astype(str)
)

divorcios_df['firma'] = (
    divorcios_df['Ano Ocurrencia'].astype(str) + '_' +
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
matrimonios_df.to_csv("dataset_modelo.csv", index=False)

# Total de registros
print("Total:", len(matrimonios_df))

# Conteo de divorcios == 0 y == 1
print(matrimonios_df['divorcio'].value_counts())