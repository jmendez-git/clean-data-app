import streamlit as st

if 'window' not in st.session_state:
    st.session_state.window = None

WINDOWS = [None, 'Cargar Datos', 'Dashboard', 'Rendimiento']

def index():
    st.header('Registro de Alumnos Nivel Media Superior')

    window = st.selectbox('Elige una Acccion', WINDOWS)

    if st.button('Seleccionar'):
        st.session_state.window = window
        st.rerun()

def back_index():
    st.session_state.window = None
    st.rerun()

window = st.session_state.window

index_page = st.Page(
    back_index,
    title='Regresar al Inicio',
    icon='👈'
)

load_data = st.Page(
    'pages/process/load_data.py',
    title='Cargar Datos',
    icon='📂',
    default=(window == 'Cargar Datos')
)

normalize_data = st.Page(
    'pages/process/normalize_data.py',
    title='Normalizar Datos',
    icon='🧹'
)

dashboard = st.Page(
    'pages/dashboard/dashboard.py',
    title='dashboard',
    icon='📊',
    default=(window == 'Dashboard')
)

performance = st.Page(
    'pages/performance/performance_fns.py',
    title='Rendimiento',
    icon='🚀',
    default=(window == 'Rendimiento')
)

inicio = [index_page]
dashboard_pages = [dashboard]
performance_pages = [performance]
process_pages = [load_data, normalize_data]

st.logo('🎓')

page_dictionary = {}

if st.session_state.window == 'Cargar Datos':
    page_dictionary['Cargar Datos'] = process_pages

if st.session_state.window == 'Dashboard':
    page_dictionary['Dashboard'] = dashboard_pages

if st.session_state.window == 'Rendimiento':
    page_dictionary['Rendimiento'] = performance_pages


if len(page_dictionary) > 0:
    page = st.navigation({'Inicio': inicio} | page_dictionary)
else:
    page = st.navigation([st.Page(index)])

page.run()