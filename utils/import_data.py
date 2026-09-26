import csv
import io
import pandas as pd
import time

def get_data_lib_csv(file):
    inicio = time.perf_counter()
    string_data = file.getvalue().decode('utf-8')
    
    io_string =io.StringIO(string_data)
    lector_dictionary = csv.DictReader(io_string)

    data_list = list(lector_dictionary)    
    fin = time.perf_counter()

    return inicio, fin, data_list

def get_data_lib_pandas(file):
    inicio = time.perf_counter()
    df = pd.read_csv(file)
    fin = time.perf_counter()

    return inicio, fin, df
