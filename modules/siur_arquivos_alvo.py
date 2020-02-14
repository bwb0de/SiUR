#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os

from modules.siur_pastas_de_dados import pasta_raiz

target_character_filename = '.target_character.siurc'
target_character_fullpath = os.sep.join([pasta_raiz, target_character_filename])
target_character_img = '.target_character_img'
target_cenario_filename = '.target_cenario.siurctx'
target_cenario_fullpath = os.sep.join([pasta_raiz, target_cenario_filename])
target_cena_filename = '.target_cena.siurctx'
target_cena_fullpath = os.sep.join([pasta_raiz, target_cena_filename])
target_bg_snd = '.target_bgsnd_pid'
