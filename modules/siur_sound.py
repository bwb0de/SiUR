#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import vlc
import os

from time import sleep

from modules.siur_pastas_de_dados import pasta_sons_de_fundo, pasta_sons_fx
from modules.cli_tools import write_to_file, read_from_file, pick_options
from modules.siur_arquivos_alvo import target_bg_snd


def select_snd(folder):
    snd_files = os.listdir(folder)
    selected_snd = pick_options(snd_files, input_label="Selecione um arquivo de audio")
    return selected_snd



def stop_bgsnd():
    try:
        old_pid = read_from_file(target_bg_snd)
        os.kill(int(old_pid), 15)
    except FileNotFoundError: pass
    except ProcessLookupError: pass


def play_bgsnd(filename, filefolder=pasta_sons_de_fundo):
    stop_bgsnd()

    independent_process = os.fork()

    if independent_process == 0:
        write_to_file(str(os.getpid()), target_bg_snd)
        filename_obj = vlc.MediaPlayer(filefolder+filename)
        filename_obj.play()
        sleep(2)
        duration = filename_obj.get_length() / 1000
        sleep(duration)
        os.remove(target_bg_snd)


def play_fxsnd(filename, filefolder=pasta_sons_fx):
    independent_process = os.fork()

    if independent_process == 0:
        filename_obj = vlc.MediaPlayer(filefolder+filename)
        filename_obj.play()
        sleep(2)
        duration = filename_obj.get_length() / 1000
        sleep(duration)
