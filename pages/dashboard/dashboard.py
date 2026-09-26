import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.header('Salud Académica Nivel Medio Superior')

processed_folder = './data/processed'

if not os.path.exists(processed_folder):
    st.error(f"El directorio {processed_folder} no existe.")
    st.stop()

archivos_procesados = [f for f in os.listdir(processed_folder) if f.endswith('.csv') and f.startswith('norm_')]

if not archivos_procesados:
    st.warning("⚠️ No se encontraron archivos normalizados. Primero ejecuta la normalización de datos.")
    st.stop()

ruta_archivo = os.path.join(processed_folder, archivos_procesados[0])
df = pd.read_csv(ruta_archivo)

df['calificacion'] = pd.to_numeric(df['calificacion'], errors='coerce')

st.write(f"**Fuente de datos:** `{archivos_procesados[0]}` | **Total de registros válidos:** {len(df)}")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Distribución de Instituciones")
    instituciones_unicas = df.drop_duplicates(subset=['institucion', 'tipo_institucion'])
    conteo_instituciones = instituciones_unicas['tipo_institucion'].value_counts().reset_index()
    conteo_instituciones.columns = ['Tipo de Institución', 'Cantidad']
    
    total_inst = conteo_instituciones['Cantidad'].sum()
    conteo_instituciones['Porcentaje'] = (conteo_instituciones['Cantidad'] / total_inst * 100).round(2)
    
    st.dataframe(conteo_instituciones, hide_index=True, use_container_width=True)
    
    fig_inst = px.pie(conteo_instituciones, values='Cantidad', names='Tipo de Institución', hole=0.4,
                      title="Proporción de Instituciones (Pública vs Privada)",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_inst, use_container_width=True)

with col2:
    st.subheader("2. Estudiantes por Tipo de Institución")
    estudiantes_por_tipo = df.groupby('tipo_institucion')['id_estudiante'].nunique().reset_index()
    estudiantes_por_tipo.columns = ['Tipo de Institución', 'Total Estudiantes']
    
    st.dataframe(estudiantes_por_tipo, hide_index=True, use_container_width=True)
    
    fig_est = px.bar(estudiantes_por_tipo, x='Tipo de Institución', y='Total Estudiantes',
                     title="Volumen de Estudiantes por Sector",
                     color='Tipo de Institución', text_auto=True,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_est, use_container_width=True)

st.divider()

st.subheader("3. Distribución de Calificaciones por Tipo de Examen")
df_calificaciones = df.dropna(subset=['calificacion', 'tipo_examen'])

col_dist1, col_dist2 = st.columns([2, 1])

with col_dist1:
    fig_dist = px.box(df_calificaciones, x='tipo_examen', y='calificacion', color='tipo_examen',
                      title="Dispersión de Calificaciones (Conocimiento General vs Idiomas)",
                      points="all")
    st.plotly_chart(fig_dist, use_container_width=True)

with col_dist2:
    promedio_examen = df_calificaciones.groupby('tipo_examen')['calificacion'].mean().round(2).reset_index()
    promedio_examen.columns = ['Tipo de Examen', 'Promedio Global']
    st.write("**Promedios Generales**")
    st.dataframe(promedio_examen, hide_index=True, use_container_width=True)

st.divider()

st.subheader("4. Promedio de Calificaciones por Institución y Examen")
pivot_promedios = df.pivot_table(
    values='calificacion', 
    index='institucion', 
    columns='tipo_examen', 
    aggfunc='mean'
).round(2).reset_index()

pivot_promedios.columns.name = None
pivot_promedios = pivot_promedios.fillna('Sin registros')
st.dataframe(pivot_promedios, use_container_width=True, height=300)
