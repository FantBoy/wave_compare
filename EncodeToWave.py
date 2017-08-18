#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: bearboyxu
@license:
@contact: bearboyxu@foxmail.com
@site:
@software: PyCharm
@file: EncodeToWave.py
@time: 2017/8/7 15:52
"""

from __future__ import unicode_literals
import sys
import os
import subprocess
import traceback
from django.conf import settings
from Common_sdk.ERROR_CODE import DecodeFileToWavException

class EncodeAudioToWav(object):

    def __init__(self):
        pass
    def DoEncode(self, local_filepath, dis_filepath):
        """
            转码到wav
        """
        try:
            if not os.path.exists(local_filepath):
                msg = """{file} not exists""".format(file=local_filepath)
                raise DecodeFileToWavException(local_filepath, msg)

            if os.path.exists(dis_filepath):
                os.remove(dis_filepath)
            exec_file = os.path.join(settings.BASE_DIR, 'Audio_Compare_app/audio_rating/tool/ffmpeg')
            param = (exec_file, '-y', '-i', local_filepath, '-ar', '44100', '-ac', '1', '-acodec', 'pcm_s16le', dis_filepath)
            pipe = subprocess.Popen(param, close_fds=True)
            pipe.wait()
            if 0 != pipe.returncode:
                msg = """encode {file} error: {return_code}""".format(file=local_filepath,return_code=pipe.returncode)
                raise DecodeFileToWavException(local_filepath, msg)
            return 0
        except Exception as e:
            raise DecodeFileToWavException(local_filepath, traceback.format_exc())
