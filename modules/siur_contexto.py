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

from modules.py_obj_data_tools import PickleDataType, ExtendedDict
from modules.py_pickle_handlers import load_selected_pickle_ob, return_object_info_and_location_list, set_target_pickle_file
from modules.cli_tools import verde, read_input, sim_ou_nao, pick_options
from modules.siur_pastas_de_dados import pasta_cenarios, pasta_cenas, pasta_protagonistas, pasta_antagonistas, pasta_raiz, pasta_sons_de_fundo
from modules.siur_arquivos_alvo import target_cenario_filename
from modules.siur_sound import play_bgsnd, select_snd


class Cenario(PickleDataType):
        def __init__(self):
                def definir_dados_gerais():
                        output  = OrderedDict()
                        output['Nome'] = read_input(input_label='Título do cenário')
                        output['Descrição'] = read_input(input_label='Descrição resumida')
                        output['Desenvolvimento tecno-científico'] = read_input(input_label='Desenvolvimento tecno-científico', data_pattern='[0-9]{1}', waring_msg="Escolha um valor entre 0 e 9...")
                        output['Tipos permitidos'] = []
                        return output

                super(Cenario, self).__init__()
                self.dados_gerais = definir_dados_gerais()
                self.itens_caidos = []
                self.target_folder = pasta_cenarios
                self.persist(fname=self.dados_gerais['Nome'], file_ext='.siurctx')

        def __repr__(self):
            return self.dados_gerais['Nome']


class Local(PickleDataType):
        def __init__(self):
                def definir_dados_gerais():
                        output  = OrderedDict()
                        output['Nome'] = read_input(input_label='Titulo da cena/local')
                        output['Descrição'] = read_input(input_label='Descrição resumida da cena/local')
                        output['Modificadores globais'] = []
                        current_cenario = set_target_pickle_file(pasta_cenarios, target_cenario_filename, pasta_raiz)
                        output['Vinculada ao cenário'] = current_cenario.dados_gerais['Nome']
                        op = sim_ou_nao(input_label='Registrar modificador global?')
                        if op == 's': self.registrar_modificadores_globais()
                        op = sim_ou_nao(input_label='Há um personagem de referência nessa cena?')
                        output['Personagem de referência'] = False
                        if op == 's': 
                                personagem_referencia = list(load_selected_pickle_ob('Nome do personagem',  pasta_antagonistas))[0]
                                output['Personagem de referência'] = personagem_referencia.fullpath()
                        output['Som de fundo'] = select_snd(pasta_sons_de_fundo)
                        return output

                super(Local, self).__init__()
                self.dados_gerais = definir_dados_gerais()
                self.itens_caidos = []
                self.target_folder = pasta_cenas
                self.persist(fname=self.dados_gerais['Nome'], file_ext='.siurctx')

        def __repr__(self):
            return self.dados_gerais['Nome']
        
        def registrar_modificadores_globais(self):
                pass

        def play_snd(self):
                play_bgsnd(self.dados_gerais["Som de fundo"])


        def registrar_itens_caidos(self, item):
                self.itens_caidos.append(item)
                self.persist()
        
        def listar_itens_caidos(self):
                return self.itens_caidos

        def registrar_retirada_de_itens(self, idx_do_item):
                item_retirado = self.itens_caidos.pop(idx_do_item)
                self.persist()
                return item_retirado


