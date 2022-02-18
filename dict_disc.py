# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 11:59:57 2022

@author: walla
"""

# Import libraries
import numpy as np

# Dictionary transforming category in csv file into a more readable string
d = {
    'ID_TURMA':'ID_TURMA',
    'IN_DISC_LINGUA_PORTUGUESA':'Português',
    'IN_DISC_EDUCACAO_FISICA': 'Educação Física',
    'IN_DISC_ARTES': 'Artes',
    'IN_DISC_LINGUA_INGLES': 'Inglês',
    'IN_DISC_LINGUA_ESPANHOL': 'Espanhol',
    'IN_DISC_LINGUA_FRANCES': 'Francês',
    'IN_DISC_LINGUA_OUTRA': 'Outra Língua',
    'IN_DISC_LIBRAS': 'Libras',
    'IN_DISC_LINGUA_INDIGENA': 'Língua Indígena',
    'IN_DISC_PORT_SEGUNDA_LINGUA': 'Português - 2ª Língua',
    'IN_DISC_MATEMATICA': 'Matemática',
    'IN_DISC_CIENCIAS': 'Ciências',
    'IN_DISC_FISICA': 'Física',
    'IN_DISC_QUIMICA': 'Química',
    'IN_DISC_BIOLOGIA': 'Biologia',
    'IN_DISC_HISTORIA': 'História',
    'IN_DISC_GEOGRAFIA': 'Geografia',
    'IN_DISC_SOCIOLOGIA': 'Sociologia',
    'IN_DISC_FILOSOFIA': 'Filosofia',
    'IN_DISC_ESTUDOS_SOCIAIS': 'Estudos Sociais',
    'IN_DISC_EST_SOCIAIS_SOCIOLOGIA': 'Sociologia',
    'IN_DISC_INFORMATICA_COMPUTACAO': 'Informática',
    'IN_DISC_ENSINO_RELIGIOSO': 'Ensino Religioso',
    'IN_DISC_PROFISSIONALIZANTE': 'Profissionalizante',
    'IN_DISC_ESTAGIO_SUPERVISIONADO': 'Estágio Supervisionado',
    'IN_DISC_PEDAGOGICAS': 'Disciplinas Pedagógicas',
    'IN_DISC_OUTRAS': 'Outro'
    }

# Save dictionary
np.save('dict_disc.npy', d) 
