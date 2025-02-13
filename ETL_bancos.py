import requests
import pandas as pd
import sqlite3
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime 


#PIPELINE

def extract(url,table_attribs):
    df = pd.DataFrame(columns=table_attribs)
    html = requests.get(url).text
    data = BeautifulSoup(html,'html.parser')

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:

        col = row.find_all('td')

        if len(col) != 0 :
            
            data_dict = {table_attribs[0] : col[1].text.strip(),
                     table_attribs[1] : col[2].text.strip(),
                     }
            
            
            df1 = pd.DataFrame(data_dict,index=[0])
            df = pd.concat([df,df1], ignore_index=True)
    
    return df


def transform(df,csv_path):
    df_csv = pd.read_csv(csv_path)
    dict = df_csv.set_index('Currency').to_dict()['Rate']

    Columns = df.columns
    column = Columns[1]

    df[column] = df[column].astype(float)
    df['MC_GBP_Billion'] = [np.round(x * dict['GBP'],2) for x in df[column]]
    df['MC_EUR_Billion'] = [np.round(x * dict['EUR'],2) for x in df[column]]
    df['MC_INR_Billion'] = [np.round(x * dict['INR'],2) for x in df[column]]
    

    return df


def load_to_csv(df,csv_path):

    df.to_csv(csv_path)

def load_to_db(df,sql_connection,table_name):

    df.to_sql(table_name,sql_connection,if_exists='replace', index = False)

def run_query(query_statement,sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement,sql_connection)
    print(query_output)
   

def log_progress(message): 
    log_file = "log_file2.txt"
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n')


    
conn = sqlite3.connect('Banks.db')
table_name = 'Largest_banks'
query= "SELECT * FROM Largest_banks"
query2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
query3 = "SELECT Name from Largest_banks LIMIT 5"
csv_path = 'largest_banks'
csv = 'exchange_rate.csv'
table_attribs = ['NAME','MC_USD_Billion']
url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'

log_progress('Preliminares completados. Inicio del proceso ETL')

df1 = extract(url,table_attribs)

log_progress('Extracción de datos completa. Inicio del proceso de transformación')

df = transform(df1,csv)

log_progress('Transformación de datos completada. Iniciando proceso de carga')

load_to_csv(df,csv_path)

log_progress('Datos guardados en archivo CSV')

load_to_db(df,conn,table_name)

log_progress('Datos cargados en la base de datos como tabla. Ejecutar la consulta')

run_query(query,conn)
run_query(query2,conn)
run_query(query3,conn)
log_progress('Proceso completado.')

conn.close()