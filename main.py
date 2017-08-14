
# -*- coding: utf-8 -*-
# @CreateDate : 2017/7/29 22:22
# @Author     : Bearboyxu
# @FileName   : main.py
# @Software   : PyCharm

from __future__ import unicode_literals
import os
import struct
import math
import wave as we
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from collections import defaultdict
from WaveUsefulData import Wave_USEFUL_DATA

FIG_COR = ['green', 'green', 'blue', 'red' , 'purple', '']

def drow_fig(name, framesra, frameswav, stand_datauses, com_datauses, score):
    fig = plt.figure(name,figsize=(15,8), frameon = False )
    for index in range(len(stand_datauses)):
        datause_dict = stand_datauses[index]
        time = np.arange(0, len(datause_dict['value']), 1)
        ax1 = fig.add_subplot(5, 2, index * 2 + 1)
        ax1.plot(time, datause_dict['value'], color = FIG_COR[index])
        ax1.set_title(datause_dict['key'])
        # ax.set_xlabel('Time')
        #隐藏坐标轴
        ax1.set_xticks([])
        # ax1.set_yticks([])
        #隐藏边框
        # ax1.spines['right'].set_color('none')
        # ax1.spines['top'].set_color('none')
        # ax1.spines['bottom'].set_color('none')
        # ax1.spines['left'].set_color('none')

        datause_dict = com_datauses[index]
        time = np.arange(0, len(datause_dict['value']), 1) * (1.0 / framesra)
        ax1 = fig.add_subplot(5, 2, index * 2 + 2)
        ax1.plot(time, datause_dict['value'], color=FIG_COR[index])
        ax1.set_title(datause_dict['key'])
        ax1.set_xticks([])

    # ax1.text(0.75 * time[-1], 0.5, str(score), fontsize = 15, verticalalignment = "bottom", horizontalalignment = "left")
    ax1.set_xlabel('SCORE: ' + str(score), fontsize = 15, horizontalalignment = "right")

def do_match(stand_filepath, com_filepath):
    wave_useful_data = Wave_USEFUL_DATA(stand_filepath)
    stand_datas = []
    stand_datas.append({'key': 'Raw Spectrum', 'value': wave_useful_data.datause})
    wave_useful_data.get_normalization_data()
    stand_datas.append({'key': 'Raw Spectrum(normalization)', 'value': wave_useful_data.datause})
    wave_useful_data.get_wave_filtering()
    stand_datas.append({'key': 'Wave Filtering', 'value': wave_useful_data.datause})
    wave_useful_data.get_short_time_energy()
    stand_datas.append({'key': 'Short Time Energy', 'value': wave_useful_data.datause})
    wave_useful_data.get_useful_short_time_energy()
    stand_datas.append({'key': 'Useful Short Time Energy', 'value': wave_useful_data.datause})

    # drow_fig('stand_wave-' + filepath, wave_useful_data.framesra, wave_useful_data.frameswav, datas)

    com_datas = []
    cop_wave_useful_data = Wave_USEFUL_DATA(com_filepath)
    com_datas.append({'key': 'Raw Spectrum', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_normalization_data()
    com_datas.append({'key': 'Raw Spectrum(normalization)', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_wave_filtering()
    com_datas.append({'key': 'Wave Filtering', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_short_time_energy()
    com_datas.append({'key': 'Short Time Energy', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_compare_useful_short_time_energy(wave_useful_data.get_data_length())
    com_datas.append({'key': 'Useful Short Time Energy', 'value': cop_wave_useful_data.datause})

    score = wave_useful_data.get_compare_score(cop_wave_useful_data.datause)
    drow_fig(stand_filepath + '-' + com_filepath, cop_wave_useful_data.framesra, cop_wave_useful_data.frameswav,
             stand_datas, com_datas, score)


if __name__ == '__main__':

    files = []
    # files.append(('wavs\daji\daji_hall_1.wav', 'tools\wavetemp\daji_hall_1_siwo.wav'))
    # files.append(('wavs\daji\daji_hall_1.wav', 'tools\wavetemp\daji_hall_1_xuchao.wav'))
    # files.append(('wavs\houyi\houyi_hall_3.wav', 'tools\wavetemp\houyi_hall_3.wav'))
    # files.append(('wavs\luban\luban_hall_2.wav', 'tools\wavetemp\luban_hall_2_xmz.wav'))
    # files.append(('wavs\luban\luban_hall_move_5.wav', 'tools\wavetemp\luban_hall_move_5_xmz.wav'))
    # files.append(('wavs\houyi\houyi_death_1.wav', 'tools\wavetemp\houyi_death_1_yy.wav'))
    # files.append(('wavs\houyi\houyi_hall_1.wav', 'tools\wavetemp\houyi_hall_1_yy.wav'))
    # files.append(('wavs\houyi\houyi_hall_3.wav', 'tools\wavetemp\houyi_hall_3_yy.wav'))
    # files.append(('wavs\houyi\houyi_move_1.wav', 'tools\wavetemp\houyi_move_1_yy.wav'))
    # files.append(('wavs\houyi\houyi_move_2.wav', 'tools\wavetemp\houyi_move_2_yy.wav'))
    # files.append(('wavs\houyi\houyi_move_4.wav', 'tools\wavetemp\houyi_move_4_yy.wav'))
    # files.append(('wavs\ysw06.wav', 'wavs\\recording.wav'))
    files.append(('wavs\ysw06.wav', 'wavs\\t4.wav'))

    for (stand_filepath, com_filepath) in files:
        do_match(stand_filepath, com_filepath)

    plt.show()

