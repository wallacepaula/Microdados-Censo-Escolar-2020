# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 11:04:01 2021

@author: walla
"""
# import libraries
import pandas as pd
import numpy as np
from datetime import timedelta

# List columns to load
col_names = ['NU_ANO_CENSO', 'NO_TURMA', 'TX_HR_INICIAL', 'TX_MI_INICIAL',
             'NU_DIAS_ATIVIDADE', 'NU_DURACAO_TURMA', 'TP_ETAPA_ENSINO', 'QT_MATRICULAS',
             'CO_ENTIDADE']

# Load csv file
turmas = pd.read_csv('C:/Users/walla/Desktop/microdados_censo_escolar_2020/DADOS/turmas.CSV',
                     encoding = 'unicode_escape',
                     sep='|',
                     usecols=col_names)

# modesta = 31003280
# Select a specific school and select only normal classes
emmmc = turmas[turmas['CO_ENTIDADE']==31002135].dropna(subset=['TP_ETAPA_ENSINO'])

# Create a DataFrame to summarize general informations about the classes
nome_col = ['Nome', 'Etapa', 'Início', 'Término', 'Duração', 'Qt Alunos']
tab_turma = pd.DataFrame(columns=nome_col)

# Copy name of the classes in 'Nome'
tab_turma.loc[:, 'Nome'] = emmmc['NO_TURMA']

# Create dictionary of TP_ETAPA_ENSINO
dict_etapa = np.load('C:/Users/walla/Desktop/microdados_censo_escolar_2020/dict_etapa.npy', allow_pickle=True).item()

# Create column 'Etapa' mapping the dictionary
tab_turma.loc[:, 'Etapa'] = emmmc['TP_ETAPA_ENSINO'].map(dict_etapa)

# Transform 'TX_HR_INICIAL' and 'TX_MI_INICIAL' in string
time_str = '2020-01-01 ' + emmmc['TX_HR_INICIAL'].astype('int').astype('str') + ':' + emmmc['TX_MI_INICIAL'].astype('int').astype('str')

# Transform time_str into datetime object
time_str = pd.to_datetime(time_str)
    
# Create table 'Início'
for key, value in time_str.items():
    tab_turma.loc[key, 'Início'] = time_str[key].strftime("%H:%M")

# Sort tab_turma by 'Início' and 'Etapa'
tab_turma.sort_values(by=['Início', 'Etapa'], inplace=True)

# Create table 'Duração'
tab_turma['Duração'] = pd.to_datetime(emmmc['NU_DURACAO_TURMA'], unit='m').dt.strftime('%H:%M')

# Create table 'Término'
for key, value in time_str.items():
    aux = {key: time_str[key] + timedelta(minutes=emmmc['NU_DURACAO_TURMA'][key])}
    tab_turma.loc[key, 'Término'] = aux[key].strftime("%H:%M")

# Create table 'Qt Alunos'
tab_turma.loc[:, 'Qt Alunos'] = emmmc['QT_MATRICULAS']