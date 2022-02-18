# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 11:45:25 2022

@author: walla
"""

# Import libraries
import pandas as pd
import numpy as np

# Assign columns names
col_names = ['ID_TURMA', 'IN_DISC_LINGUA_PORTUGUESA',
             'IN_DISC_EDUCACAO_FISICA', 'IN_DISC_ARTES', 'IN_DISC_LINGUA_INGLES',
             'IN_DISC_LINGUA_ESPANHOL', 'IN_DISC_LINGUA_FRANCES', 'IN_DISC_LINGUA_OUTRA',
             'IN_DISC_LIBRAS', 'IN_DISC_LINGUA_INDIGENA', 'IN_DISC_PORT_SEGUNDA_LINGUA',
             'IN_DISC_MATEMATICA', 'IN_DISC_CIENCIAS', 'IN_DISC_FISICA', 
             'IN_DISC_QUIMICA', 'IN_DISC_BIOLOGIA', 'IN_DISC_HISTORIA', 
             'IN_DISC_GEOGRAFIA', 'IN_DISC_SOCIOLOGIA', 'IN_DISC_FILOSOFIA',
             'IN_DISC_ESTUDOS_SOCIAIS', 'IN_DISC_EST_SOCIAIS_SOCIOLOGIA',
             'IN_DISC_INFORMATICA_COMPUTACAO', 'IN_DISC_ENSINO_RELIGIOSO',
             'IN_DISC_PROFISSIONALIZANTE', 'IN_DISC_ESTAGIO_SUPERVISIONADO',
             'IN_DISC_PEDAGOGICAS', 'IN_DISC_OUTRAS'
             ]

# Load csv file
classes = pd.read_csv('C:/Users/walla/Desktop/microdados_censo_escolar_2020/DADOS/turmas.CSV',
                      encoding = 'unicode_escape',
                      sep='|',
                      usecols=col_names)

# Load dictionary of TP_ETAPA_ENSINO
dict_disc = np.load('C:/Users/walla/Desktop/microdados_censo_escolar_2020/dict_disc.npy', allow_pickle=True).item()

# Create function columns_to_dict
def columns_to_dict(school_class):
  
    # Drop disciplines with values 0 or nan
    for key, value in school_class.items():
        if value == 0:
            school_class[key] = np.nan
    
    # If the number of the columns is 27, then the class has no discipline assigned 
    if school_class.isna().sum() == 27:
        dict_class = {int(school_class[0]):''}
    else:
        school_class.dropna(inplace=True)
        
        # Create columns 'Disciplinas' and set it to index
        school_class = pd.DataFrame(school_class)
        school_class.rename(columns = {school_class.columns[0]: 0}, inplace = True)
        school_class.loc[:, 'Disciplinas'] = school_class.index.map(dict_disc)
        school_class.set_index('Disciplinas', inplace=True)
    
        # Create str 'disc' and get all disciplines of the class
        disc = str()
        for key in school_class.index:
            disc = disc + ', ' + key    
        disc = disc.split(' ', 2)[2]
        
        # Create dictionary to assign key 'ID_TURMA' and value 'disc'
        dict_class = {int(school_class[0][0]):disc}
    
    return dict_class

# Create dictionary
dict_total = dict()

# For loop to iterate over all dataframe classes and assign key 'ID_TURMA' 
# and value 'disc' to dict_total
for i in range(len(classes)):
    dict_aux = columns_to_dict(classes.loc[i, :])
    dict_total[list(dict_aux.keys())[0]] = dict_aux[list(dict_aux.keys())[0]]

# Save
np.save('dict_disc_total.npy', dict_total) 
