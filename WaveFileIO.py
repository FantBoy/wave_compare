#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @CreateDate : 2017/7/29 18:12
# @Author     : Bearboyxu
# @FileName   : WaveFileIO.py
# @Software   : PyCharm

import struct
import numpy as np
import shutil
import os


class WaveFileIO(object):
    """
        以文件读写的方式，读写wave文件信息：头部信息，数据信息
    """

    def __init__(self, filepath):
        self.filepath = os.path.join(os.getcwd(), filepath)
        self.wav_file = None
        print self.filepath
        if os.path.exists(filepath):
            self.wav_file = open(self.filepath, 'r')
            if not self.check_wave_file():
                self.wav_file = None

        if self.wav_file:
            self.cksize = self.__read_uint(self.__get_chunck_size())
            fmt_chunk_data = self.__get_chunk_data(20)
            self.format_tag = self.__read_ushort(fmt_chunk_data[0:2])
            self.channels = self.__read_ushort(fmt_chunk_data[2:4])
            self.sample_rate = self.__read_uint(fmt_chunk_data[4:8])
            self.samples_persec = self.__read_uint(fmt_chunk_data[8:12])
            self.block_align = self.__read_ushort(fmt_chunk_data[12:14])

            if self.__check_list_format():
                self.list_length = self.__read_uint(self.__get_data_length(20 + self.cksize + 4, 4))
                if self.__check_audio_data_format():
                    self.data_chunk_size = self.__read_uint(self.__get_data_length(20 + self.cksize + 4 + 4 + self.list_length + 4, 4))
                    self.total_samples = (self.data_chunk_size / self.block_align)
                    self.audio_data_duration = 20 + self.cksize + 4 + 4 + self.list_length + 4 + 4
                else:
                    self.wav_file = None

            else:
                self.wav_file = None


    def check_wave_file(self):
        if self.__check_riff_format() and self.__check_wave_format() and self.__check_fmt_format():
            return True
        return False

    def get_channels(self):
        """Returns the number of channels in the file."""
        return self.channels

    def get_block_align(self):
        """Returns the number of bytes used in the file
        to represent a sample, multiplied by the number of channels."""
        return self.block_align

    def get_sample_rate(self):
        """Returns the numbers of samples per second, per channel."""
        return self.sample_rate

    def get_total_samples(self):
        """Returns the total number of samples per channel."""
        return self.total_samples

    def get_audio_data(self, duration, size):
        self.wav_file.seek(duration, 0)
        data = np.fromfile(self.wav_file, dtype=np.uint16, count=-1)
        return data

    def __check_riff_format(self):
        self.wav_file.seek(0, 0)
        RIFF = self.wav_file.read(4)
        self.wav_file.seek(0, 0)
        print RIFF
        return 'RIFF' == RIFF


    def __check_wave_format(self):
        self.wav_file.seek(8, 0)
        WAVE = self.wav_file.read(4)
        self.wav_file.seek(0, 0)
        print WAVE
        return 'WAVE' == WAVE


    def __check_fmt_format(self):
        self.wav_file.seek(12, 0)
        fmt = self.wav_file.read(4)
        self.wav_file.seek(0, 0)

        return 'fmt ' == fmt


    def __check_list_format(self):
        self.wav_file.seek(20 + self.cksize, 0)
        LIST = self.wav_file.read(4)
        print LIST
        return 'LIST' == LIST


    def __check_audio_data_format(self):
        self.wav_file.seek(20 + self.cksize + 4 + 4 + self.list_length, 0)
        data = self.wav_file.read(4)
        print data
        return 'data' == data

    def __get_chunck_size(self):
        self.wav_file.seek(16, 0)
        cksize = self.wav_file.read(4)
        self.wav_file.seek(0, 0)
        return cksize


    def __get_data_length(self, duration, size):
        self.wav_file.seek(duration, 0)
        length = self.wav_file.read(size)
        self.wav_file.seek(0, 0)
        return length


    def __get_chunk_data(self, chunk_size):
        self.wav_file.seek(20, 0)
        fmt_chunk_data = self.wav_file.read(chunk_size)
        return fmt_chunk_data

    @staticmethod
    def __read_ushort(data):
        """Turn a 2-byte little endian number into a Python number."""
        return struct.unpack("<H", data)[0]

    @staticmethod
    def __read_uint(data):
        """Turn a 4-byte little endian number into a Python number."""
        return struct.unpack("<I", data)[0]