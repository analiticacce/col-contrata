import pandas as pd
import matplotlib.pyplot as plt
import json
import re

# Paquetes de consulta a traves de Socrata

from sodapy import Socrata
    
identificador_columnas=pd.read_csv('datos/identificador_columnas.csv')
valor_columnas={'SECOP I':'API_DA_S_I','SECOP II':'API_DA_S_II','TVEC':'API_DA_S_TVEC'}
identificador_columnas=identificador_columnas[['Unificado','API_DA_S_I', 'API_DA_S_II']]
identificador_columnas=identificador_columnas.dropna()
identificador_columnas=identificador_columnas.set_index('Unificado')
identificador_columnas.drop('Fuente',axis=0,inplace=True)
identificador_datos={'SECOP I':'f789-7hwg','SECOP II':'jbjy-vk9h','TVEC':'rgxm-mmea'}
valor_columnas={'SECOP I':'API_DA_S_I','SECOP II':'API_DA_S_II','TVEC':'API_DA_S_TVEC'}
### Definición de cliente para Socrata

cliente=Socrata('www.datos.gov.co',None,timeout=1000000)
with open('datos/dptos.json') as json_file:
    dptos = json.load(json_file)