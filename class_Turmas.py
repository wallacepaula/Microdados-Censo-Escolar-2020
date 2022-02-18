# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 20:50:06 2022

@author: walla
"""

# import libraries
import pandas as pd
import numpy as np
from datetime import timedelta

col_names = ['NU_ANO_CENSO', 'NO_TURMA', 'TX_HR_INICIAL', 'TX_MI_INICIAL',
             'NU_DIAS_ATIVIDADE', 'NU_DURACAO_TURMA', 'TP_ETAPA_ENSINO',
             'QT_MATRICULAS','CO_ENTIDADE', 'ID_TURMA']

# Load csv file
classes = pd.read_csv('C:/Users/walla/Desktop/microdados_censo_escolar_2020/DADOS/turmas.CSV',
                      encoding = 'unicode_escape',
                      sep='|',
                      usecols=col_names)

# Load dictionary of TP_ETAPA_ENSINO
dict_etapa = np.load('C:/Users/walla/Desktop/microdados_censo_escolar_2020/dict_etapa.npy', allow_pickle=True).item()

# Load dictionary of 'ID_TURMA' and 'Disciplinas'
dict_disc_total = np.load('C:/Users/walla/Desktop/microdados_censo_escolar_2020/dict_disc_total.npy', allow_pickle=True).item()

class Turmas:
    
    def __init__(self, cod_inep):
        self.cod_inep = cod_inep
        self.school = classes[classes['CO_ENTIDADE']==self.cod_inep].dropna(subset=['TP_ETAPA_ENSINO'])
    
    def summary(self):
        # Create a DataFrame to summarize general informations about the classes
        table = pd.DataFrame(columns=['Etapa', 'Qt Turmas', 'Qt Alunos'])
        
        # Group By 'TP_ETAPA_ENSINO'
        group = self.school.groupby(by=['TP_ETAPA_ENSINO'])
        
        # Create columns 'Qt Turmas'
        table.loc[:, 'Qt Turmas'] = group.count()['QT_MATRICULAS']
        
        # Create columns 'Qt Alunos'
        table.loc[:, 'Qt Alunos'] = group['QT_MATRICULAS'].sum()
        
        # Crete column 'Etapa' and set it to index
        table.loc[:, 'Etapa'] = table.index.map(dict_etapa)
        table.set_index('Etapa', inplace=True)
        
        # Calculate total values of each column
        table.loc['Total', 'Qt Turmas'] = sum(table['Qt Turmas'])
        table.loc['Total', 'Qt Alunos'] = sum(table['Qt Alunos'][0:-1])
        
        return table
    
    def table(self):
        
        # Create a DataFrame to summarize general informations about the classes
        table = pd.DataFrame(columns=['Nome', 'Etapa', 'Início', 'Término',
                                      'Duração', 'Qt Alunos', 'Disciplinas'])
    
        # Copy name of the classes in 'Nome'
        table.loc[:, 'Nome'] = self.school['NO_TURMA']
        
        # Create column 'Etapa' mapping the dictionary
        table.loc[:, 'Etapa'] = self.school['TP_ETAPA_ENSINO'].map(dict_etapa)
        
        # Create column 'Qt Alunos'
        table.loc[:, 'Qt Alunos'] =  self.school['QT_MATRICULAS']
        
        # Create column 'Duração'
        table['Duração'] = pd.to_datetime(self.school['NU_DURACAO_TURMA'], unit='m').dt.strftime('%H:%M')
        
        # Transform 'TX_HR_INICIAL' and 'TX_MI_INICIAL' in datetime object
        time_str = '2020-01-01 ' + self.school['TX_HR_INICIAL'].astype('int').astype('str') + ':' + self.school['TX_MI_INICIAL'].astype('int').astype('str')
        time_str = pd.to_datetime(time_str)
        
        # Create column 'Início' and 'Término'
        for key, value in time_str.items():
            aux = {key: time_str[key] + timedelta(minutes=self.school['NU_DURACAO_TURMA'][key])}
            table.loc[key, 'Início'] = time_str[key].strftime("%H:%M")
            table.loc[key, 'Término'] = aux[key].strftime("%H:%M")
        
        # Create column 'Disciplinas'
        table.loc[:, 'Disciplinas'] = self.school['ID_TURMA'].map(dict_disc_total)
        
        table.sort_values(by=['Início', 'Etapa'], inplace=True)
        
        return table