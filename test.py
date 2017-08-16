
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


class TestgDemo(object):
    urls = []
    # self.urls = []
    def add_urls(self, url):
        self.urls.append(url)

demo1 = TestgDemo()
demo1.add_urls('www.ximalaya.com')
print demo1.urls

demo2 = TestgDemo()
demo2.add_urls('www.qingting.com')
print demo2.urls



a = {'1': 'qwe', '2': 'ewq'}
b = a
# b=a.copy()
b['add'] = '354'
print a


aa = [1,2,3,4,5]
# bb = aa
bb = aa[:]
bb.append(34)
print aa
