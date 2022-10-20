from col_credentials import *
import pandas as pd
import numpy as np
import json

def consulta_departamento(departamento):
    results_detalle=[]
    for i in ['SECOP I','SECOP II']:
        queries_list=[]
        results_detalle_dpto=[]
        for j in dptos[departamento]:
            query_secop_tot=""" Select
                {0} as id_contrato,
                {1} as id_proceso,
                {2} as valor_contrato,
                {3} as entidad,
                {4} as departamento_entidad,
                {5} as orden,
                {6} as modalidad,
                {7} as tipo_contrato,
                {8} as codigo_unspsc,
                {9} as objeto_contrato,
                {10} as descripcion_proceso,
                {11} as nombre_proveedor,
                {12} as tipo_documento_proveedor,
                {13} as numero_documento_proveedor,
                {14} as fecha_inicio,
                {15} as fecha_fin,
                {16} as fecha_firma,
                {17} as url

            where
                {4}='{18}'
            limit
                10000000
            """.format(identificador_columnas[valor_columnas[i]]['ID Contrato'],identificador_columnas[valor_columnas[i]]['ID Proceso'],
            identificador_columnas[valor_columnas[i]]['Valor del contrato'],
            identificador_columnas[valor_columnas[i]]['Entidad'],identificador_columnas[valor_columnas[i]]['Departamento Entidad'],
            identificador_columnas[valor_columnas[i]]['Orden'],identificador_columnas[valor_columnas[i]]['Modalidad'],
            identificador_columnas[valor_columnas[i]]['Tipo de contrato'],identificador_columnas[valor_columnas[i]]['UNSPSC'],
            identificador_columnas[valor_columnas[i]]['Objeto Contrato'],identificador_columnas[valor_columnas[i]]['Descripción proceso'],
            identificador_columnas[valor_columnas[i]]['Nombre Proveedor'],identificador_columnas[valor_columnas[i]]['Tipo de documento proveedor'],
            identificador_columnas[valor_columnas[i]]['Documento Proveedor'],identificador_columnas[valor_columnas[i]]['Inicio de contrato'],
            identificador_columnas[valor_columnas[i]]['Fin de contrato'],identificador_columnas[valor_columnas[i]]['Fecha de Firma'],
            identificador_columnas[valor_columnas[i]]['URL'],j)
            queries_list.append(query_secop_tot)
            df_temp=pd.DataFrame(cliente.get(identificador_datos[i], query=query_secop_tot))
            df_temp['fuente']=i
            if df_temp.shape[0]>0:
                results_detalle_dpto.append(df_temp)
        if len(results_detalle_dpto)>0:
            results_detalle.append(pd.concat(results_detalle_dpto))
    results_detalle=pd.concat(results_detalle)
    results_detalle.reset_index(inplace=True)
    results_detalle.drop('index',axis=1,inplace=True)
    results_detalle['valor_contrato']=results_detalle['valor_contrato'].astype(float)
    results_detalle['departamento_entidad']=results_detalle['departamento_entidad'].replace('Distrito Capital de Bogotá','Bogotá DC')\
    .replace('San Andrés Providencia y Santa Catalina','San Andrés, Providencia y Santa Catalina').replace('Norte De Santander','Norte de Santander')
      
    return results_detalle

def consulta_datos_departamento(departamento,año):
    df_consulta=pd.read_csv('datos/contratos_entidad.csv')
    df_consulta=df_consulta[df_consulta['departamento_entidad']==departamento]
    df_consulta=df_consulta[df_consulta['año']==año]
    df_consulta['suma_valor_contrato']=df_consulta['suma_valor_contrato'].astype(float)
    df_consulta['cantidad']=df_consulta['cantidad'].astype(int)
    df_consulta['departamento_entidad']=df_consulta['departamento_entidad'].replace('Distrito Capital de Bogotá','Bogotá DC')\
    .replace('San Andrés Providencia y Santa Catalina','San Andrés, Providencia y Santa Catalina').replace('Norte De Santander','Norte de Santander')
    return df_consulta