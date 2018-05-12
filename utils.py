from music_file import MusicFile
from random import shuffle
import os
from config import GLOSSIKA_EN, GLOSSIKA_VN
import subprocess
from generator import generate_from_list_of_files
import sys
from convert2mp3 import convert_file_2_mp3
import copy


def get_num_files(n):
    if n < 30: return 7
    if n >= 30: return 8


def generate_glossika(start, end, type_output='B', shuffled='', silence_padding='0'):
    makedir('output' + type_output)
    input_files = []
    for i in range(start, end + 1):
        input_files.append(GLOSSIKA_EN + 'FL-%04d-en.wav' % i)
    generate_from_list_of_files(input_files, GLOSSIKA_VN, type_output, False, silence_padding)
    files = ['output%s/FL-%04d-%s%s' % (type_output, i, type_output, '.wav') for i in range(start, end + 1)]
    if shuffled == 'group': shuffle(files)
    return files


def get_sox():
    sox = ''
    if sys.platform == "linux" or sys.platform == "linux2":
        sox = '/usr/bin/sox'
    else:
        sox = '/usr/local/bin/sox'
    return sox


def makedir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def shuffle_track(files, num_plays, num_files_per_group):
    start = 0
    end = len(files) - 1
    list_of_items = []
    for file in files:
        m = MusicFile(file, num_plays)
        list_of_items.append(m)
    result = []
    sub_list = list_of_items[start:start + num_files_per_group]
    j = start + num_files_per_group
    shuffle_else = False
    while True:
        if len(sub_list) == 0: break
        if shuffle_else:
            shuffle_else = False
            new_sub_list = sub_list[1:]
            shuffle(new_sub_list)
            new_sub_list.insert(0, sub_list[0])
            sub_list = new_sub_list
        else: shuffle(sub_list)
        new_list = copy.copy(sub_list)
        for item in new_list:
            if type(item) is str: print ('Item = ' + item)
            else:
                result.append(item.name)
                item.num_plays -= 1
                if item.num_plays == 0:
                    sub_list.remove(item)
                    if j <= end:
                        sub_list.insert(0, MusicFile(files[j], num_plays))
                        shuffle_else = True
                        j += 1
                    break
    return result


'''
if toMP3 = True, convert output file into mp3 format
listOfArgvs is list of argument
lame: path to lame
lameParas: parameters used when lame is executed
name: input (.wav) file in directory Output(wav)
name1: input (.mp3) file in directory Output(mp3)
'''
def convert_mp3(to_mp3, name, folder_name, artist, album):
    if to_mp3:
        makedir(folder_name)
        convert_file_2_mp3(name, folder_name + '/' + name.split('/')[-1].replace('wav', 'mp3'), artist, album)


def print_log(log, log_tracks, list_of_files):
    if log:
        for item in list_of_files:
            if item.find(str('%04d'%log_tracks)) != -1:
                print ('####' + item + '####')
            else: print(item)


def get_name(output_folder, prefix, num_plays, silence_padding='0'):
    if (int(silence_padding) >= 10000):
        silence_padding = '%05d' % (int(silence_padding))
    else:
        silence_padding = '%04d' % (int(silence_padding))
    name_id = 1
    if silence_padding != '0000':
        addition_padding = '-p' + silence_padding
    else:
        addition_padding = ''
    name = './' + output_folder + '/' + prefix + '_' + '%1ds-%1d' % (num_plays, name_id) + addition_padding + '.wav'
    max_id = None
    while True:
        if os.path.exists(name):
            name_id += 1
            name = './' + output_folder + '/' + prefix + '_' + '%1ds-%1d' % (num_plays, name_id) + addition_padding + '.wav'
        else: break
    return name


def make_track(result, name):
    sox = get_sox()
    list_of_argvs = [sox, ] + result + [name,]
    subprocess.call(list_of_argvs)


def sub_directory():
    from time import gmtime, strftime
    return strftime("%Y-%d-%m", gmtime())
