import os
import pandas as pd
import pyreadstat

# Directorio donde están los archivos .sav
directorio = r"D:\Downloads\Matrimonios"  # Asegúrate de usar `r` para evitar problemas con `\`


# Obtener la lista de archivos .sav
archivos_sav = [f for f in os.listdir(directorio) if f.endswith(".sav")]

# Lista para almacenar los DataFrames
dataframes = []

for archivo in archivos_sav:
    ruta_completa = os.path.join(directorio, archivo)
    df, meta = pyreadstat.read_sav(ruta_completa)
    
    # Normalizar nombres de columnas (convertir a minúsculas y eliminar espacios)
    df.columns = df.columns.str.lower().str.strip()
    
    # Agregar el DataFrame a la lista
    dataframes.append(df)

# Unir todos los DataFrames en uno solo
df_unido = pd.concat(dataframes, ignore_index=True)

# Diccionario de columnas equivalentes (nombres alternativos para los mismos datos)
column_merge = {
    "ocuhom": "ciuohom",  # Ocupación del Hombre
    "ocumuj": "ciuomuj",  # Ocupación de la Mujer
    "puehom": "pperhom",  # Pueblo de Pertenencia del Hombre
    "puemuj": "ppermuj",  # Pueblo de Pertenencia del Mujer
}

# Fusionar columnas duplicadas (si una está vacía, usa la otra)
for col_main, col_alt in column_merge.items():
    if col_main in df_unido.columns and col_alt in df_unido.columns:
        df_unido[col_main] = df_unido[col_main].combine_first(df_unido[col_alt])
        df_unido.drop(columns=[col_alt], inplace=True)  # Eliminar la columna fusionada

# Diccionario para corregir nombres incorrectos
column_mapping = {
    "depreg": "Departamento de Registro",
    "mupreg": "Municipio de Registro",
    "mesreg": "Mes de Registro",
    "añoreg": "Ano de Registro",
    "añoocu": "Ano Ocurrencia",
    "clauni": "Clase de Union",
    "edadhom": "Edad del Hombre",
    "edadmuj": "Edad de la Mujer",
    "nunuho": "Numero de Nupcias del Hombre",
    "nunumu": "Numero de Nupcias de la Mujer",
    "nachom": "Nacionalidad del Hombre",
    "nacmuj": "Nacionalidad de la Mujer",
    "eschom": "Escolaridad del Hombre",
    "escmuj": "Escolaridad de la Mujer",
    "ciuohom": "Ocupacion del Hombre",
    "ciuomuj": "Ocupacion de la Mujer",
    "depocu": "Departamento de Ocurrencia",
    "mupocu": "Municipio de Ocurrencia",
    "diaocu": "Dia de la Ocurrencia",
    "mesocu": "Mes de la Ocurrencia",
    "areagocu": "Area Geografica de la Ocurrencia",
    "puehom": "Pueblo de Pertenencia del Hombre",
    "puemuj": "Pueblo de Pertenencia de la Mujer",
    "areag": "Area Geografica de Residencia",
    "ocuhom": "Ocupacion del Hombre",
    "ocumuj": "Ocupacion de la Mujer",
    "getmuj": "Grupo etnico de la mujer",
    "gethom": "Grupo etnico del Hombre",
    "pperhom": "Pueblo de Pertenencia del Hombre",
    "ppermuj": "Pueblo de Pertenencia de la Mujer"
}

# Renombrar columnas si están en el diccionario de correcciones
df_unido.rename(columns=lambda x: column_mapping.get(x, x), inplace=True)

# Guardar el archivo final limpio
df_unido.to_csv("matrimonios_limpio.csv", index=False)

print("Archivo unido y limpio guardado como matrimonios_limpio.csv")

