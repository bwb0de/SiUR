#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from collections import OrderedDict

from modules.siur_personagens import lista_de_capacidades, lista_de_marcadores, lista_de_ferimentos
from modules.py_obj_data_tools import PickleDataType
from modules.cli_tools import select_ops, select_op, input_op, input_num, verde, limpar_tela, read_input, sim_ou_nao, pick_options
from modules.siur_pastas_de_dados import pasta_testes

lista_de_marcadores += lista_de_ferimentos
lista_de_escopos = ['Pré-combate', 'Combate', 'Cura ou cuidados', 'Embates sociais']
lista_de_tipo = ['Simples', 'Prolongada', 'Disputada', 'Prolongada e diretamente disputada', 'Prolongada e indiretamente disputada', 'Sustentada', 'Colaborativa direta', 'Colaborativa indireta']
 
class Teste(PickleDataType):
    def __init__(self, label):
        def definir_dados_gerais():
            output = OrderedDict()
            output['Nome'] = read_input(input_label="Nome do teste/ação")
            output['Escopo'] = pick_options(lista_de_escopos, input_label='Qual escopo da ação?')
            output['Tipo'] = pick_options(lista_de_tipo, input_label='Qual o tipo da ação?', max_selection=100)
            output['Capacidades'] = pick_options(lista_de_capacidades, input_label='Capacidades mobilizadas', max_selection=100)
            output['Penalidades'] = registrar_penalidades()
            output['Bônus'] = registrar_bonus()
            output['Efeito da vantagem afetiva'] = registrar_efeito_vantagem_afetiva()
            output['Efeito da desvantagem afetiva'] = registrar_efeito_desvantagem_afetiva()
            return output


        def registrar_penalidades():
            penalidades = []
            op = sim_ou_nao(input_label="Registrar marcador de penalidade?")
            if op == 's':
                while not op == 'n':
                    marcador = pick_options(lista_de_marcadores,input_label='Selecione o marcador de penalidade')
                    valor = read_input(input_label='Valor a ser descontado por marcador', dada_type='int')
                    penalidades.append((marcador, valor))
                    op = sim_ou_nao(input_label="Registrar marcador de penalidade?")
            return penalidades

        def registrar_bonus():
            bonus = []
            op = sim_ou_nao(input_label="Registrar marcador de bonificação?")
            if op == 's':
                while not op == 'n':
                    marcador = pick_options(lista_de_marcadores,input_label='Selecione o marcador de bônus')
                    valor = read_input(input_label="Valor a ser somado por marcador", dada_type='int')
                    bonus.append((marcador, valor))
                    op = sim_ou_nao(input_label="Registrar marcador de bônus?")
            return bonus
        
        def registrar_efeito_vantagem_afetiva():
            #Elo para fora, o personagem que age possui Elo registrado na planilha
            vantagem_afetiva = []
            op = sim_ou_nao(input_label="Registrar modificador quando há vantagem afetiva (personagem possui Elo com alvo)?")
            if op == 's':
                efeito = pick_options(['Bônus', 'Penalidade'], input_label='Efeito da vantagem afetiva ante o alvo')
                valor = read_input(input_label="Valor a ser somado por marcador", dada_type='int')
                vantagem_afetiva.append((efeito,valor))
            return vantagem_afetiva


        def registrar_efeito_desvantagem_afetiva():
            #Elo para dentro, o personagem alvo possui Elo registrado em relação ao agente
            desvantagem_afetiva = []
            op = sim_ou_nao(input_label="Registrar modificador quando há vantagem afetiva (alvo possui Elo com o personagem)?")
            if op == 's':
                efeito = pick_options(['Bônus', 'Penalidade'], input_label='Efeito da desvantagem afetiva ante o alvo')
                valor = read_input(input_label="Valor a ser somado por marcador", dada_type='int')
                desvantagem_afetiva.append((efeito,valor))
            return desvantagem_afetiva


        super(Teste, self).__init__()
        self.dados_gerais = definir_dados_gerais()
        self.target_folder = pasta_testes
        self.persist(fname=self.dados_gerais['Nome'], file_ext='.siurt')
    
    
    def __repr__(self):
        return self.dados_gerais['Nome']
    
    def info(self):
        output  = ''
        output += verde(self.dados_gerais['Nome'])
        output += '\n  Escopo: {}'.format(self.dados_gerais['Escopo'])
        output += '\n  Tipo: {}'.format(self.dados_gerais['Tipo'])
        output += '\n  Capacidades: {}'.format(self.dados_gerais['Capacidades'])
        output += '\n  Penalidades: {}'.format(self.dados_gerais['Penalidades'])
        output += '\n  Bônus: {}'.format(self.dados_gerais['Bônus'])
        output += '\n  Efeito de Elos com alvo: {}'.format(self.dados_gerais['Efeito da vantagem afetiva'])
        output += '\n  Efeito de Elos do alvo com personagem: {}\n'.format(self.dados_gerais['Efeito da desvantagem afetiva'])
        return output
