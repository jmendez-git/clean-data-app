import csv
import pandas as pd
import numpy as np

NUMEROS_TEXTO = {
    "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "cincuenta": 50, "sesenta y seis": 66, "cien": 100
}

MARCADORES_AUSENCIA = ["", "n/a", "null", "nan", "s/c", "none"]

def es_nulo_manual(valor):
    if pd.isna(valor) or valor is None: return True
    return str(valor).strip().lower() in MARCADORES_AUSENCIA

def convertir_calificacion(valor):
    if es_nulo_manual(valor): return None
    valor_str = str(valor).strip().lower()
    
    try:
        num = float(valor_str)
    except ValueError:
        if "punto" in valor_str:
            partes = valor_str.split("punto")
            entero = NUMEROS_TEXTO.get(partes[0].strip(), 0)
            decimal = NUMEROS_TEXTO.get(partes[1].strip(), 0)
            num = float(f"{entero}.{decimal}")
        else:
            num = float(NUMEROS_TEXTO.get(valor_str, 0))

    if num > 10:
        num = num / 10.0
        
    return num

def normalizar_datos_manual(ruta_archivo):
    datos_normalizados = []
    
    columnas_texto = [
        'nombre', 'apellido', 'tipo_examen', 'modalidad',
        'institución', 'institucion', 
        'tipo_institución', 'tipo_institucion'
    ]
    columnas_calificacion = ['calificacion', 'nota', 'promedio'] 
    
    stats = {
        'total_filas': 0, 'total_columnas': 0, 'total_nulos': 0,
        'filas_con_nulos': 0, 'filas_validas': 0, 'nulos_por_columna': {}
    }

    with open(ruta_archivo, mode='r', encoding='utf-8-sig') as archivo:
        lector = csv.DictReader(archivo)
        stats['total_columnas'] = len(lector.fieldnames) if lector.fieldnames else 0
        
        if lector.fieldnames:
            for col in lector.fieldnames:
                stats['nulos_por_columna'][col.strip().lower()] = 0
        
        for fila in lector:
            stats['total_filas'] += 1
            fila_normalizada = {}
            fila_tiene_nulo = False
            
            for col, valor in fila.items():
                col_norm = col.strip().lower() if col else ""
                
                if es_nulo_manual(valor):
                    stats['nulos_por_columna'][col_norm] += 1
                    stats['total_nulos'] += 1
                    fila_tiene_nulo = True
                
                # Normalización
                if col_norm in columnas_texto:
                    if es_nulo_manual(valor):
                        fila_normalizada[col_norm] = None
                    else:
                        texto_limpio = " ".join(str(valor).lower().strip().split())
                        fila_normalizada[col_norm] = texto_limpio
                elif col_norm in columnas_calificacion:
                    fila_normalizada[col_norm] = convertir_calificacion(valor)
                else:
                    fila_normalizada[col_norm] = None if es_nulo_manual(valor) else str(valor).strip()
                    
            if fila_tiene_nulo:
                stats['filas_con_nulos'] += 1
            else:
                stats['filas_validas'] += 1
                
            datos_normalizados.append(fila_normalizada)
            
    return datos_normalizados, stats

def normalizar_datos_pandas(df_original):
    df = df_original.copy()
    df.columns = df.columns.str.strip().str.lower()
    
    mask_nulos = df.apply(lambda col: col.map(es_nulo_manual))
    df = df.mask(mask_nulos, np.nan)

    stats = {
        'total_filas': len(df),
        'total_columnas': len(df.columns),
        'total_nulos': int(df.isna().sum().sum()),
        'filas_con_nulos': int(df.isna().any(axis=1).sum()),
        'filas_validas': int(len(df) - df.isna().any(axis=1).sum()),
        'nulos_por_columna': df.isna().sum().to_dict()
    }
    
    columnas_texto = [
        'nombre', 'apellido', 'tipo_examen', 'modalidad',
        'institución', 'institucion', 
        'tipo_institución', 'tipo_institucion'
    ]
    columnas_calificacion = ['calificacion', 'nota', 'promedio']
    
    for col in columnas_texto:
        if col in df.columns:
            mask_not_null = df[col].notna()
            df.loc[mask_not_null, col] = df.loc[mask_not_null, col].astype(str).str.lower().str.strip()
            df.loc[mask_not_null, col] = df.loc[mask_not_null, col].replace(r'\s+', ' ', regex=True)
            
    def convertir_calificacion_pandas(valor):
        if pd.isna(valor): return np.nan
        return convertir_calificacion(valor)

    for col in columnas_calificacion:
        if col in df.columns:
            df[col] = df[col].apply(convertir_calificacion_pandas)
            
    return df, stats