import numpy as np
import pandas as pd

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline

import vis_layout
import matplotlib.pyplot as plt

import geopandas as gpd

import unidecode


def variable_name_file_name(dd,var_file,var):
    df =  dd[(dd['variavel']==var)]
    
    ano = max(df['ano'])
    if (max(df['absolute']==1)  & (df['variavel'].unique().tolist()[0] != 'População')) :
        var_name = f'{var} a cada 100 mil habitantes ({ano})'
    else:
        var_name = f'{var} ({ano})'
    
    file_name = unidecode.unidecode(var.lower().replace(' ','_').replace('-',''))
    var_file[var_name] = file_name
    
    return var_file, file_name



def plot_bars(df, var,themes ,xx='localidade', yy='valor'):
    
    mask = (df['variavel']==var) & (df['valor']!=' ') 
    # mask = (dd['portal']==1)
    df = df[mask]
    
    df = df.fillna(0)
    df = df.sort_values(by='valor')

    sp_color = '#0D485A'
    vale_color  = '#FA7609'
    
    
    df['color'] = np.where((df['localidade']=='Estado de São Paulo') | (df['localidade']=='Vale do Paraíba e Litoral Norte'), sp_color,vale_color)
    
    trace = go.Bar(
                    y=df[xx],
                    x=df[yy],
                    marker_color=df['color'],
                    orientation='h'
            )
    
    data = [trace]
    
    ano = max(df['ano'])
    
    title = f'{var} - {ano}'
    
    layout = vis_layout.get_layout(themes,title)
    
    
    
    fig = go.Figure(data=data, layout=layout)

    
    return fig



def plot_map(df, sp, var, xx='localidade', yy='valor'):
    
    mask = (df['variavel']==var) & (df['valor']!=' ')
    # mask = (dd['portal']==1)
    df = df[mask]
    
    
    mask = df['localidade'].isin(['Vale do Paraíba e Litoral Norte','Estado de São Paulo'])
    df = df[np.logical_not(mask)]
    
    df['valor'] = np.where(df['valor']==0, np.nan, df['valor'])
    
    
    da = df.sort_values(by='valor')
    
    
    da = da.merge(sp, on='geocodigo', how='left')
    da = da[da['geocodigo'].notnull()]
    da = gpd.GeoDataFrame(da)

    # ano = max(da['ano'])
    
    #Plot Map
    fig = plt.figure(figsize=(25,25))
    ax  = fig.add_subplot(1,1,1)
    # ax.set_title(f'{var} - {ano}', fontsize=23)


    missings={
        "color": "white",
        "edgecolor": "black",
        "hatch": "///",
        "label": "Valores Ausentes",
    }
    
    legend_kwds={'loc': 'lower right'}
    edgecolor = "black"
    edge_width = 2.2
    
    
    
    # da.plot(column='valor',ax=ax, legend=True,cmap='Oranges', edgecolor = edgecolor,linewidth=edge_width,\
    #         scheme='user_defined', classification_kwds={'bins':[1, 3, 5,7,9,11]},\
    #         missing_kwds=missings, legend_kwds={'loc': 'lower left'})
    
    
    # df_plot.plot(column=var ,ax=ax, legend=True,cmap='Oranges', edgecolor = "#807158",scheme='quantiles',k=100, missing_kwds=missings
    # df_plot.plot(column=var ,ax=ax, legend=True,cmap='Oranges',missing_kwds=missings, edgecolor = "#807158",scheme='user_defined',classification_kwds={'bins':scale} )

    da.plot(column='valor' ,ax=ax, legend=True,cmap='Oranges', edgecolor = edgecolor, linewidth=edge_width, \
            missing_kwds=missings,legend_kwds=legend_kwds ,scheme='quantiles',k=5)
    
    
    
    ax.axis('off')

    # for idx, row in df_test.iterrows():
    #     plt.annotate(s=row[var_dissolve] + "\n" + str('{:.1f}'.format(row[var])), xy=row['coords'],fontsize=18,
    #                  horizontalalignment='center', color='#360102')


    plt.rc('legend',fontsize=25)


    return fig