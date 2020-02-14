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

from collections import OrderedDict
from cli_tools import \
	verde,\
	vermelho,\
	amarelo,\
	azul_claro,\
	limpar_tela,\
	select_ops,\
	input_num

import copy

class Personagem:
	def __init__(self, nome, tipo):
		self.nome = nome
		self.tipo = tipo
		self.fase = 'declarativa'
		self.ac = ''
		self.prioridade = False
		self.h_ac = []
		self.iniciativa = 0
		self.pos = 0

protagonistas = ['Reginaldo', 'Shun', 'Heloise', 'Bellanto', 'Antoine', 'Luigi', 'Lazarus', 'Marco']
acoes = ['Sacar arma', 'Mover e atacar', 'Atacar', 'Preparar ou mover', 'Defender-se']

def init_turn_script():
	limpar_tela(amarelo("Selecione os protagonistas que participarão da cena:"))
	prot = select_ops(protagonistas, 1)
	extr = []
	limpar_tela(amarelo("Quais outros personagens participarão da cena?"))
	op = ''
	while True:
		if op == 'n':
			break
		extr.append(input(verde("Nome: ")))
		op = input("Adicionar outro personagem (s/n)? ")
	
	protcolor = []
	for protagonista in prot:
		protcolor.append(Personagem(verde(protagonista), "protagonista"))
	
	extrcolor = []
	for extra in extr:
		extrcolor.append(Personagem(vermelho(extra), "antagonista"))

	p_in_cbt = protcolor + extrcolor
	limpar_tela("Definição das iniciativas: ")
	max_init_ref = []
	for p in p_in_cbt:
		p.iniciativa = input_num("{}: ".format(p.nome))
		max_init_ref.append(int(p.iniciativa))
	
	max_init_ref = max(max_init_ref)
	
	for p in p_in_cbt:
		p.pos = (max_init_ref - p.iniciativa) * 2

	while True:
		limpar_tela()
		turn_order = sort_personagens(p_in_cbt)
		for p in turn_order:
			show_turn_order(turn_order)
			if p.pos == turn_order[0].pos:
				if p.fase == 'declarativa':
					print(amarelo('Selecione o tipo de ação de {}'.format(p.nome)))
					p.ac = select_ops(acoes, 1)[0]
					p.h_ac.append(p.ac)
					p.prioridade = False
					if p.ac == 'Defender-se':
						p.fase = 'resolutiva_def'
					if p.ac == 'Mover e atacar' or p.ac == 'Atacar':
						p.fase = 'resolutiva_atk'
						print('')
						print('Selecione o alvo')

						if p.tipo == 'protagonista':
							p.alvo = select_ops(extr, 1)
						elif p.tipo == 'antagonista':
							p.alvo = select_ops(prot, 1)

						p.prioridade = True
						p.ac += " -> " + amarelo(p.alvo[0])
					print('')
					p.pos += int(input("Número instantes? "))
				elif p.fase == 'resolutiva_atk':
					input('Faça o teste de ATAQUE de {}'.format(p.nome))
					p.pos += 1
					p.ac = ''
					p.fase = 'declarativa'
				else:
					p.ac = ''
					p.fase = 'declarativa'

			else:
				break
		
		
	
def sort_personagens(p_in_cbt):
	max_index = []
	for p in p_in_cbt:
		max_index.append(p.pos)
	max_index = max(max_index)+1
	turn_order = []
	for n in range(0,max_index):
		atacantes = []
		outros = []
		for p in p_in_cbt:
			if p.pos == n:
				if p.prioridade == True:
					atacantes.append(p)
				else:
					outros.append(p)
		for p in atacantes:
			turn_order.append(p)
		for p in outros:
			turn_order.append(p)
	return turn_order

def show_turn_order(order_list):
	limpar_tela(amarelo('Ordem das ações'))
	print(azul_claro('==============================================='))
	for p in order_list:
		print(' ' + str(p.pos).zfill(2) + ' >> ' + p.nome + ' ({})'.format(p.ac))
	print(azul_claro('==============================================='))
	print('')