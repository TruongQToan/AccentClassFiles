import eyed3
import os
import subprocess
import sys
import os.path


if sys.platform == "linux" or sys.platform == "linux2":
    sox = '/usr/bin/sox'
else:
    sox = '/usr/local/bin/sox'


def create_silence_from_list_of_files(list_of_files, output_folder, silence_padding='0'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for f in list_of_files:
        create_silence_from_file(f, output_folder + '/' + f.split('/')[-1][:-4] + 's.' + f.split('/')[-1][-3:], silence_padding)


def create_silence_from_file(input_file, output_file, silence_padding='0'):
    if os.path.isfile(output_file): return
    if not (input_file[-3:] == 'wav' or input_file[-3:] == 'mp3'): return
    subprocess.call([sox, '-v', '0', input_file, output_file])
    if silence_padding == '0':
        return
    new_output = output_file[:-4] + '-p' + silence_padding + output_file[-4:]
    subprocess.call([sox, '-n', '-r', '44100', '-c', '1', 'temp_silence.wav', 'trim', '0.0', str(float(silence_padding) / 1000.0)])
    subprocess.call([sox, output_file, 'temp_silence.wav', new_output])
    #subprocess.call(['rm', '-f', 'temp_silence.wav', output_file])


def create_silence_from_folder(input_folder, output_folder, silence_padding='0'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for f in os.listdir(input_folder):
        if not (f[-3:] == 'wav' or f[-3:] == 'mp3'): continue
        create_silence_from_file(input_folder + '/' + f, output_folder + '/' + f[:-4] + 's.' + f[-3:], silence_padding)
