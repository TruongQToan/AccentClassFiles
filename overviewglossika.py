import argparse
import math

from random import shuffle
from shutil import rmtree
from convert2mp3 import convert_file_2_mp3
from generator import generate
from create_silence import create_silence_from_file
from utils import makedir, convert_mp3, generate_glossika, make_track, get_num_files, sub_directory, get_name
from config import GLOSSIKA_EN, GLOSSIKA_OVERVIEW, OUTPUT_ALL

def _get_name(prefix, type_output, dir_name, old_start=-1, old_end=-1, silence_padding='0'):
    name = ''
    if prefix == '' or prefix is None:
        if type_output == 'en':
            name = dir_name +'/%04d_%04d_OverviewEN.wav' % (start, end)
        elif type_output == '0':
            name = dir_name + '/%04d_%04d_Overview0.wav' % (start, end)
        elif type_output == '1' or type_output == '2':
            name = dir_name + ('/%04d_%04d_Overview' % (old_start, old_end)) + type_output + '.wav'
    else:
        name = get_name(dir_name, prefix, 2, silence_padding)
    return name


def create_overview_en(files, start, end, to_mp3, prefix='', silence_padding='0'):
    makedir('outputSE')
    result = []
    for f in files:
        silence_file = 'outputSE/' + f.split('/')[-1][:-4] + 's.' f[-3:]
        create_silence_from_file(f, silence_file, silence_padding)
        result += [GLOSSIKA_EN + f.split('/')[-1], silence_file[:-4] + '-p' + silence_padding + silence_file[-4:]]

    dir_name = OUTPUT_ALL + '(wav)/' + sub_directory()
    name = _get_name(prefix, 'en', dir_name, silence_padding)

    makedir(dir_name)
    make_track(result, name)
    convert_mp3(to_mp3, name, dir_name.replace('wav', 'mp3'), artist, album)


def create_overview_0(start, end, to_mp3, prefix=''):
    result = ['outputB/FL-%04d-B%s' % (i, '.wav') for i in range(start, end + 1)]
    dir_name = OUTPUT_ALL + '(wav)/' + sub_directory()
    name = _get_name(prefix, '0', dir_name)
    makedir(dir_name)
    make_track(result, name)
    folder_name = GLOSSIKA_OVERVIEW
    convert_mp3(to_mp3, name, dir_name.replace('wav', 'mp3'), artist, album)


def create_overview(files, start, end, num_files_per_group=8, type_output='B', to_mp3=False,
    artist='Glossika', album='Glossika Training', prefix=''):
    if num_files_per_group == 0:
        num_files_per_group = get_num_files(len(files))
    result = []
    old_start = start
    old_end = end
    start = 0
    end = old_end - old_start + 1
    for i in range(math.ceil((end - start + 1) / num_files_per_group)):
        sub_list = files[start:min(start + num_files_per_group, end)][:]
        result = result + sub_list + sub_list
        start = start + num_files_per_group

    type_num = '1' if type_output == 'B' else '2'
    dir_name = OUTPUT_ALL + '(wav)/' + sub_directory()
    name = _get_name(prefix, type_num, dir_name, old_start, old_end)
    makedir(dir_name)
    make_track(result, name)
    convert_mp3(to_mp3, name, dir_name.replace('wav', 'mp3'), artist, album)

    print ('Shuffle Files: Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make overview tracks from Glossika Training files')
    parser.add_argument('start_track', type=int)
    parser.add_argument('end_track', type=int)
    parser.add_argument('--num_files_per_group','-f', required=False, nargs=1, type=int)
    parser.add_argument('--type','-t', required=False, nargs=1, help='Overview: 0, 1, 2, en, all')
    parser.add_argument('--to_mp3', '-m', nargs='*', required=False,
        help='Files will be converted to mp3 if this value is set True')
    parser.add_argument('--padding', '-o', required=False, nargs=1)
    parser.add_argument('--name', '-n', required=False, nargs=1)

    args = parser.parse_args()

    to_mp3 = not (args.to_mp3 is None)

    artist = 'Glossika'
    album = 'Glossika Training'

    if to_mp3 and len(args.to_mp3) == 2:
        artist = args.to_mp3[0]
        album = args.to_mp3[1]

    start_track = args.start_track
    end_track = args.end_track

    files_B = generate_glossika(start_track, end_track, 'B')
    files_A = generate_glossika(start_track, end_track, 'A')
    files_en = generate_glossika(start_track, end_track, 'en')

    if args.type[0] == 'all':
        create_overview_0(start_track, end_track, to_mp3, args.name[0])
        create_overview_en(files_en, start_track, end_track, to_mp3, args.name[0])
        create_overview(files_B, start_track, end_track, args.num_files_per_group[0], 'B', to_mp3, args.name[0])
        create_overview(files_A, start_track, end_track, args.num_files_per_group[0], 'A', to_mp3, args.name[0])
    else:
        if args.type[0] == '0':
            create_overview_0(start_track, end_track, to_mp3, args.name[0])
        elif args.type[0] == '1':
            create_overview(files_B, start_track, end_track, args.num_files_per_group[0], 'B', to_mp3, args.name[0])
        elif args.type[0] == '2':
            create_overview(files_A, start_track, end_track, args.num_files_per_group[0], 'A', to_mp3, args.name[0])
        elif args.type[0] == 'en':
            create_overview_en(files_en, start_track, end_track, to_mp3, args.name[0], args.padding[0])
