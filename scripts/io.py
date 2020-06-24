#!/usr/bin/python3
import pandas as pd
import numpy as np
import pandas_gbq
import pydata_google_auth
import gspread
from gcloud import storage
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import os
from os import listdir
import requests
import json
from datetime import datetime
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

import manipulation


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../credentials/gabinete_sv_credentials.json"





def read_sheets(sheet_name, workSheet=0):


    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('../../credentials/gabinete-sv-9aed310629e5.json', scope)
    gc          = gspread.authorize(credentials)
    if workSheet==0:
        wks         = gc.open(sheet_name).sheet1
    else:
        wks = gc.open(sheet_name).worksheet(workSheet)
        
    data        = wks.get_all_values()
    headers     = data.pop(0)

    return pd.DataFrame(data, columns=headers)



def load_variables_geocodes():
    var = pd.read_csv('../data/variaveis_selected.csv')
    mask = (var['tipo']=='agro') | (var['variavel'].str.contains('Série interrompida'))
    var  = var[np.logical_not(mask)]

    geocode_seade = pd.read_csv('../../brasil_geodata/dados/seade_codigo_ibge.csv')
    
    return var, geocode_seade


def load_kpis():
    df = pd.read_csv('../data/dados_consolidados.csv')
    mask = df['variavel']!='missing'
    df = df[mask]

    ddf = manipulation.split_data(df)

    dd = ddf.sort_values(by=['codigo_localidade','periodo','nome_localidade_pai','year'], ascending=False).drop_duplicates(['localidade','variavel'],keep='first').sort_values(by='variavel')

    dh = ddf.sort_values(by=['codigo_localidade','periodo','nome_localidade_pai','year'], ascending=False).sort_values(by=['variavel','ano'])
    
    return dd, dh


