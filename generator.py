import os
import subprocess
import sys
from random import shuffle
from shutil import rmtree
import argparse
from create_silence import create_silence_from_folder, create_silence_from_list_of_files
from config import TYPES


if sys.platform == "linux" or sys.platform == "linux2":
    sox = '/usr/bin/sox'
else:
    sox = '/usr/local/bin/sox'


def generate_from_list_of_files(list_of_files, l2, output='Accent', rm_silence=True, silence_padding='0'):
    if l2[-1] != '/': l2 = l2 + '/'
    files_vn = [l2 + f.split('/')[-1][:-6] + 'vn.' + f.split('/')[-1][-3:] for f in list_of_files]
    files_en = list_of_files[:]
    isB = False
    isA = False
    is_en = False
    if output == 'B' or output in TYPES: isB = True
    elif output == 'A': isA = True
    else: is_en = True
    if not os.path.exists('output' + output):
        os.makedirs('output' + output)
    files_vn.sort()
    files_en.sort()
    create_silence_from_list_of_files(files_en, 'outputSE', silence_padding)
    create_silence_from_list_of_files(files_vn, 'outputSV', silence_padding)
    for fe, fv in zip(files_en, files_vn):
        set_type = False
        se = 'outputSE/' + fe.split('/')[-1][:-4] + 's-p' + silence_padding + fe.split('/')[-1][-4:]
        sv = 'outputSV/' + fv.split('/')[-1][:-4] + 's-p' + silence_padding + fv.split('/')[-1][-4:]
        if isB and not set_type:
            file_type = [fv, se, fe, se]
            set_type = True
        elif isA and not set_type:
            file_type = [fv, se, fe, se, fe, se]
            set_type = True
        elif is_en and not set_type:
            file_type = [fe, se]
            set_type = True
        output_name = './output' + output + '/' + fe.split('/')[-1][:-6] + output + fe[-4:]
        if not os.path.exists(output_name):
            subprocess.call([sox,] + file_type + [output_name,])
    if rm_silence:
        rmtree('outputSE')
        rmtree('outputSV')
    print ('Generate Files: Done')
    return True


def generate(l1, l2, start, end, output='B', rm_silence=True, silence_padding='0'):
    '''
    Generate glossika type A (vietnamese + english + english) or type B (vietnamese + english)
    traning .wav files
    l1: folder contains Vietnamese files
    l2: folder contains English files
    start: start track number
    end: end track number
    '''
    if l1[-1] != '/': l1 = l1 + '/'
    if l2[-1] != '/': l2 = l2 + '/'
    files_en = os.listdir(l1)
    files_vn = os.listdir(l2)
    if output == 'B': isB = True
    else: isB = False
    if not os.path.exists('output' + output):
        os.makedirs('output' + output)
    for f in files_en:
        if f[0] == '.' or f[-4:] != '.wav':
            files_en.remove(f)
    for f in files_vn:
        if f[0] == '.' or f[-4:] != '.wav':
            files_vn.remove(f)
    files_vn.sort()
    files_en.sort()
    files_vn = files_vn[start - 1:end]
    files_en = files_en[start - 1:end]
    create_silence_from_folder(l1, 'outputSE', silence_padding)
    create_silence_from_folder(l2, 'outputSV', silence_padding)
    for fe, fv in zip(files_en, files_vn):
        set_type = False
        se = 'outputSE/' + fe[:-4] + 's-p' + silence_padding + fe[-4:]
        sv = 'outputSV/' + fv[:-4] + 's-p' + silence_padding + fv[-4:]
        fe = l1 + fe
        fv = l2 + fv
        if isB and not set_type:
            file_type = [fv, se, fe, se]
            set_type = True
        elif not set_type:
            file_type = [fv, se, fe, se, fe, se]
            set_type = True
        subprocess.call([sox,] + file_type + ['./output' + output + '/' + fe.split('/')[-1][:-7] + '-' + output + fe[-4:],])
    if rm_silence:
        rmtree('outputSE')
        rmtree('outputSV')
    print ('Generate Files: Done')
    return True


def generate_from_arguments(args):
    generate(args.english_folder, args.vietnamese_folder, args.start,
        args.end, args.output_type, args.remove_silence)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate type A or B of Glossika training files')
    parser.add_argument('english_folder')
    parser.add_argument('vietnamese_folder')
    parser.add_argument('start', type=int)
    parser.add_argument('end', type=int)
    parser.add_argument('--output_type', '-o', nargs=1, required=False, default='B', help='Type A or type B')
    parser.add_argument('--remove_silence', '-r', action='store_false',
        help='Set this flag to remove silence folder')
    args = parser.parse_args()
    generate_from_arguments(args)
