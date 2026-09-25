import streamlit as st
import csv

st.header('Datos')
file = st.file_uploader(
    'Seleccione el archivo a cargar',
    help='El archivo tiene que ser en extension .csv',
    type='csv',
    key='file',
    max_upload_size=500, 
    accept_multiple_files=False
)

st.divider()
st.write('##### Previsualización')

if st.session_state.file is not None:
    with open(file, mode='r', encoding='utf-8-sig') as archivo:
        lector = csv.reader(archivo)


    print(lector)
    # st.write(lector)
    # df = pd.read_csv(st.session_state.file)
    # st.write(df)
    # save_data = st.button('Seleccionar Archivo', type='primary')
