from col_credentials import *
import pandas as pd
import numpy as np
import json
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table
from datetime import date
from IPython.core.display import HTML,display

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


def consulta_mae(departamento,entidad,fecha_firma_inicio,fecha_firma_fin,valor_min,valor_max,cod_unspsc):
    results_detalle=[]
    
    for i in ['SECOP I','SECOP II']:
        queries_list=[]
        results_detalle_dpto=[]
        if cod_unspsc==0:
            aditional_string=""
        else:
            aditional_string=" and {0} like '%{1}%'".format(identificador_columnas[valor_columnas[i]]['UNSPSC'],cod_unspsc) 
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
                ({4}='{18}') and
                ({3} = '{19}') and
                ({16} between '{20}' and '{21}') and
                ({2} between {22} and {23})  
                {24}
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
            identificador_columnas[valor_columnas[i]]['URL'],j,entidad,fecha_firma_inicio,fecha_firma_fin,valor_min,valor_max,aditional_string)
            #print(query_secop_tot)
            queries_list.append(query_secop_tot)
            df_temp=pd.DataFrame(cliente.get(identificador_datos[i], query=query_secop_tot))
            df_temp['fuente']=i
            #print(df_temp.shape)
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

    results_detalle['url']=[url['url'] for url in results_detalle['url'] ]
      
    return results_detalle

def consulta_MAE_simple():
    clas_unspsc=pd.read_csv('datos/clasificador_de_bienes_y_servicios.csv')
    clas_unspsc=clas_unspsc[['Nombre Clase','Código Clase']].drop_duplicates()
    clas_unspsc.set_index('Código Clase',inplace=True)
    app=JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    df=pd.read_csv('datos/contratos_entidad.csv')
    app.layout=html.Div([
        html.H1("Análisis de datos del sistema de compra pública"),
        html.H2("Datos de la compra pública"),
        html.H3("Seleccione el departamento"),
        dcc.Dropdown(
            id='departamento',
            options=[{'label': i, 'value': i} for i in dptos],
            multi=True,
            value='Cundinamarca'),
        html.H3("Seleccione el año"),
        dcc.Dropdown(
            id='anio',
            options=[{'label': i, 'value': i} for i in ['2018','2019','2020','2021','2022']],
            multi=True,
            value='2022'),
        html.H3("Seleccione la entidad"),
        dcc.Dropdown(
            id='dropdown_entidad',
            multi=True,
            value='Todas',
            ),
        
        dbc.Row([
            
            dbc.Col([
            html.Div(id='card_1'),
            html.Div(id='card_2'),
            html.Div(id='card_3'),
            ]),
            dbc.Col([
            dcc.Graph(id='grafica_1'),
            ]),
            dbc.Col([
            dcc.Graph(id='grafica_2'),
            ]),    

    ])
        
    ])
    @app.callback(Output('dropdown_entidad','options'),
                [Input('departamento','value'),
                Input('anio','value'),])
    def update_dropdown_entidad(departamento,anio):
        if departamento is None:
            departamento=dptos
        if anio is None:
            anio=2022
        if type(departamento)==str:
            departamento=[departamento]
        if type(anio)==str:
            anio=[anio]
        lista_consulta=[]
        for dpto in departamento:
            for a in anio:
                a=int(a)
                df_dpto=consulta_datos_departamento(dpto,a)
                lista_consulta.append(df_dpto)
        df=pd.concat(lista_consulta)
        return [{'label': i, 'value': i} for i in list(df['entidad'].unique())+['Todas']]


    @app.callback(
        Output('card_1', 'children'),
        Output('card_2', 'children'),
        Output('card_3', 'children'),
        Output('grafica_1', 'figure'),
        Output('grafica_2', 'figure'),
        Input('departamento', 'value'),
        Input('anio', 'value'),
        Input('dropdown_entidad', 'value'),
        )
    def update_output(departamento,anio,entidad):
        if type(departamento)==str:
            departamento=[departamento]
        if type(anio)==str:
            anio=[anio]
        lista_consulta=[]
        for dpto in departamento:
            for an in anio:
                an=int(an)
                df_temp=consulta_datos_departamento(dpto,an)
                lista_consulta.append(df_temp)
        df=pd.concat(lista_consulta)
        if type(entidad)==str and entidad!='Todas':
            entidad=[entidad]
            df=df[df['entidad'].isin(entidad)]
        if type(entidad)==str and entidad=='Todas':
            None
        else:
            df=df[df['entidad'].isin(entidad)]
        df=df.dropna()
        df=df.drop_duplicates()
        table=dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
        )
        card_1=dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Número de contratos", className="card-title"),
                    html.P(
                        df['cantidad'].sum(),
                        className="card-text",
                    ),
                ]
            ),
            style={"width": "18rem"},
        )
        card_2=dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Valor total de contratos", className="card-title"),
                    html.P(
                        df['suma_valor_contrato'].sum(),
                        className="card-text",
                    ),
                ]
            ),
            style={"width": "18rem"},
        )
        card_3=dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Promedio valor de Contratos", className="card-title"),
                    html.P(
                        df['suma_valor_contrato'].sum()/df['cantidad'].sum(),
                        className="card-text",
                    ),
                ]
            ),
            style={"width": "18rem"},
        ),
        fig1=px.bar(df, x="año", y="suma_valor_contrato", color="departamento_entidad")
        fig2=px.bar(df, x="año", y="cantidad",  color="departamento_entidad")
        return card_1,card_2,card_3,fig1,fig2#,table

    return app.run_server(mode='inline',debug=True)

def consulta_MAE(port=np.random.randint(1000,9999)):
    app=JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    clas_unspsc=pd.read_csv('datos/clasificador_de_bienes_y_servicios.csv')
    clas_unspsc=clas_unspsc[['Nombre Clase','Código Clase']].drop_duplicates()
    clas_unspsc.set_index('Código Clase',inplace=True)
    df=pd.read_csv('datos/contratos_entidad.csv')
    app.layout=html.Div([
        html.H1("Análisis de datos del sistema de compra pública"),
        html.H2("Datos de la compra pública"),
        dbc.Row([            
            dbc.Col([
        html.H3("Seleccione el departamento"),
        dcc.Dropdown(
            id='departamento',
            options=[{'label': i, 'value': i} for i in dptos],
            multi=True,
            value='Cundinamarca'),
            ]),         
            dbc.Col([
        html.H3("Seleccione el valor inicial del rango"),
        dcc.Input(
            id='valor_inicial',
            type='text',
            value='0'),
            ]),
        dbc.Col([
        html.H3("Seleccione el valor final del rango"),
        dcc.Input(
            id='valor_final',
            type='text',
            value='1000000000'),

            ]),
        ])    ,
        dbc.Row([            
            dbc.Col([
        html.H3("Seleccione rango de fechas"),
        dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2000, 1, 1),
        max_date_allowed=date(2023, 1, 1),
        start_date=date(2010,1, 1),
        end_date=date(2022, 9, 30)
    )

            ]),
            dbc.Col([
        html.H3("Seleccione Clase UNSPSC"),
        dcc.Dropdown(
            id='unspsc',
            multi=True,
            options=[{'label': str(i)+' - '+clas_unspsc['Nombre Clase'][i], 'value': str(i)} for i in clas_unspsc.index],
            ),
            ]),
    ]),
        dbc.Row([
                dbc.Col([
        html.H3("Seleccione la entidad"),
        dcc.Dropdown(
            id='dropdown_entidad',
            multi=True,
            value='ALCALDIA ZIPACON',
            ),
            ]),
               ]),
        html.Button("Consultar y descargar CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
        dbc.Row([
            
            dbc.Col([
            html.Div(id='card_1'),
            html.Div(id='card_2'),
            html.Div(id='card_3'),
            ]),
            dbc.Col([
            dcc.Graph(id='grafica_1'),
            ]),
            dbc.Col([
            dcc.Graph(id='grafica_2'),
            ]),    

    ])
        
    ])
    @app.callback(Output('dropdown_entidad','options'),
                [Input('departamento','value'),])
    def update_dropdown_entidad(departamento):
        anio=[str(i) for i in range(2000,2023)]
        if departamento is None:
            departamento=dptos
        if type(departamento)==str:
            departamento=[departamento]
        lista_consulta=[]
        for dpto in departamento:
            for a in anio:
                a=int(a)
                df_dpto=consulta_datos_departamento(dpto,a)
                lista_consulta.append(df_dpto)
        df=pd.concat(lista_consulta)
        return [{'label': i, 'value': i} for i in list(df['entidad'].unique())+['Todas']]


    @app.callback(
        Output('card_1', 'children'),
        Output('card_2', 'children'),
        Output('card_3', 'children'),
        Output('grafica_1', 'figure'),
        Output('grafica_2', 'figure'),
        Output("download-dataframe-csv", "data"),
        Input('departamento', 'value'),
        Input('dropdown_entidad', 'value'),
        Input('valor_inicial', 'value'),
        Input('valor_final', 'value'),
        Input('unspsc', 'value'),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        Input("btn_csv", "n_clicks"),prevent_initial_call=True,
        )
    def update_output(departamento,entidad,valor_inicial,valor_final,unspsc,fecha_inicio,fecha_fin,n_clicks):
        valor_inicial=str(valor_inicial)
        valor_final=str(valor_final)
        fecha_inicio_obj = date.fromisoformat(fecha_inicio)
        fecha_inicio_str = fecha_inicio_obj.strftime('%Y-%m-%d')
        fecha_fin_obj = date.fromisoformat(fecha_inicio)
        fecha_fin_str = fecha_fin_obj.strftime('%Y-%m-%d')
        if type(departamento)==str:
            departamento=[departamento]
        if type(entidad)==str:
            entidad=[entidad]
        if type(unspsc)==str:
            unspsc=[unspsc]      
        if unspsc==None:
            unspsc=['0']  
        lista_consulta=[]


        for dpto in departamento:
            for ent in entidad:
                for u in unspsc:
                    #print(dpto+ "|"+ ent+ "|"+ fecha_inicio+ "|"+ fecha_fin+ "|"+ valor_inicial+ "|"+ valor_final+ "|"+ u)
                    try:
                        
                        df_dpto=consulta_mae(dpto,ent,fecha_inicio,fecha_fin,valor_inicial,valor_final,u)
                        lista_consulta.append(df_dpto)
                    except:
                        None
                        continue
        print(lista_consulta)
        global df
        df=pd.concat(lista_consulta)
        df=df.dropna()
        df=df.drop_duplicates()
        card_1=dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Número de contratos", className="card-title"),
                    html.P(
                        df.shape,
                        className="card-text",
                    ),
                ]
            ),
            style={"width": "18rem"},
        )
        card_2=dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Valor total de contratos", className="card-title"),
                    html.P(
                        df['valor_contrato'].sum(),
                        className="card-text",
                    ),
                ]
            ),
            style={"width": "18rem"},
        )
        card_3=dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Promedio valor de Contratos", className="card-title"),
                    html.P(
                        df['valor_contrato'].sum()/df.shape[0],
                        className="card-text",
                    ),
                ]
            ),
            style={"width": "18rem"},
        ),
        fig1=px.pie(df, values='valor_contrato', names='departamento_entidad', title='Valor de contratos por departamento')
        fig2=px.bar(df, x="modalidad", y="valor_contrato",  color="fuente")
        return card_1,card_2,card_3,fig1,fig2, dcc.send_data_frame(df.to_csv, "mydf.csv")#,table


    return app.run_server(mode='inline',debug=True,port=port)


def consulta_MAE_powerbi():
    display(
        HTML(
            """
            <iframe title="Analisis_de_demanda - V2.2-datos_completos" width="1200" height="900" src="https://app.powerbi.com/view?r=eyJrIjoiMGY4MWZmZmUtNGJlYy00YTBlLTgzYmYtZGE2NGRkZDA1YTJlIiwidCI6IjdiMDkwNDFlLTI0NTEtNDlkMC04Y2IxLTc5ZDVlM2Q4YzFiZSIsImMiOjR9&pageName=ReportSection17ad17361e56dd6a009c" frameborder="0" allowFullScreen="true"></iframe>
            """
            )
    )