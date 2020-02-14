#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os

from modules.siur_pastas_de_dados import pasta_imagens
from modules.cli_tools import pick_options

def select_img(folder=pasta_imagens):
    img_files = os.listdir(folder)
    selected_img = pick_options(img_files, input_label="Selecione uma imagem")
    return selected_img