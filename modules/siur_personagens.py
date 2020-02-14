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

import os

from random import randint

from collections import OrderedDict
from modules.cli_tools import read_input, pick_options, sim_ou_nao, pick_options, vermelho, limpar_tela
from modules.siur_pastas_de_dados import pasta_personagens, pasta_especialidades
from modules.py_obj_data_tools import PickleDataType
from modules.py_pickle_handlers import return_object_info_and_location_list
from modules.siur_listas import \
        lista_de_capacidades,\
        lista_de_capacidades_secundarias,\
        lista_de_marcadores,\
        lista_de_comportamentos,\
        lista_de_dados_gerais,\
        lista_de_ferimentos,\
        lista_de_todos_marcadores,\
        lista_de_especialidades


diferenca_explosao_vigor = OrderedDict()
diferenca_explosao_vigor[-5] = 0.02
diferenca_explosao_vigor[-4] = 0.04
diferenca_explosao_vigor[-3] = 0.06
diferenca_explosao_vigor[-2] = 0.08
diferenca_explosao_vigor[-1] = 0.10
diferenca_explosao_vigor[0] = 0.12
diferenca_explosao_vigor[1] = 0.14
diferenca_explosao_vigor[2] = 0.16
diferenca_explosao_vigor[3] = 0.18
diferenca_explosao_vigor[4] = 0.20
diferenca_explosao_vigor[5] = 0.22


class Capacidade:
        def __init__(self, nivel):
                self.nivel = nivel
                self.modificador = 0


class Personagem(PickleDataType):
        def __init__(self, papel_no_enredo, jogador=False):
                def definir_nome_do_arquivo_de_saida():
                        if not jogador:
                                self.filename = self.dados_gerais['Nome']
                                return
                        self.filename = self.dados_gerais['Jogador'] + '-' + self.dados_gerais['Nome']

                def definir_dados_gerais(jogador, papel_no_enredo):
                        output = OrderedDict()
                        output['Jogador'] = jogador
                        output['Papel no enredo'] = papel_no_enredo
                        altura_media = 0
                        for campo in lista_de_dados_gerais:
                                if campo == 'Traços de personalidade':
                                        output[campo] = pick_options(lista_de_comportamentos, input_label="Traços de personalidade")

                                elif campo == 'Especialidade':
                                        output[campo] = pick_options(lista_de_especialidades, input_label="Especialidade")

                                elif campo == 'Sexo':
                                        output[campo] = pick_options(['Masculino', 'Feminino'], input_label="Sexo")
                                        if output[campo] == 'Masculino': altura_media = randint(165, 185) / 100
                                        else: altura_media = randint(155, 175) / 100

                                elif campo == 'Orientação sexual':
                                        output[campo] = pick_options(['Heteroafetiva', 'Homoafetiva'], input_label="Orientação sexual")

                                elif campo == 'Gênero':
                                        output[campo] = pick_options(['Homem sis', 'Homem trans', 'Mulher sis', 'Mulher trans'], input_label="Gênero")

                                elif campo == 'Altura':
                                        output[campo] = read_input(input_label='Altura', dada_type='float', default=altura_media)

                                elif campo == 'Idade':
                                        output[campo] = read_input(input_label='Idade', dada_type='float', default=24)

                                else:
                                        output[campo] = read_input(input_label=campo)
                        return output


                def definir_capacidades(lista_de_capacidades=lista_de_capacidades):
                        print(vermelho('Capacidades:'))
                        output = OrderedDict()
                        for capacidade in lista_de_capacidades:
                                output[capacidade] = Capacidade(read_input(input_label=capacidade, dada_type='int'))
                        return output


                def definir_marcadores(label, lista_de_marcadores):
                        print(vermelho('Marcadores:'))
                        output = OrderedDict()
                        for marcador in lista_de_marcadores:
                                output[marcador] = int(read_input(marcador, 0))
                        return output

                def definir_capacidades_secundarias(lista_de_capacidades=lista_de_capacidades_secundarias):
                        output = OrderedDict()
                        for capacidade_secundaria in lista_de_capacidades:
                                if capacidade_secundaria == 'Iniciativa':
                                        output[capacidade_secundaria] = self.capacidades['Malícia'].nivel + self.capacidades['Reatividade'].nivel + self.capacidades['Integridade'].nivel

                                elif capacidade_secundaria == 'Blindagem':
                                        output[capacidade_secundaria] = OrderedDict()
                                        output[capacidade_secundaria]['Cabeça'] = 0
                                        output[capacidade_secundaria]['Pescoço'] = 0
                                        output[capacidade_secundaria]['Peito'] = 0
                                        output[capacidade_secundaria]['Braços'] = 0
                                        output[capacidade_secundaria]['Mãos'] = 0
                                        output[capacidade_secundaria]['Pernas'] = 0
                                        output[capacidade_secundaria]['Pés'] = 0

                                elif capacidade_secundaria == 'Deslocamento':
                                        output[capacidade_secundaria] = 0

                                elif capacidade_secundaria == 'Salto horizontal':
                                        output[capacidade_secundaria] = self.capacidades['Explosão'].nivel + int(self.capacidades['Coordenação'].nivel/2)

                                elif capacidade_secundaria == 'Salto vertical':
                                        dif_exp_vig = int(self.capacidades['Explosão'].nivel - self.capacidades['Vigor'].nivel)
                                        if self.dados_gerais['Sexo'] == 'Masculino': I = 1.44
                                        elif self.dados_gerais['Sexo'] == 'Feminino': I = 1.42
                                        output[capacidade_secundaria] = self.dados_gerais['Altura'] * I + dif_exp_vig

                                elif capacidade_secundaria == 'Carga':
                                        carga = []
                                        steps = [1] + list(range(2,9,2))
                                        if self.dados_gerais['Idade'] > 12 and self.dados_gerais['Idade'] < 19:
                                                for step in steps:
                                                        step_value = (self.capacidades['Explosão'].nivel + self.capacidades['Vigor'].nivel) * 2 * step
                                                        carga.append(step_value)

                                        elif self.dados_gerais['Idade'] >= 19 and self.dados_gerais['Sexo'] == 'Masculino':
                                                for step in steps:
                                                        step_value = (self.capacidades['Explosão'].nivel + self.capacidades['Vigor'].nivel + 2) * 2 * step
                                                        carga.append(step_value)

                                        elif self.dados_gerais['Idade'] >= 19 and self.dados_gerais['Sexo'] == 'Feminino':
                                                for step in steps:
                                                        step_value = (self.capacidades['Explosão'].nivel + self.capacidades['Vigor'].nivel + 1) * 2 * step
                                                        carga.append(step_value)

                                        elif self.dados_gerais['Idade'] > 6 and self.dados_gerais['Idade'] <= 12:
                                                for step in steps:
                                                        step_value = (self.capacidades['Explosão'].nivel + self.capacidades['Vigor'].nivel - 1) * 2 * step
                                                        carga.append(step_value)

                                        elif self.dados_gerais['Idade'] > 0 and self.dados_gerais['Idade'] <= 6:
                                                for step in steps:
                                                        step_value = (self.capacidades['Explosão'].nivel + self.capacidades['Vigor'].nivel - 2) * 2 * step
                                                        carga.append(step_value)

                                        output[capacidade_secundaria] = carga

                                elif capacidade_secundaria == 'Arremesso':
                                        output[capacidade_secundaria] = (self.capacidades['Explosão'].nivel * 3) + self.capacidades['Coordenação'].nivel
                        return output

                def definir_variaveis_de_combate():
                        output = OrderedDict()
                        output['Mão direita'] = None
                        output['Mão esquerda'] = None
                        output['Usando arma de duas mãos'] = False
                        output['Mão de domínio'] = pick_options(['Mão direita', 'Mão esquerda'], input_label="Mão de domínio")
                        output['Instantes para deslocamento base'] = self.recalcular_modificador_deslocamento()
                        output['Instante de agência'] = 0
                        return output


                def definir_inventario():
                        output = OrderedDict()
                        output['$$$'] = read_input(input_label="Quantidade de recursos ($)", default=100)
                        output['Peso $$$'] = output['$$$'] * 0.08
                        output['Itens'] = []
                        output['Peso itens'] = 0.0
                        return output


                super(Personagem, self).__init__()
                self.dados_gerais = definir_dados_gerais(jogador, papel_no_enredo)
                self.capacidades = definir_capacidades()
                self.vantagens = OrderedDict()
                self.desvantagens = OrderedDict()
                # Criar função para verificar se 'Ambidestria' foi adquirida...
                # Caso contrário proceder à próxima pergunta...
                self.elos = OrderedDict()
                self.marcadores = definir_marcadores('Marcadores', lista_de_todos_marcadores)
                self.capacidades_secundarias = definir_capacidades_secundarias()
                self.inventario = definir_inventario()
                self.combate = definir_variaveis_de_combate()
                self.dados_gerais['Nome'] = read_input(input_label="Que nome desejas dar ao personagem?")
                self.target_folder = pasta_personagens + papel_no_enredo
                self.persist(fname=definir_nome_do_arquivo_de_saida(), file_ext='.siurc')



        def definir_novo_elo(self):
                personagem = read_input(input_label='Nome do personagem')
                valor = read_input(input_label='Qual a quantidade de Elos a serem registrados?')
                self.elos[personagem] = valor
                self.persist()


        def calcular_dano_recebido(self, margem_do_ataque, proporcao_dano, tipo_de_dano):
                margem, dano = proporcao_dano.split(':')
                margem = int(margem)
                dano = int(dano)
                significativo, letal, agravado = 0, 0, 0

                if tipo_de_dano == 'Significativo':
                        while True:
                                if margem <= margem_do_ataque: 
                                        significativo += 1
                                        margem_do_ataque -= margem
                                else: break
                
                elif tipo_de_dano == 'Letal':
                        while True:
                                if margem <= margem_do_ataque:
                                        letal += 1
                                        margem_do_ataque -= margem
                                else:
                                        significativo += margem_do_ataque
                                        margem_do_ataque = 0
                                        break

                elif tipo_de_dano == 'Agravado':
                        while True:
                                if margem <= margem_do_ataque:
                                        agravado += 1
                                        margem_do_ataque -= margem
                                else:
                                        significativo += margem_do_ataque
                                        margem_do_ataque = 0
                                        break

                self.registrar_dano_recebido(significativo, letal, agravado)


        def registrar_dano_recebido(self, significativo, letal, agravado):
                self.marcadores['Significativo'] += significativo
                self.marcadores['Letal'] += letal
                self.marcadores['Agravado'] += agravado
                self.persist()


        def listar_elos(self):
                output = ''
                for personagem in self.elos.keys():
                        output += '\n  -' + personagem + ': ' + str(int(self.elos[personagem]))
                return output


        def adicionar_elos(self, remove=False):
                while True:
                        limpar_tela(self.dados_gerais['Nome'])
                        self.mostrar_elos()
                        if len(self.elos) > 0:
                                limpar_tela('O Elo a ser registrado dereciona-se a algum desses personagens? [s|n]')
                                for personagem in self.elos.keys():
                                        print('  -', personagem)
                                r = sim_ou_nao(['s', 'n'])
                                if r == 's':
                                        personagem = pick_options(list(self.elos.keys()), input_label="Registrar Elo em relação a qual deles?")
                                        valor = read_input('Qual a quantidade de Elos a serem registrados?', 1)
                                        if remove:
                                                self.elos[personagem] -= valor
                                        else:
                                                self.elos[personagem] += valor
                                else:
                                        self.definir_novo_elo()
                        else:
                                self.definir_novo_elo()
                        self.persist()


        def modificar_marcadores(self, marcador, valor):
                self.marcadores[marcador] += valor
                self.persist()


        def recalcular_peso(self):
                self.inventario['Peso itens'] = 0.0
                self.inventario['Peso $$$'] = self.inventario['$$$'] * 0.08
                for item in self.inventario['Itens']:
                        self.inventario['Peso itens'] += item.peso
                self.inventario['Peso itens'] += self.inventario['Peso $$$']
                self.instantes_deslocamento_base = self.recalcular_modificador_deslocamento()

        def recalcular_modificador_deslocamento(self):
                nivel = self.capacidades_secundarias['Carga']
                if self.inventario['Peso itens'] <= nivel[0]:
                        return 1

                elif self.inventario['Peso itens'] <= nivel[1] and self.inventario['Peso itens'] > nivel[0]:
                        return 2

                elif self.inventario['Peso itens'] <= nivel[2] and self.inventario['Peso itens'] > nivel[1]:
                        return 3

                elif self.inventario['Peso itens'] <= nivel[3] and self.inventario['Peso itens'] > nivel[2]:
                        return 4

                elif self.inventario['Peso itens'] <= nivel[4] and self.inventario['Peso itens'] > nivel[3]:
                        return 5



        def incluir_item_no_inventario(self, item):
                item.ultimo_possuidor = self.dados_gerais['Nome']
                self.inventario['Itens'].append(item)
                self.recalcular_peso()
                self.persist()


        def incluir_dinheiro_no_inventario(self, valor):
                self.inventario['$$$'] += valor
                self.recalcular_peso()
                self.persist()


        def largar_item_da_mao(self, mao='Mão direita'):
                item_caido = self.combate[mao]
                self.combate[mao] = False
                self.persist()
                return item_caido



        def largar_item_das_maos_no_chao(self):
                if self.combate['Usando arma de duas mãos']:
                        self.combate['Mão esquerda'] = False
                        self.combate['Usando arma de duas mãos'] = False
                        yield self.largar_item_da_mao()

                elif self.combate['Mão direita'] and self.combate['Mão esquerda']:
                        print('Mão direita:', self.combate['Mão direita'])
                        print('Mão direita:', self.combate['Mão esquerda'])
                        
                        op = pick_options(['Mão direita', 'Mão esquerda', 'Ambas'], input_label='Qual item foi lardado?')
                        
                        if op == 'Mão direita':
                                yield self.largar_item_da_mao()

                        elif op == 'Mão esquerda':
                                yield self.largar_item_da_mao('Mão esquerda')

                        else:
                                maos = ['Mão esquerda', 'Mão direita']
                                
                                for mao in maos:
                                        yield self.largar_item_da_mao(mao)
                
                elif self.combate['Mão esquerda']:
                        yield self.largar_item_da_mao('Mão esquerda')
                

                elif self.combate['Mão direita']:
                        yield self.largar_item_da_mao()


        def deixar_item_do_inventario_no_chao(self, random=False):
                #Usar random em caso de queda acidental...
                if random:
                        random_idx = randint(0,len(self.inventario['Itens'])+1)
                        item_deixado = self.inventario['Itens'].pop(random_idx)
                        self.recalcular_peso()
                        self.persist()
                        yield item_deixado
                
                itens_deixados = pick_options(self.inventario['Itens'], input_label='Selecione os itens que serão deixados no chão')
                for item in itens_deixados:
                        self.inventario['Itens'].remove(item)
                        self.recalcular_peso()
                        self.persist()
                        yield item

        def pegar_item_do_cenario(self, cenario):
                itens = pick_options(cenario.listar_itens_caidos(), input_label="Itens encontrados em {}".format(cenario.nome.lower()), return_index=True)
                itens.sort(reverse=True)
                for item_idx in itens:
                        self.incluir_item_no_inventario(cenario.registrar_retirada_de_itens(item_idx))
                        


        def passar_item_para_outro_personagem(self, personagem_alvo):
                itens_transferidos = pick_options(self.inventario['Itens'], input_label='Selecione os itens que serão transferidos')
                for item in itens_transferidos:
                        self.inventario['Itens'].remove(item)
                        self.recalcular_peso()
                        self.persist()
                        personagem_alvo.incluir_item_no_inventario(item)


        def comprar_item(self, item):
                if item.valor < self.inventario['$$$']:
                        self.inventario['$$$'] -= item.valor
                        self.incluir_item_no_inventario(item)
                else: print('Não há recursos suficientes para comprar o item...')


        def guardar_armas(self):
                if self.combate['Mão direita'] and self.combate['Usando arma de duas mãos']:
                        self.inventario['Itens'].append(self.combate['Mão direita'])
                        self.combate['Mão direita'] = False
                        self.combate['Mão esquerda'] = False
                        self.combate['Usando arma de duas mãos'] = False
                
                elif self.combate['Mão direita']:
                        self.inventario['Itens'].append(self.combate['Mão direita'])
                        self.combate['Mão direita'] = False
                
                if self.combate['Mão esquerda']:
                        self.inventario['Itens'].append(self.combate['Mão esquerda'])
                        self.combate['Mão esquerda'] = False
                
                self.persist()


        def usar_arma(self):
                armas = []
                for arma in self.inventario['Itens']:
                        if arma.categoria == 'Arma':
                                armas.append(arma)
                
                arma_escolhida_idx = pick_options(armas, input_label="Selecione a arma a ser usada:", clear_screen=False, return_index=True)
                arma_escolhida = self.inventario['Itens'][arma_escolhida_idx]

                if self.combate['Usando arma de duas mãos']:
                        print('Você está usando uma arma de suas mãos...')
                        op = pick_options(['Guardar arma', 'Soltar arma'], input_label="O que fazer com a arma em punho?", clear_screen=False)
                        
                        if op == 'Soltar arma':
                                self.largar_item_das_maos_no_chao()

                        else:
                                self.guardar_armas()

                        self.combate['Mão direita'] = False
                        self.combate['Mão esquerda'] = False
                        self.combate['Usando arma de duas mãos'] = False

                if arma_escolhida.num_maos == 2:
                        self.combate['Mão direita'] = self.inventario['Itens'].pop(arma_escolhida_idx)
                        self.combate['Mão esquerda'] = self.combate['Mão direita']
                        self.combate['Usando arma de duas mãos'] = True
                        

                elif arma_escolhida.num_maos == 1:
                        print('Mão direita:', self.combate['Mão direita'])
                        print('Mão esquerda:', self.combate['Mão esquerda'])

                        mao_escolhida = pick_options(['Direita', 'Esquerda'], input_label="Usar em qual mão?", clear_screen=False)
                        if mao_escolhida == 'Direita':
                                self.combate['Mão direita'] = self.inventario['Itens'].pop(arma_escolhida_idx)
                        else:
                                self.combate['Mão esquerda'] = self.inventario['Itens'].pop(arma_escolhida_idx)

                self.persist()

        def mostrar_marcadores_de_estado(self):
                output = ''
                output += 'Marcadores de Estado:'
                output += '\n  -Fome: ' + str(int(self.marcadores['Fome']))
                output += '\n  -Sede: ' + str(int(self.marcadores['Sede']))
                output += '\n  -Fadiga: ' + str(int(self.marcadores['Fadiga']))
                output += '\n  -Sangue: ' + str(int(self.marcadores['Sangue']))
                output += '\n  -Pavor: ' + str(int(self.marcadores['Pavor']))
                output += '\n  -Melancolia: ' + str(int(self.marcadores['Melancolia']))
                output += '\n  -Estresse: ' + str(int(self.marcadores['Estresse']))
                print(output, '\n')


        def mostrar_marcadores_de_ferimento(self):
                output = ''
                output += 'Marcadores de Ferimento:'
                output += '\n  -Superficial: ' + str(int(self.marcadores['Superficial']))
                output += '\n  -Letal: ' + str(int(self.marcadores['Letal']))
                output += '\n  -Agravado: ' + str(int(self.marcadores['Agravado']))
                print(output, '\n')


        def mostrar_elos(self):
                output = ''
                output += 'Elos:'
                output += self.listar_elos()
                print(output, '\n')


        def mostrar_inventario(self):
                output = ''
                output += 'Inventário:'
                for item in self.inventario['Itens']:
                        output += '\n  -' + item.nome
                output += '\n  -Peso total dos itens: ' + str(self.inventario['Peso itens'])
                output += '\n  -$: ' + str(self.inventario['$$$'])
                output += '\n  -Instantes para deslocamento base: ' + str(self.combate['Instantes para deslocamento base'])

                if self.combate['Usando arma de duas mãos']:
                        if self.capacidades['Explosão'].nivel < self.combate['Mão direita'].explosao_minima:
                                output += vermelho('\n  -Arma de duas mãos em uso: ') + str(self.combate['Mão direita'])
                                modificador = (self.combate['Mão direita'].explosao_minima - self.capacidades['Explosão'].nivel) * -10
                                output += vermelho('\n  -Penalidade devido Explosão inferior: ') + str(modificador) + '%'


                else:
                        if self.combate['Mão direita']:
                                output += vermelho('\n  -Arma em uso na mão direita: ') + str(self.combate['Mão direita'])
                                if self.capacidades['Explosão'].nivel < self.combate['Mão direita'].explosao_minima:
                                        modificador = (self.combate['Mão direita'].explosao_minima - self.capacidades['Explosão'].nivel) * -10
                                        output += vermelho('\n  -Penalidade devido Explosão inferior: ') + str(modificador) + '%'
                                if self.combate['Mão de domínio'] == 'Mão esquerda':
                                        output += vermelho('\n  -Penalidade à mão direita (inábil): ') + str(20) + '%'


                        if self.combate['Mão esquerda']:
                                output += vermelho('\n  -Arma em uso na mão esquerda: ') + str(self.combate['Mão esquerda'])
                                if self.capacidades['Explosão'].nivel < self.combate['Mão esquerda'].explosao_minima:
                                        modificador = (self.combate['Mão esquerda'].explosao_minima - self.capacidades['Explosão'].nivel) * -10
                                        output += vermelho('\n  -Penalidade devido Explosão inferior: ') + str(modificador) + '%'
                                if self.combate['Mão de domínio'] == 'Mão direita':
                                        output += vermelho('\n  -Penalidade à mão esquerda (inábil): ') + str(20) + '%'
                print(output, '\n')


        def mostrar_estado(self):
                limpar_tela(self.dados_gerais['Nome'])
                self.mostrar_marcadores_de_estado()
                self.mostrar_marcadores_de_ferimento()
                self.mostrar_elos()
                self.mostrar_inventario()


        def __repr__(self):
                return self.dados_gerais['Nome']




class Humano(Personagem):
        def __init__(self, *args):
                super(Humano, self).__init__(*args)
                self.metatipo = 'Humano'

class Elfo(Personagem):
        def __init__(self, *args):
                super(Elfo, self).__init__(*args)
                self.metatipo = 'Elfo'
                self.elemento = input()

class Orc(Personagem):
        def __init__(self, *args):
                super(Orc, self).__init__(*args)
                self.metatipo = 'Orc'
                self.tribo = input()

class Hobbit(Personagem):
        def __init__(self, *args):
                super(Hobbit, self).__init__(*args)
                self.metatipo = 'Hobbit'
                self.povoado = input()

class Anao(Personagem):
        def __init__(self, *args):
                super(Anao, self).__init__(*args)
                self.metatipo = 'Anão'

class Vampiro(Personagem):
        def __init__(self, *args):
                super(Vampiro, self).__init__(*args)
                self.metatipo = 'Vampiro'
                self.cla = input('Clã')


class Lobisomem(Personagem):
        def __init__(self, *args):
                super(Lobisomem, self).__init__(*args)
                self.metatipo = 'Lobisomem'
                self.lua = input()
                self.tribo = input()
                self.cicatrizes = input()


