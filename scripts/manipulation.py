import pandas as pd
import numpy as np




def split_data(df):
    df['ano'] = df['ano'].str.replace("'","").str.replace("{","").str.replace("}","").apply(lambda x: x.split(":"))    
    df['valor']  = df['ano'].apply(lambda x: x[1])
    df['ano']  = df['ano'].apply(lambda x: x[0])
    df['valor'] = df['valor'].str.replace('.','').str.replace(',','.')
    
    return(df)


def merge_data(dd, var, geocode_seade):
    dd = dd.merge(var,on='variavel', how='inner')

    dd['codigo_localidade'] = dd['codigo_localidade'].astype(int) 
    dd = dd.sort_values(by=['variavel','codigo_localidade'])

    cols = ['codigo_localidade','nome_localidade_pai','codigo_variavel','loc','year']
    dd = dd.drop(cols,1)


    mask = (dd['portal']==1)
    dd = dd[mask]

    dd = dd.merge(geocode_seade,on='localidade', how='left')
    
    dd['localidade'] = dd['localidade'].str.replace('Total do Estado de São Paulo','Estado de São Paulo').str.replace('Região Metropolitana do Vale do Paraíba e Litoral Norte','Vale do Paraíba e Litoral Norte')
    
    return dd