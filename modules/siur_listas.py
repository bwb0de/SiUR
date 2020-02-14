#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os

from modules.py_pickle_handlers import return_object_info_and_location_list
from modules.siur_pastas_de_dados import \
    pasta_especialidades,\
    pasta_cenarios


lista_de_capacidades = ['Explosão', 'Equilíbrio', 'Coordenação', 'Ritmo', 'Vigor', 'Sensibilidade', 'Presença', 'Malícia', 'Integridade', 'Memória', 'Logicidade', 'Determinação', 'Expressividade', 'Eloquência', 'Reatividade']
lista_de_capacidades_secundarias = ['Iniciativa', 'Blindagem', 'Deslocamento', 'Salto horizontal', 'Salto vertical', 'Carga', 'Arremesso']
lista_de_marcadores = ['Fadiga', 'Sede', 'Fome', 'Sangue', 'Pavor', 'Melancolia', 'Estresse']
lista_de_comportamentos = ['Quente', 'Frio', 'Explosivo', 'Opaco', 'Cristalino', 'Brilhante', 'Áspero', 'Suave', 'Ácido']
lista_de_dados_gerais = ['Conceito', 'Mote', 'Traços de personalidade', 'Especialidade', 'Sexo', 'Orientação sexual', 'Gênero', 'Idade', 'Altura']
lista_de_ferimentos = ['Superficial', 'Letal']
lista_de_todos_marcadores = lista_de_marcadores + lista_de_ferimentos

lista_de_especialidades = return_object_info_and_location_list(pasta_especialidades, only_names=True)
lista_de_cenarios = return_object_info_and_location_list(pasta_cenarios, only_names=True)

