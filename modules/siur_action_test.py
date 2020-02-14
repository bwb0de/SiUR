#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from collections import OrderedDict
from modules.py_obj_data_tools import PickleDataType
from modules.siur_personagens import lista_de_capacidades, lista_de_marcadores, lista_de_ferimentos
from modules.cli_tools import select_ops, select_op, input_op, input_num, vermelho, verde, verde_agua, amarelo, branco

lista_de_marcadores += lista_de_ferimentos

percentual_base = OrderedDict()

               #Cap-∑NV
percentual_base['01-01'] = 16
percentual_base['01-02'] = 32
percentual_base['01-03'] = 48
percentual_base['01-04'] = 64
percentual_base['01-05'] = 80
percentual_base['01-06'] = 96
percentual_base['02-02'] = 16
percentual_base['02-03'] = 24
percentual_base['02-04'] = 32
percentual_base['02-05'] = 40
percentual_base['02-06'] = 48
percentual_base['02-07'] = 56
percentual_base['02-08'] = 64
percentual_base['02-09'] = 72
percentual_base['02-10'] = 80
percentual_base['02-11'] = 88
percentual_base['02-12'] = 96
percentual_base['03-03'] = 16
percentual_base['03-04'] = 21
percentual_base['03-05'] = 26
percentual_base['03-06'] = 32
percentual_base['03-07'] = 37
percentual_base['03-08'] = 42
percentual_base['03-09'] = 48
percentual_base['03-10'] = 53
percentual_base['03-11'] = 58
percentual_base['03-12'] = 64
percentual_base['03-13'] = 69
percentual_base['03-14'] = 74
percentual_base['03-15'] = 80
percentual_base['03-16'] = 85
percentual_base['03-17'] = 90
percentual_base['03-18'] = 96
percentual_base['04-04'] = 16
percentual_base['04-05'] = 20
percentual_base['04-06'] = 24
percentual_base['04-07'] = 28
percentual_base['04-08'] = 32
percentual_base['04-09'] = 36
percentual_base['04-10'] = 40
percentual_base['04-11'] = 44
percentual_base['04-12'] = 48
percentual_base['04-13'] = 52
percentual_base['04-14'] = 56
percentual_base['04-15'] = 60
percentual_base['04-16'] = 64
percentual_base['04-17'] = 68
percentual_base['04-18'] = 72
percentual_base['04-19'] = 76
percentual_base['04-20'] = 80
percentual_base['04-21'] = 84
percentual_base['04-22'] = 88
percentual_base['04-23'] = 92
percentual_base['04-24'] = 96
percentual_base['05-05'] = 16
percentual_base['05-06'] = 19
percentual_base['05-07'] = 22
percentual_base['05-08'] = 25
percentual_base['05-09'] = 28
percentual_base['05-10'] = 32
percentual_base['05-11'] = 35
percentual_base['05-12'] = 38
percentual_base['05-13'] = 41
percentual_base['05-14'] = 44
percentual_base['05-15'] = 48
percentual_base['05-16'] = 51
percentual_base['05-17'] = 54
percentual_base['05-18'] = 57
percentual_base['05-19'] = 60
percentual_base['05-20'] = 64
percentual_base['05-21'] = 67
percentual_base['05-22'] = 70
percentual_base['05-23'] = 73
percentual_base['05-24'] = 76
percentual_base['05-25'] = 80
percentual_base['05-26'] = 83
percentual_base['05-27'] = 86
percentual_base['05-28'] = 89
percentual_base['05-29'] = 92
percentual_base['05-30'] = 96
percentual_base['06-06'] = 16
percentual_base['06-07'] = 18
percentual_base['06-08'] = 21
percentual_base['06-09'] = 24
percentual_base['06-10'] = 26
percentual_base['06-11'] = 29
percentual_base['06-12'] = 32
percentual_base['06-13'] = 34
percentual_base['06-14'] = 37
percentual_base['06-15'] = 40
percentual_base['06-16'] = 42
percentual_base['06-17'] = 45
percentual_base['06-18'] = 48
percentual_base['06-19'] = 50
percentual_base['06-20'] = 53
percentual_base['06-21'] = 56
percentual_base['06-22'] = 58
percentual_base['06-23'] = 61
percentual_base['06-24'] = 64
percentual_base['06-25'] = 66
percentual_base['06-26'] = 69
percentual_base['06-27'] = 72
percentual_base['06-28'] = 74
percentual_base['06-29'] = 77
percentual_base['06-30'] = 80
percentual_base['06-31'] = 82
percentual_base['06-32'] = 85
percentual_base['06-33'] = 88
percentual_base['06-34'] = 90
percentual_base['06-35'] = 93
percentual_base['06-36'] = 96

def calcular_bonus(marcador, valor, percentual_base_inicial, personagem):
    percentual_base_final = percentual_base_inicial
    percentual_base_final += personagem.marcadores[marcador].quantidade * int(valor)
    if percentual_base_final > 96:
        return 96
    return percentual_base_final


def calcular_penalidade(marcador, valor, percentual_base_inicial, personagem):
    percentual_base_final = percentual_base_inicial
    percentual_base_final -= personagem.marcadores[marcador].quantidade * int(valor)
    if percentual_base_final < 0:
        return 0
    return percentual_base_final

def calcular_todas_penalidades(lista_de_penalidades, percentual_base_inicial, personagem):
    percentual_base_final = percentual_base_inicial
    for penalidade in lista_de_penalidades:
        marcador = penalidade[0]
        peso = penalidade[1]
        percentual_base_final = calcular_penalidade(marcador, peso, percentual_base_final, personagem)
    return percentual_base_final


def calcular_todos_bonus(lista_bonus, percentual_base_inicial, personagem):
    percentual_base_final = percentual_base_inicial
    for bonus in lista_bonus:
        marcador = bonus[0]
        peso = bonus[1]
        percentual_base_final = calcular_bonus(marcador, peso, percentual_base_final, personagem)
    return percentual_base_final



def calcular_percentual_base(personagem, teste, magnitude_sucesso_parcial=False):
    capacidades = teste.capacidades
    num_capacidades_mobilizadas = len(capacidades)
    soma_nives_capacidades = 0
    for capacidade in capacidades:
        soma_nives_capacidades += personagem.capacidades[capacidade].nivel
    soma_nives_capacidades = int(soma_nives_capacidades)
    percentual_base_key = '{}-{}'.format(str(num_capacidades_mobilizadas).zfill(2), str(soma_nives_capacidades).zfill(2))
    
    # valor do percentual base (pb)

    pb = percentual_base[percentual_base_key]
    pb = calcular_todas_penalidades(teste.penalidades, pb, personagem)
    pb = calcular_todos_bonus(teste.bonus, pb, personagem)

    pb_str = '... ' + str(pb) + '% ...'
    
    if magnitude_sucesso_parcial:
        
        # faixa de sucesso parcial (fsp)
        minimo = pb-magnitude_sucesso_parcial
        maximo = pb+magnitude_sucesso_parcial
        if minimo <= 0: minimo = 1
        if maximo >= 94: maximo = 94
        fsp_str = str(minimo) + '% ... ' + str(maximo) + '%'
        return fsp_str
    return pb_str
        