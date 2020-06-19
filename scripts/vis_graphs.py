import numpy as np
import pandas as pd

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline

import vis_layout
import matplotlib.pyplot as plt

import geopandas as gpd





def plot_bars(df, var, xx='localidade', yy='valor'):
    
    mask = (df['variavel']==var) & (df['valor']!=' ') 
    # mask = (dd['portal']==1)
    df = df[mask]
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    
    df = df.sort_values(by='valor')


    sp_color = '#0D485A'
    vale_color  = '#FA7609'
    
    
    df['color'] = np.where(df['localidade']=='Total do Estado de São Paulo', sp_color,vale_color)
    
    trace = go.Bar(
                    y=df[xx],
                    x=df[yy],
                    marker_color=df['color'],
                    orientation='h'
            )
    
    data = [trace]
    
    fig = go.Figure(data)
    

    ano = max(df['ano'])
    fig.update_layout({'template': 'plotly_white', 
                       'title': f'{var} - {ano}'})
    
    return fig.update_layout(hovermode = 'y', height=1200), df




def plot_map(df, sp, var, xx='localidade', yy='valor'):
    
    mask = (df['variavel']==var) & (df['valor']!=' ') 
    # mask = (dd['portal']==1)
    df = df[mask]
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    
    da = df.sort_values(by='valor')
    
    
    da = da.merge(sp, on='geocodigo', how='left')
    da = da[da['geocodigo'].notnull()]
    da = gpd.GeoDataFrame(da)

    ano = max(da['ano'])
    
    #Plot Map
    fig = plt.figure(figsize=(25,25))
    ax  = fig.add_subplot(1,1,1)
    ax.set_title(f'{var} - {ano}', fontsize=23)


    missings={
        "color": "white",
        "edgecolor": "red",
        "hatch": "///",
        "label": "Missing values",
    }
    
    legend_kwds={'loc': 'lower left'}
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