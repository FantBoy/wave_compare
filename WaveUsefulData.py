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
from scipy import signal

#TODO 有效数据阈值待优化调整
DATA_START_VALUE = 0.025
DATA_END_VALUE = 0.025

class Wave_USEFUL_DATA(object):

    def __init__(self, filepath):
        wave_file = wave.open(filepath, 'rb')
        params = wave_file.getparams()
        """
            nchannels, sampwidth, framerate, nframes = params[:4]
            nchannels:声道数
            sampwidth:量化位数（byte）
            framerate:采样频率
            nframes:采样点数
        """
        self.framesra = params[2]
        self.frameswav = params[3]
        wave_data = wave_file.readframes(self.frameswav)
        self.datause = np.fromstring(wave_data, dtype = np.short) #16位，-32767~32767

        #按照通道数分开处理
        # waveData = np.reshape(waveData, [nframes, nchannels])
        # waveData[:, 0], waveData[:, 1],....waveData[:, nchannels]
    def get_data_length(self):
        return len(self.datause)

    def get_normalization_data(self):
        """
            归一化

        :return:
        """
        max_index = np.argmax(abs(self.datause))
        max_value = abs(self.datause[max_index])
        self.datause = self.datause / (1.0 * max_value)

    def get_wave_filtering(self):
        """
            求滤波
            y(n) = 1.0*x(n)+(-0.9375)*x(n-1)

        :return:
        """
        #TODO 公式原理待验证，优化
        datause_n_2_list = [0.00] + list(self.datause[:-1])
        datause_n_2 = np.array(datause_n_2_list)

        self.datause = self.datause * 1.0 + (-0.9375) * datause_n_2
        self.get_normalization_data()

        #使用signal做高通滤波
        # b, a = signal.butter(1, 0.9375, 'low')
        # self.datause = signal.filtfilt(b, a, self.datause)

    @staticmethod
    def get_generate_hamming_windows(row, column):
        """
            创建hammin窗口

        :param row:
        :param column:
        :return:
        """

        hammin_windows = [0] * row * column
        for index in range(row * column):
            hammin_windows[index] = 0.54 - 0.46 * (math.cos(2 * math.pi * index / (row * column - 1)))
        return np.array(hammin_windows)

        # 也可直接使用numpy的hamming方法直接获取窗口函数
        # hammin_windows = np.hamming(32 * 16)

    def get_short_time_energy(self):
        """
            获取短时能量数据

        :return:
        """

        # 点乘
        self.datause = self.datause * self.datause
        # hammin窗口
        hammin_windows = self.get_generate_hamming_windows(32, 16)
        # 卷积
        self.datause = np.convolve(self.datause, hammin_windows, 'full')
        self.get_normalization_data() # 对结果做归一化处理

    def get_data_start_index(self):
        """
            去除音频起始静音片段

        :param datause:
        :return:
        """
        for index in range(len(self.datause)):
            if self.datause[index] > DATA_START_VALUE:
                return index
        return -1

    def get_data_end_index(self):
        """
            去除音频末尾静音片段

        :param datause:
        :return:
        """
        for index in range(len(self.datause))[::-1]:
            if self.datause[index] > DATA_START_VALUE:
                return index
        return -1

    def get_useful_short_time_energy(self):
        """
            去除首尾的静音片段

        :return:
        """
        start_index = self.get_data_start_index()
        end_index = self.get_data_end_index()
        self.datause = np.array(list(self.datause)[start_index:end_index])

    def get_compare_useful_short_time_energy(self, stand_length):
        """
            获取对比音频的有效能量数据，保持对比音频有效长度跟原始音频长度一致
            若不够，则用[0]填充末尾，方便做余弦距离（[0]不影响计算结果）

        :param stand_length:
        :return:
        """

        start_index = self.get_data_start_index()
        end_index = start_index + stand_length
        if end_index <= len(self.datause):
            self.datause = np.array(list(self.datause)[start_index:end_index])
        else:
            zero_arr = [0] * (end_index - len(self.datause))
            self.datause = np.array(list(self.datause)[start_index:] + zero_arr)

    def get_compare_score(self, compare_useful_data):
        """
            计算余弦距离
        :param compare_useful_data:
        :return:
        """

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
