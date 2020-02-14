#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import itertools
import math

from modules.cli_tools import verde, vermelho, input_num
from collections import OrderedDict

def mk_tabela_arremesso():
    output = OrderedDict()
    counter = itertools.count(4)
    l_idx = list(range(4,31))
    l_idx.reverse()
    for n in l_idx:
        output[next(counter)] = math.log(2.055, 1.000+(n/100000))
    return output

tabela_arremesso = mk_tabela_arremesso()

#Aceleração da gravidade
g = 9.8 

#Coeficiente aerodinâmico de uma esfera esfera
coef_aero_esfera = 0.4 

#Densidade do ar em kg/m³
densidade_ar = 1.22

#Raio do projétil
raio_bola_tenis = 0.033

#Conversões
#1 kg/m³ === 1000 g/m³
#1 m² ====== 10000 cm²

#
# Pendente
#
# Buscar densidades de materiais para a partir da massa estimar o volume e,
# a partir do cálculo do volume da esfera, estimar a resistencia aerodinâmica
# automaticamente...
#
# Exemplo: pedra, vidro, frutas, metais...
#

def calculate_speed(indice_arremesso, massa):
    return tabela_arremesso[indice_arremesso] / massa

def calculate_vspeed(indice_arremesso, massa, angulo):
    return calculate_speed(indice_arremesso, massa) * math.sin(math.radians(angulo))

def calculate_hspeed(indice_arremesso, massa, angulo):
    r = calculate_speed(indice_arremesso, massa) * math.cos(math.radians(angulo))
    if r == 0:
        return False
    return r

def calculate_hight(indice_arremesso, massa, angulo):
    vspeed = calculate_vspeed(indice_arremesso, massa, angulo)
    return vspeed**2/(2*g)

def calculate_uptime(indice_arremesso, massa, angulo):
    return calculate_vspeed(indice_arremesso, massa, angulo)/g

def calculate_downtime(indice_arremesso, massa, angulo):
    return calculate_uptime(indice_arremesso, massa, angulo) * 2

def calculate_distance(indice_arremesso, massa, angulo):
    return calculate_hspeed(indice_arremesso, massa, angulo) * calculate_downtime(indice_arremesso, massa, angulo)

def calculate_instant_quantum(downtime):
    return downtime / 0.2

def calculete_distance_per_instant(distance, num_of_instants):
    return distance / num_of_instants

def calculate_maxang(indice_arremesso, massa, altura_limite):
    list_of_angs = list(range(0,91))
    list_of_angs.reverse()
    for ang in list_of_angs:
        h = calculate_hight(indice_arremesso, massa, ang)
        if not h >= altura_limite:
            print('Ângulo máximo de saída permitido:', ang)
            return ang

def calculate_best_ang(indice_arremesso, massa, distancia_do_alvo):
    list_of_angs = list(range(0,91))
    for ang in list_of_angs:
        s = calculate_distance(indice_arremesso, massa, ang)
        if s >= distancia_do_alvo:
            print('Ângulo ideal de saída, conforme distância:', ang)
            return ang


def l0(massa_g, area_frontal, coef_arrasto=coef_aero_esfera, densid_meio=densidade_ar):
    return massa_g / (0.5*coef_arrasto*densid_meio*area_frontal)

def area_frontal_esfera(raio):
    return math.pi*(raio**2)

def f_arrasto(hspeed, area_frontal, coef_arrasto=coef_aero_esfera, densid_meio=densidade_ar):
    return 0.5 * coef_arrasto * area_frontal * densid_meio * hspeed

def desacel(forca_arrasto, massa_g):
    return forca_arrasto/massa_g*1000

def calculate_distance_corrigida(hspeed, tempo_voo, desacel):
    return hspeed*tempo_voo - (desacel*(tempo_voo**2))/2

def show_stats(indice_arremesso, massa, angulo, raio, distancia_do_alvo=0):
    downtime = calculate_downtime(indice_arremesso, massa, angulo)
    speed = calculate_speed(indice_arremesso, massa)
    hspeed = calculate_hspeed(indice_arremesso, massa, angulo)
    s = calculate_distance(indice_arremesso, massa, angulo)

    area_frontal_projetil = area_frontal_esfera(raio)

    f_arr = f_arrasto(hspeed, area_frontal_projetil)

    desacel_projetil = desacel(f_arr, massa)
    num_of_instants = calculate_instant_quantum(downtime)
    altura = calculate_hight(indice_arremesso, massa, angulo)
    s_corrigido_pela_resistencia = calculate_distance_corrigida(hspeed, downtime, desacel_projetil)
    distance_per_instant = calculete_distance_per_instant(s_corrigido_pela_resistencia, num_of_instants)
    if s < distancia_do_alvo:
        instants_til_target = "alvo está muito distante..."    
    else:
        instants_til_target = distancia_do_alvo / distance_per_instant

    final_speed = (speed**2 - 2*desacel_projetil*s_corrigido_pela_resistencia)**0.5
    final_perc_speed = (speed**2 - 2*desacel_projetil*distancia_do_alvo)**0.5
    q_impact = final_perc_speed * massa

    print(verde('Ângulo de saída:'), angulo)
    print(verde('Velocidade de saída: {spd1}m/s ({spd2}km/h):'.format(spd1=speed, spd2=round(speed * 3.6))))
    print(verde('Massa do objeto: {m1}g ({m2}kg)'.format(m1=massa, m2=massa/1000)))
    print(verde('Altura máxima: {h}m'.format(h=altura)))
    print(verde('Tempo de vôo: {tv}s'.format(tv=downtime)))
    print('Velocidade final: ', final_speed)
    print('Q no momento do inpacto:', q_impact)
    if hspeed:
        print(vermelho('Distância sem atrito (m):'), s)
        print(vermelho('Distância com resistencia do ar (m):'), s_corrigido_pela_resistencia)
        print(vermelho('Distância por instante (m):'), distance_per_instant)
        print(vermelho('Instantes até o alvo:'), instants_til_target)