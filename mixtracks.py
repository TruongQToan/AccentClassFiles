import math
import argparse
from random import shuffle
from shutil import rmtree
import os
import re

from utils import shuffle_track, get_name, makedir, convert_mp3, make_track, get_num_files, sub_directory
from music_file import MusicFile
from convert2mp3 import convert_file_2_mp3
from generator import generate_from_list_of_files
from config import OUTPUT_ALL, MAPPING


def get_prefix(list_of_tracks, grammar):
    min_track = 1000
    max_track = 0
    for track in list_of_tracks:
        if track > max_track:
            max_track = track
        if track < min_track:
            min_track = track
    if grammar:
        name = '%s-%03d-%03d' % ('Grammar', min_track, max_track)
    else:
        name = '%s-%03d-%03d' % ('Accent', min_track, max_track)
    return name


def find_exceptions(exceptions):
    results = []
    for f in exceptions.split('.'):
        if ':' in f:
            for i in range(int(f.split(':')[0]), int(f.split(':')[1]) + 1):
                results.append(i)
        else:
            results.append(int(f))
    return results


def get_track_numbers(s):
    track_numbers = []
    for f in s.split('.'):
        if ':' in f:
            for i in range(int(f.split(':')[0]), int(f.split(':')[1]) + 1):
                track_numbers.append(i)
        else:
            track_numbers.append(int(f))
    return track_numbers


def get_files(track):
    add = 0
    if track.find('+') != -1:
        add = 1
    elif track.find('-') != -1:
        add = -1
    if add == 1:
        track = track.split('+')
        return add, get_track_numbers(track[0][1:]), find_exceptions(track[1])
    elif add == -1:
        track = track.split('-')
        return add, get_track_numbers(track[0][1:]), find_exceptions(track[1])
    return add, get_track_numbers(track[1:]), []


def filter_files(list_of_tracks, shuffled):
    def check_exception(u, exceptions):
        if len(u) > 1 and int(u[1]) in exceptions:
            return True
        if len(u) == 1 and int(u[0]) in exceptions:
            return True
        return False

    input_files = []
    artist = ''
    for track in list_of_tracks:
        type_file = MAPPING[track[0]]
        if type_file not in artist.split('_'):
        	artist += type_file + '_'
        sub_input_files = []
        add, track_numbers, exceptions = get_files(track)
        for f in sorted(os.listdir(type_file + '/' + type_file + 'EN/')):
            if not (f[-3:] == 'mp3' or f[-3:] == 'wav'): continue
            m = re.search(r"\d{3}(-\d{2})?", f)
            u = m.group(0).split('-')
            if int(u[0]) in track_numbers:
                if add == 1 and check_exception(u, exceptions):
                    sub_input_files.append(type_file + '/' + type_file + 'EN/' + f)
                    continue
                elif add == -1 and check_exception(u, exceptions):
                    continue
                elif add == 0 or add == -1:
                    sub_input_files.append(type_file + '/' + type_file + 'EN/' + f)
        if shuffled == "group":
            shuffle(sub_input_files)
        input_files.extend(sub_input_files)
    for f in input_files:
        print (f)
    return input_files, artist, type_file


def mix(list_of_tracks, num_files_per_group, num_plays,
    num_copies=1, prefix='', to_mp3=False, shuffled='', silence_padding='0'):
    #type_file = 'Accent' if not grammar else 'Grammar'
    #artist = 'Accent' if not grammar else 'Grammar'
    #album = 'Accent Training' if not grammar else 'Grammar Training'
    album = ''
    input_files, artist, type_file = filter_files(list_of_tracks, shuffled)
    if shuffled == "all": shuffle(input_files)
    if prefix == '' or prefix == None:
        prefix = get_prefix(list_of_tracks, type_file)
    if num_files_per_group == 0:
        num_files_per_group = get_num_files(len(input_files))
    generate_from_list_of_files(input_files, artist[:-1], False, silence_padding)
    files = ['output_' + artist[:-1] + '/' + f.split('/')[-1][:-6] + artist[:-1] + f.split('/')[-1][-4:] for f in input_files]
    album = artist + 'Training'
    artist = artist[:-1] # delete last space
    # Shuffle files
    for copies in range(int(num_copies)):
        result = shuffle_track(files, num_plays, num_files_per_group)
        dir_name = OUTPUT_ALL + '(wav)/' + sub_directory() + '/' + artist
        makedir(dir_name)
        name = get_name(dir_name, prefix, num_plays, silence_padding)
        make_track(result, name)
        convert_mp3(to_mp3, name, dir_name.replace("wav", "mp3"), artist, album)
    rmtree('output_' + artist)
