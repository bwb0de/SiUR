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
from modules.cli_tools import read_input, pick_options, listar_dicionario
from modules.py_pickle_handlers import load_selected_pickle_ob, read_pickle
from modules.siur_pastas_de_dados import pasta_equipamentos, pasta_especialidades, pasta_testes

lista_de_ocultabilidade = ['Bolso', 'Jaqueta', 'Sobretudo']
lista_de_disponibilidade = ['Comum', 'Restrito', 'Raro', 'Único/Artesanal']
lista_de_categorias_danos = ['Cortante', 'Contundente', 'Contucortante', 'Perfurante', 'Corrosivo', 'Queimante']
lista_de_tipo_danos = ['Significativo', 'Letal', 'Agravado']
lista_de_alcances_armas_brancas = ['Insignificante', 'Curto', 'Médio', 'Longo', 'Muito longo', 'Extremamente longo']
lista_de_materiais_armas = ['Pedra', 'Ferro', 'Aço', 'Madeira', 'Prata']
lista_de_materiais_vestes = ['Lã', 'Algodão', 'Couro', 'Ferro', 'Aço', 'Bambu']

class Especialidade(PickleDataType):
        def __init__(self):
                def definir_dados_gerais():
                        output  = OrderedDict()
                        output['Nome'] = read_input(input_label="Nome da especialidade")
                        output['Descrição'] = read_input(input_label="Descrição resumida")
                        output['Ações da especialidade'] = vincular_acoes('Ações da especialidade:')
                        output['Ações familiares'] = vincular_acoes('Ações familiares:')
                        return output
                
                def vincular_acoes(label):
                        tmp_list = load_selected_pickle_ob(label, pasta_testes)
                        output = OrderedDict()
                        for item in tmp_list:
                                output[item.dados_gerais['Nome']] = item.fullpath()
                        return output

                super(Especialidade, self).__init__()
                self.dados_gerais = definir_dados_gerais()
                self.target_folder = pasta_especialidades
                self.persist(fname=self.dados_gerais['Nome'], file_ext='.siuresp')
        
        def __repr__(self):
                return self.dados_gerais['Nome']

        def info(self):
                output  = ''
                output += self.dados_gerais['Nome']
                output += os.linesep + " Ações da especialidade:" + os.linesep
                
                for item, location in self.dados_gerais['Ações da especialidade'].items():
                        output += '   ' + item + ', ' + location + os.linesep

                output += os.linesep + ' Ações familiares:' + os.linesep

                for item, location in self.dados_gerais['Ações familiares'].items():
                        output += '   ' + item + ', ' + location + os.linesep

                return output
        



