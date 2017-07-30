#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @CreateDate : 2017/7/30 20:03
# @Author     : Bearboyxu
# @FileName   : WaveUsefulData.py
# @Software   : PyCharm

from __future__ import unicode_literals
import math
import wave
import numpy as np

DATA_START_VALUE = 0.025
DATA_END_VALUE = 0.025

class Wave_USEFUL_DATA(object):

    def __init__(self, filepath):
        wave_file = wave.open(filepath, 'rb')
        params = wave_file.getparams()
        self.framesra = params[2]
        self.frameswav = params[3]
        wave_data = wave_file.readframes(self.frameswav)
        self.datause = np.fromstring(wave_data, dtype = np.short)

    def get_data_length(self):
        return len(self.datause)

    def get_normalization_data(self):
        # 归一化
        max_index = np.argmax(self.datause)
        self.datause = self.datause / (1.0 * self.datause[max_index])

    def get_wave_filtering(self):
        # 滤波
        # y(n) = 1.0*x(n)+(-0.9375)*x(n-1)  滤波
        datause_n_2_list = [0.00] + list(self.datause[:-1])
        datause_n_2 = np.array(datause_n_2_list)

        self.datause = self.datause * 1.0 + (-0.9375) * datause_n_2
        self.get_normalization_data()

    @staticmethod
    def get_generate_hamming_windows(row, column):
        # hamming窗
        hammin_windows = [0] * row * column
        for index in range(row * column):
            hammin_windows[index] = 0.54 - 0.46 * (math.cos(2 * math.pi * index / (row * column)))
        return np.array(hammin_windows)

    def get_short_time_energy(self):
        # 短时能量波形
        # 电乘
        self.datause = self.datause * self.datause
        # hamming窗
        hammin_windows = self.get_generate_hamming_windows(32, 16)
        # 卷积
        self.datause = np.convolve(self.datause, hammin_windows, 'full')
        self.get_normalization_data()

    def get_data_start_index(self):
        """
        通过阈值得到音频有效数据开始的下标
        :param datause:
        :return:
        """
        for index in range(len(self.datause)):
            if self.datause[index] > DATA_START_VALUE:
                return index
        return -1

    def get_data_end_index(self):
        """
        通过阈值得到音频有效数据结束的下标
        :param datause:
        :return:
        """
        for index in range(len(self.datause))[::-1]:
            if self.datause[index] > DATA_START_VALUE:
                return index
        return -1

    def get_useful_short_time_energy(self):
        # 有效的短时能量波形
        start_index = self.get_data_start_index()
        end_index = self.get_data_end_index()
        self.datause = np.array(list(self.datause)[start_index:end_index])

    def get_compare_useful_short_time_energy(self, stand_length):
        """
        处理对比音频使其与标准音频长度相同
        通过阈值获得的数据开始下标截取与标准音频相同长度的音频数据
        :param stand_length:
        :return:
        """
        # 对比音频的有效短时能量波形
        start_index = self.get_data_start_index()
        end_index = start_index + stand_length
        if end_index <= len(self.datause):
            self.datause = np.array(list(self.datause)[start_index:end_index])
        else:
            zero_arr = [0] * (end_index - len(self.datause))
            self.datause = np.array(list(self.datause)[start_index:] + zero_arr)

    def get_compare_score(self, compare_useful_data):
        dot = (self.datause * compare_useful_data).sum()
        normStandard = (self.datause * self.datause).sum()
        normCompare = (compare_useful_data * compare_useful_data).sum()
        print dot,normStandard,normCompare
        return 100 * (dot / (math.sqrt(normStandard) * math.sqrt(normCompare)))

    def auto_get_usrful_data(self):
        self.get_normalization_data()
        self.get_wave_filtering()
        self.get_short_time_energy()
        self.get_useful_short_time_energy()