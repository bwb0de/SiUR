#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2017 Daniel Cruz <bwb0de@bwb0dePC>
#  Version 0.1
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import json
import os

from collections import OrderedDict

from modules.py_obj_data_tools import PickleDataType
from modules.cli_tools import select_op, input_num, input_op, verde, show_dict_data, read_input, sim_ou_nao, vermelho, pick_options, amarelo
from modules.siur_pastas_de_dados import pasta_equipamentos, pasta_sons_fx
from modules.siur_sound import select_snd, play_fxsnd

lista_de_ocultabilidade = ['Bolso', 'Jaqueta', 'Sobretudo']
lista_de_disponibilidade = ['Comum', 'Restrito', 'Raro', 'Único/Artesanal']
lista_de_categorias_danos = ['Cortante', 'Contundente', 'Contucortante', 'Perfurante', 'Corrosivo', 'Queimante']
lista_de_tipo_danos = ['Significativo', 'Letal', 'Agravado']
lista_de_alcances_armas_brancas = ['Insignificante', 'Curto', 'Médio', 'Longo', 'Muito longo', 'Extremamente longo']
lista_de_materiais_armas = ['Pedra', 'Ferro', 'Aço', 'Madeira', 'Prata']
lista_de_materiais_vestes = ['Lã', 'Algodão', 'Couro', 'Ferro', 'Aço', 'Bambu']

class Equipamento(PickleDataType):
        def __init__(self):
                def definir_dados_gerais():
                        output  = OrderedDict()
                        output['Nome'] = read_input(input_label="Nome do item/equipamento")
                        output['Disponibilidade'] = pick_options(selection_list=lista_de_disponibilidade, input_label='Disponibilidade')
                        output['Ocultabilidade'] = pick_options(selection_list=lista_de_ocultabilidade, input_label="Ocultabilidade")
                        output['Material'] = pick_options(selection_list=lista_de_materiais_armas, input_label="De que é feita a arma em questão?")
                        output['Peso'] = read_input(input_label='Peso (kg)', dada_type='float')
                        output['Preço'] = read_input(input_label="Preço", dada_type='int', default=estimar_preco())
                        return output
                
                def estimar_preco(disponibilidade, material, peso):
                        return 0

                super(Equipamento, self).__init__()
                self.dados_gerais = definir_dados_gerais()
                self.ultimo_possuidor = ''
                self.target_folder = pasta_equipamentos


class ArmaBranca(Equipamento):
        def __init__(self):
                def redefinir_dados_gerais(dados_gerais):
                        dados_gerais['Categoria'] = 'Arma'
                        dados_gerais['Tipo'] = 'Arma Branca'
                        dados_gerais['Alcance'] = pick_options(selection_list=lista_de_alcances_armas_brancas,input_label="Qual o alcance da arma branca?", )
                        default_explosao, default_velocidade_recuperacao, default_velocidade_manobra, default_velocidade_saque = calcular_velociade_padrao()
                        dados_gerais['Velocidade de saque'] = read_input(input_label="Qual a velocidade do saque?", dada_type='int', default=default_velocidade_saque)
                        dados_gerais['Número de mãos'] = read_input(input_label="Quantas mãos são necessárias para o uso?", dada_type='int', default=1)
                        dados_gerais['Explosão'] = read_input(input_label="Qual o valor mínimo da característica Explosão?", dada_type='int', default=1)
                        dados_gerais['Manobras'] = adicionar_manobra(default_explosao, default_velocidade_recuperacao, default_velocidade_manobra)
                        return dados_gerais


                def calcular_velociade_padrao():
                        if self.dados_gerais['Alcance'] == 'Insignificante' or self.dados_gerais['Alcance'] == 'Curto':
                             #exp. rec. manobra. saque
                                return 2, 1, 2, 6
                        
                        elif self.dados_gerais['Alcance'] == 'Médio':
                                return 3, 2, 3, 8
                                
                        elif self.dados_gerais['Alcance'] == 'Longo':
                                return 3, 3, 4, 8
                                
                        elif self.dados_gerais['Alcance'] == 'Muito longo':
                                return 4, 3, 4, 8
                                
                        elif self.dados_gerais['Alcance'] == 'Extremamente longo':
                                return 5, 4, 5, 12


                def adicionar_manobra(default_explosao, default_velocidade_recuperacao, default_velocidade_manobra):
                        output = OrderedDict()

                        while True:
                                nome_manobra = read_input(input_label='Nome da manobra')
                                output[nome_manobra] = OrderedDict()
                                output[nome_manobra]['Tipo de dano'] = pick_options(selection_list=lista_de_tipo_danos, input_label="Quais os tipos de dano a arma pode provocar?")
                                output[nome_manobra]['Categoria de dano'] = pick_options(selection_list=lista_de_categorias_danos, input_label="Como o dano desta manobra é categorizado?")
                                output[nome_manobra]['Magnitude do dano'] = read_input(input_label="Proporção margem:dano", data_pattern=r'\d\:\d', waring_msg='Utilizar o formato #:# para este campo...')
                                output[nome_manobra]['Velocidade da manobra'] = read_input(input_label='Velocidade da manobra', dada_type='int', default=default_velocidade_manobra)
                                output[nome_manobra]['Tempo de recuperação'] = read_input(input_label='Tempo de recuperação', dada_type='int', default=default_velocidade_recuperacao)
                                output[nome_manobra]['Som: ataque'] = False
                                output[nome_manobra]['Som: ataque-aparado'] = False
                                output[nome_manobra]['Som: ataque-bloqueado'] = False
                                output[nome_manobra]['Som: ataque-erro/esquiva'] = False
                                op = sim_ou_nao(input_label="Inserir sons para a manobra?")
                                if op == 's':
                                        output[nome_manobra]['Som: ataque'] = select_snd(pasta_sons_fx)
                                        output[nome_manobra]['Som: ataque-aparado'] = select_snd(pasta_sons_fx)
                                        output[nome_manobra]['Som: ataque-bloqueado'] = select_snd(pasta_sons_fx)
                                        output[nome_manobra]['Som: ataque-erro/esquiva'] = select_snd(pasta_sons_fx)
                                op = sim_ou_nao(input_label="Registrar outra manobra?")
                                if op == 'n': break
                        
                        return output

                super(ArmaBranca, self).__init__()
                self.dados_gerais = redefinir_dados_gerais(self.dados_gerais)
                self.persist(fname=self.dados_gerais['Nome'], file_ext='.siurab')


        def listar_manobras(self):
                return list(self.dados_gerais['Manobras'].keys())


        def mostrar_manobras(self):
                output = 'Manobras:'
                for manobra in self.listar_manobras():
                        output += os.linesep + '  »' + amarelo(manobra)
                        output += os.linesep + '    '
                        
                        for k, v in self.dados_gerais['Manobras'][manobra].items():
                                output += '{}: {}'.format(k,v)
                                output += os.linesep + '    '
                return output


        def play_snd(self, snd_file_ref):
                play_fxsnd(snd_file_ref, filefolder=pasta_sons_fx)

        def info(self):
                output  = vermelho(self.dados_gerais['Nome'])
                output += os.linesep + '{}: {}'.format('Alcance', str(self.dados_gerais['Alcance']))
                output += os.linesep + ' ' + self.mostrar_manobras()
                return output


        def __repr__(self):
                return str(self.dados_gerais['Nome'] + ' (' + self.ultimo_possuidor +')') 

                

class Veste(Equipamento):
        def __init__(self):
                super(Veste, self).__init__()
                self.tipo = 'Veste'
                self.material = pick_options(selection_list=lista_de_materiais_vestes, input_label="De que é feita a veste?")

class Amuleto(Equipamento):
        def __init__(self):
                super(Amuleto, self).__init__()
                self.tipo = 'Amuleto'

class Item(Equipamento):
        def __init__(self):
                super(Item, self).__init__()
                self.tipo = 'Item'

class Alimento(Equipamento):
        def __init__(self):
                super(Alimento, self).__init__()
                self.tipo = 'Alimento'