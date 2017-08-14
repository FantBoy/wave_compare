#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @CreateDate : 2017/8/1 0:00
# @Author     : Bearboyxu
# @FileName   : test.py
# @Software   : PyCharm


from WaveUsefulData import Wave_USEFUL_DATA
import numpy as np
import matplotlib.pyplot as plt

filepath = 'E:\programes\github\wave_compare\wavs\ysw03.wav'
wave_useful_data = Wave_USEFUL_DATA(filepath)

hammin_windows = wave_useful_data.get_generate_hamming_windows(32, 16)
x = np.arange(0, len(hammin_windows), 1)
fig = plt.figure()
# time = np.arange(0, len(datause_dict['value']), 1) * (1.0 / framesra)
ax1 = fig.add_subplot(1, 1 , 1)
ax1.plot(x, hammin_windows, color = 'red')
plt.show()
