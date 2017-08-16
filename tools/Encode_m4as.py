
# -*- coding: utf-8 -*-
# @CreateDate : 2017/7/31 11:22
# @Author     : Bearboyxu
# @FileName   : Encode_m4as.py
# @Software   : PyCharm

from __future__ import unicode_literals
import sys
import os
import subprocess

def get_files(local_path):
    print local_path
    dirs = os.listdir(local_path)
    file_paths = []
    for dir in dirs:
        file_path = os.path.join(local_path, dir)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths

def do(local_path, temp_path):

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    file_paths = get_files(local_path)
    for filepath in file_paths:
        base_name = os.path.basename(filepath)
        base_name_sp = os.path.splitext(base_name)
        #../ffmpeg -i ybbp.m4a -ar 44100 -ac 1 -acodec pcm_s16le ybbp.wav

        exec_file = './ffmpeg.exe'
        m4afile = filepath
        wavfile = os.path.join(temp_path, base_name_sp[0] + '.wav')
        param = (exec_file, '-i', m4afile, '-ar', '44100', '-ac', '1', '-acodec', 'pcm_s16le', wavfile)
        print param
        pipe = subprocess.Popen(param, close_fds=True)
        pipe.wait()
        if 0 != pipe.returncode:
            print """encode {file} error: {return_code}""".format(file=filepath,return_code=pipe.returncode)

def main(argv):
    #if len(argv) != 3:
        # return None
    # local_path = argv[1]
    # temp_path = argv[2]
    names = ['daji']
    for name in names:
        local_path = u'E:\github_programes\wave_compare\\tools\wavetemp\\' + name
        temp_path = u'E:\github_programes\wave_compare\\tools\m4atemp\\' + name

        do(local_path, temp_path)

if __name__ == '__main__':
    main(sys.argv)
