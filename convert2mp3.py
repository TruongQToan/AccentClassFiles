import eyed3
import os
import subprocess
import argparse
import sys
import eyed3


if sys.platform == "linux" or sys.platform == "linux2":
    lame = '/usr/bin/lame'
else:
    lame = '/usr/local/bin/lame'


def convert_file_2_mp3(input_file, output_file, artist='', album=''):
    lame_paras = '-V 5 --vbr-new'
    args = [lame,] + [lame_paras,] + [input_file] + [output_file]
    subprocess.call(args)
    ''' ID3 is used to change meta information of mp3 file'''
    mp3file = eyed3.load(output_file)
    mp3file.initTag()
    mp3file.tag.artist = artist
    mp3file.tag.album = album

    mp3file.tag.save()


def convert_folder_2_mp3(input_folder, output_folder='Output(wav)', artist='', album=''):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for f in os.listdir(input_folder):
        if not (f[-3:] == 'wav'): continue
        convert_file_2_mp3(input_folder + '/' + f, output_folder + '/' + f.replace('wav', 'mp3'), artist, album)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Convert one file or files in a folder from .wav to .mp3')
    parser.add_argument('--one_file', '-o', action='store_true', help='set true to convert one file')
    parser.add_argument('input',
        help='Input file or folder. If -o is set, the value is name of a file, otherwise, it is the name of a folder')
    parser.add_argument('output', default='Output(wav)',
        help='Output folder or file. If folder, the default output folder is Output(wav)')
    args = parser.parse_args()
    if args.one_file:
        convert_file_2_mp3(args.input, args.output)
    else: convert_folder_2_mp3(args.input, args.output)
