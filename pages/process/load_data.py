import streamlit as st
import csv
import io
import os

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

if file is not None:
    string_data = file.getvalue().decode('utf-8')

    io_string =io.StringIO(string_data)
    lector_dictionary = csv.DictReader(io_string)

    # lector_csv = csv.reader(io_string)

    data_list = list(lector_dictionary)

    if data_list:
        st.write('##### Previsualización')
        st.dataframe(data_list)

        file_name = st.text_input(
            'Renombrar al archivo',
            value=file.name
        )

        save_data = st.button('Guardar Archivo en el Servidor', type='primary')

        if save_data:
            server_folder = './data/raw'

            complete_path = os.path.join(server_folder, file_name)
            st.write(complete_path)

            try:
                if not os.path.exists(server_folder):
                    os.makedirs(server_folder)

                with open(complete_path, 'wb') as f:
                    f.write(file.getbuffer())

                    st.success(f'✅ Archivo Guardado Correctamente en: {complete_path}')
            except Exception as e:
                st.error(f'❌ Error al Guardar el Archivo: {e}')
    else:
        st.warning("⚠️ No se pudieron cargar los datos.")

    


