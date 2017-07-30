#!/usr/bin/env python
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

# from WaveFileIO import WaveFileIO
#
# wavfileid = WaveFileIO('wavs\ysw02.wav')
# print wavfileid.wav_file, wavfileid.audio_data_duration, wavfileid.data_chunk_size
# audioData = wavfileid.get_audio_data(wavfileid.audio_data_duration, wavfileid.data_chunk_size)
# print len(audioData)
#
# DataX = np.arange(0, 56832, 1) * (1.0/44100)
#
# # 绘制波形
# pl.subplot(211)
# pl.plot(DataX,audioData)
# pl.subplot(212)
# pl.plot(time, wave_data[1], c="g")
# pl.xlabel("time (seconds)")
# pl.show()

FIG_COR = ['green', 'green', 'blue', 'red' , 'purple', '']

def drow_fig(name, framesra, frameswav, datauses):

    fig = plt.figure(name)
    for index in range(len(datauses)):
        datause_dict = datauses[index]
        time = np.arange(0, len(datause_dict['value']), 1) * (1.0 / framesra)
        ax1 = fig.add_subplot(3, 2, index + 1)
        ax1.plot(time, datause_dict['value'], color = FIG_COR[index])
        ax1.set_title(datause_dict['key'])
        # ax.set_xlabel('Time')
        index += 1

if __name__ == '__main__':

    filepath = 'E:\programes\github\wave_compare\wavs\ysw03.wav'
    wave_useful_data = Wave_USEFUL_DATA(filepath)
    datas = []
    datas.append({'key': 'Raw Spectrum', 'value': wave_useful_data.datause})
    wave_useful_data.get_normalization_data()
    datas.append({'key': 'Raw Spectrum(normalization)', 'value': wave_useful_data.datause})
    wave_useful_data.get_wave_filtering()
    datas.append({'key': 'Wave Filtering', 'value': wave_useful_data.datause})
    wave_useful_data.get_short_time_energy()
    datas.append({'key': 'Short Time Energy', 'value': wave_useful_data.datause})
    wave_useful_data.get_useful_short_time_energy()
    datas.append({'key': 'Useful Short Time Energy', 'value': wave_useful_data.datause})

    drow_fig('stand_wave-' + filepath, wave_useful_data.framesra, wave_useful_data.frameswav, datas)

    filepath = 'E:\programes\github\wave_compare\wavs\\ckj.wav'
    cop_wave_useful_data = Wave_USEFUL_DATA(filepath)
    datas = []
    datas.append({'key': 'Raw Spectrum', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_normalization_data()
    datas.append({'key': 'Raw Spectrum(normalization)', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_wave_filtering()
    datas.append({'key': 'Wave Filtering', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_short_time_energy()
    datas.append({'key': 'Short Time Energy', 'value': cop_wave_useful_data.datause})
    cop_wave_useful_data.get_compare_useful_short_time_energy(wave_useful_data.get_data_length())
    datas.append({'key': 'Useful Short Time Energy', 'value': cop_wave_useful_data.datause})

    drow_fig('compare_wave-' + filepath, cop_wave_useful_data.framesra, cop_wave_useful_data.frameswav, datas)

    print wave_useful_data.get_compare_score(cop_wave_useful_data.datause)
    plt.show()

