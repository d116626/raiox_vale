import pandas as pd
import numpy as np




def split_data(df):
    df['ano'] = df['ano'].str.replace("'","").str.replace("{","").str.replace("}","").apply(lambda x: x.split(":"))    
    df['valor']  = df['ano'].apply(lambda x: x[1])
    df['ano']  = df['ano'].apply(lambda x: x[0])
    df['valor'] = df['valor'].str.replace('.','').str.replace(',','.')
    
    return(df)


def merge_data(dd,dh_history, var, geocode_seade):
    dd = dd.merge(var,on='variavel', how='inner')

    dd['codigo_localidade'] = dd['codigo_localidade'].astype(int) 
    dd = dd.sort_values(by=['variavel','codigo_localidade'])

    cols = ['codigo_localidade','nome_localidade_pai','codigo_variavel','loc','year']
    dd = dd.drop(cols,1)


    mask = (dd['portal']==1)
    dd = dd[mask]

    dd = dd.merge(geocode_seade,on='localidade', how='left')
    
    dd['localidade'] = dd['localidade'].str.replace('Total do Estado de São Paulo','Estado de São Paulo').str.replace('Região Metropolitana do Vale do Paraíba e Litoral Norte','Vale do Paraíba e Litoral Norte')
    
    
    
    
    
    ### Create Vale Values from cities values
    dd['valor'] = pd.to_numeric(dd['valor'], errors='coerce')
    dd['cities'] = 1


    mask  = (dd['valor'].isnull()) | (dd['localidade'].isin(['Vale do Paraíba e Litoral Norte','Estado de São Paulo']))

    dd_vale = dd[np.logical_not(mask)].groupby(by=['variavel'], as_index=False).agg(
        {
            'unidade':'last',
            'periodo':'last',
            'ano':'max',
            'valor':sum,
            'tipo':'last',
            'portal':'last',
            'cities':sum,
            'absolute':'last',
            'percapta':'last'

        }
    )
    dd_vale['valor'] = np.where(dd_vale['absolute']==0,round(dd_vale['valor']/dd_vale['cities'],2),dd_vale['valor'])
    dd_vale = dd_vale.drop(columns=['cities'])


    dd = dd.drop(columns=['cities'])


    dd_vale['localidade'] = 'Vale do Paraíba e Litoral Norte'
    dd_vale['geocodigo'] = np.nan
    dd_vale = dd_vale[dd.columns]

    mask  = (dd['localidade'].isin(['Vale do Paraíba e Litoral Norte']))
    dd = dd[np.logical_not(mask)]
    dd = pd.concat([dd,dd_vale], axis=0)

    dd = dd.sort_values(by=['variavel','localidade'])


    ### Add Population data
    mask = dh_history['variavel']=='População'
    df_populacao = dh_history[mask]
    df_populacao['valor'] = df_populacao['valor'].str.replace('NA','2309772')
    df_populacao['localidade'] = df_populacao['localidade'].str.replace('Total do Estado de São Paulo','Estado de São Paulo').str.replace('Região Metropolitana do Vale do Paraíba e Litoral Norte','Vale do Paraíba e Litoral Norte')
    df_populacao = df_populacao[['localidade','ano','valor']].rename(columns={'valor':'populacao'})
    
    
    dd = dd.merge(df_populacao, how = 'left', on=['localidade','ano'])

    dd['sufix'] = ''
    
    
    # ### Normalize by 10**5 population
    mask = ((dd['absolute']==1)  & (dd['percapta']==0) & (dd['valor'].notnull()) & (dd['variavel']!='População') ) 
    dd['valor'] = np.where(mask, np.int64((dd['valor']/dd['populacao'].astype(int))*10**5),dd['valor'])
    dd['sufix'] = np.where(mask, 'a cada 100 mil habitantes', dd['sufix'])

    mask = ((dd['absolute']==1)  & (dd['percapta']==1) & (dd['valor'].notnull()) & (dd['variavel']!='População') )
    dd['valor'] = np.where(mask, np.int64((dd['valor']/dd['populacao'].astype(int))),dd['valor'])
    dd['sufix'] = np.where(mask, 'per capita', dd['sufix'])

    return dd