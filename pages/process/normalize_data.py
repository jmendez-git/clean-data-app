import streamlit as st
import os
import time
import csv
from utils.normalize import normalizar_datos_manual, normalizar_datos_pandas
from utils.import_data import get_data_lib_pandas

st.header('Normalizar Datos y Diagnóstico de Calidad')

server_folder = './data/raw'
processed_folder = './data/processed'

os.makedirs(processed_folder, exist_ok=True)

def mostrar_estadisticas(stats, tiempo):
    """Renderiza las métricas en la interfaz de Streamlit"""
    st.success(f"Proceso completado en {tiempo:.4f} segundos.")
    
    st.write("#### 📊 Resumen del Dataset")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Filas", stats['total_filas'])
    col2.metric("Total de Columnas", stats['total_columnas'])
    col3.metric("Valores Faltantes/Inválidos", stats['total_nulos'])
    
    col4, col5 = st.columns(2)
    col4.metric("Registros Válidos (Limpios)", stats['filas_validas'])
    col5.metric("Registros con Nulos", stats['filas_con_nulos'])

    st.write("#### Problemas por Columna")
    columnas_con_problemas = {k: v for k, v in stats['nulos_por_columna'].items() if v > 0}
    if columnas_con_problemas:
        for col, count in columnas_con_problemas.items():
            st.write(f"- **{col}**: {count} valores nulos")
    else:
        st.info("No se encontraron valores nulos en ninguna columna.")

    st.write("---")
    st.write("#### Justificación de Decisiones")
    st.markdown("""
    * **Conversión:** Las calificaciones textuales (ej. *'seis'*, *'cinco punto tres'*) se transformaron a tipo numérico de punto flotante utilizando un diccionario.
    * **Corrección (Homologación de escala):** Si se detectaron calificaciones superiores a 10, el sistema asumió una escala de 0-100 y dividió el valor entre 10 para acoplar todos los registros a una escala unificada de 0-10.
    * **Corrección (Campos de texto):** Los campos categóricos (*nombre, institución, modalidad, etc.*) se convirtieron a minúsculas y se eliminaron los espacios intermedios .
    * **Conservación (Nulos):** Los valores identificados como ausentes (*"N/A", "NULL", "S/C", etc.*) fueron convertidos a un formato nulo estándar (`None` o `NaN`). Se decidió **conservarlos** en esta etapa en lugar de descartar la fila entera.
    """)

if os.path.exists(server_folder):
    archivos_disponibles = [
        f for f in os.listdir(server_folder) 
        if os.path.isfile(os.path.join(server_folder, f))
    ]

    if archivos_disponibles:
        archivo_seleccionado = st.selectbox(
            'Selecciona el archivo que desea cargar:',
            options=archivos_disponibles
        )

        ruta_completa = os.path.join(server_folder, archivo_seleccionado)
        nuevo_nombre = f"norm_{archivo_seleccionado}"
        ruta_guardado = os.path.join(processed_folder, nuevo_nombre)
        
        file = get_data_lib_pandas(ruta_completa)
        df_crudo = file[2] if isinstance(file, tuple) else file 
        
        st.write('##### Previsualización Original')
        st.dataframe(df_crudo.head())

        col1, col2 = st.columns(2)
        with col1:
            btn_manual = st.button('Normalizar (Manual)', type='primary', use_container_width=True)
        with col2:
            btn_pandas = st.button('Normalizar (Pandas)', type='primary', use_container_width=True)

        if btn_manual:
            with st.spinner("Ejecutando proceso manual..."):
                inicio = time.time()
                datos_procesados, stats_manual = normalizar_datos_manual(ruta_completa)
                fin = time.time()
                
                mostrar_estadisticas(stats_manual, fin - inicio)
                
                st.write('##### Previsualización de Datos Normalizados')
                st.dataframe(datos_procesados[:10]) 

                if datos_procesados:
                    claves = datos_procesados[0].keys()
                    with open(ruta_guardado, 'w', newline='', encoding='utf-8-sig') as f:
                        dict_writer = csv.DictWriter(f, fieldnames=claves)
                        dict_writer.writeheader()
                        dict_writer.writerows(datos_procesados)
                    
                    st.success(f"📁 Archivo guardado en el servidor: `{ruta_guardado}`")

        if btn_pandas:
            with st.spinner("Ejecutando proceso con Pandas..."):
                inicio = time.time()
                df_procesado, stats_pandas = normalizar_datos_pandas(df_crudo)
                fin = time.time()
                
                mostrar_estadisticas(stats_pandas, fin - inicio)
                
                st.write('##### Previsualización de Datos Normalizados')
                st.dataframe(df_procesado)

                df_procesado.to_csv(ruta_guardado, index=False, encoding='utf-8-sig')
                
                st.success(f"📁 Archivo guardado en el servidor: `{ruta_guardado}`")

    else:
        st.warning("⚠️ No hay archivos guardados en el servidor todavía.")
else:
    st.error("❌ La carpeta del servidor no existe. Primero debes guardar un archivo.")