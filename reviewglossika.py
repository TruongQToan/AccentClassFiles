import os
import subprocess
from random import shuffle
from shutil import rmtree
import eyed3
import argparse
import sys
from utils import shuffle_track, convert_mp3, print_log, get_name, makedir, generate_glossika, make_track, get_num_files, sub_directory
from config import OUTPUT_ALL


def create_review(files, start, end, num_plays, num_files_per_group, log=False,
    log_tracks=0, num_copies=1, to_mp3=False, artist='Glossika', silence_padding='0', album='Glossika Training', name=None):
    '''
    Combine files to make them useful for Glossika Traning
    numPlays: each track is played numPlays times
    numFilesPerTrack: the number of tracks per playlist
    start: start track number
    end: end track number
    log: set True to print debug information
    logTracks: use in debug mode
    numCopies: number of copies of output file
    toMP3: set True to convert output file to .mp3
    artist:
    album: if toMP3=True, use these values to set meta information
    '''
    makedir('output_B')
    # if shuffled == 'all': shuffle(files)
    if num_files_per_group == 0:
        num_files_per_group = get_num_files(len(input_files))
    # Shuffle files
    prefix = 'Review_%04d_%04d' % (start, end)
    if name is not None and not name == '':
        prefix = name
    for copies in range(int(num_copies)):
        result = shuffle_track(files, num_plays, num_files_per_group)
        dir_name = OUTPUT_ALL + '(wav)/' + sub_directory()
        if not os.path.exists(dir_name):
            makedir(dir_name)
        name = get_name(dir_name, prefix, num_plays, silence_padding)
        make_track(result, name)
        convert_mp3(to_mp3, name, dir_name.replace("wav", "mp3"), artist, album)
        print_log(log, log_tracks, result)
    print ('Shuffle Files: Done')


def get_files(lists, shuffled, silence_padding='0'):
    files = []
    min_start = 5000
    max_end = -1
    for i in range(len(lists)):
        start = int(lists[i].split('-')[0])
        if start < min_start: min_start = start
        end = int(lists[i].split('-')[1])
        if end > max_end: max_end = end
        files += generate_glossika(start, end, shuffled=shuffled, silence_padding=silence_padding)
    if shuffled == 'all': shuffle(files)
    return (files, min_start, max_end)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make review tracks from Glossika training files ')
    parser.add_argument('--num_files_per_group','-f', required=False, nargs=1, type=int)
    parser.add_argument('--num_plays', '-p', required=False, nargs=1, type=int)
    parser.add_argument('--num_copies', '-c', required=False, nargs=1, type=int)
    parser.add_argument('--to_mp3', '-m', nargs='*', required=False,
        help='Files will be converted to mp3 if this value is set True')
    parser.add_argument('--name', '-n', required=False, nargs=1)
    parser.add_argument('--log', '-x', nargs=1, required=False, help='log')
    parser.add_argument('--all', '-a', action='store_true', required=False)
    parser.add_argument('--shuffled', '-s', required=False, nargs=1, help='Shuffle the original list')
    parser.add_argument('--padding', '-o', required=False, nargs=1)
    parser.add_argument('--list', '-l', required=False, nargs='*', help='sublist name to create track')
    args = parser.parse_args()

    if args.to_mp3 and len(args.to_mp3) == 2:
        artist = args.to_mp3[0]
        album = args.to_mp3[1]
    to_mp3 = not (args.to_mp3 is None)
    log = not (args.log is None)
    log_tracks = 0
    name = None

    if args.name is not None:
        name = args.name[0]

    if log:
        log_tracks = int(args.log[0])
    shuffled = ''
    if args.shuffled is not None:
        shuffled = args.shuffled[0]

    artist = 'Glossika'
    album = 'Glossika Training'

    if args.all:
        for num_plays in [2, 3, 4]:
                files, min_start, max_end = get_files(args.list, shuffled, args.padding[0])
                if min_start < max_end:
                    create_review(files, start=min_start,
                        end=max_end,
                        num_plays=num_plays,
                        num_copies=2,
                        num_files_per_group=8,
                        to_mp3=to_mp3,
                        log=log,
                        log_tracks=log_tracks,
                        artist=artist,
                        album=album,
                        silence_padding=args.padding[0],
                        name=name)
    else:
        files, min_start, max_end = get_files(args.list, shuffled, args.padding[0])
        if min_start < max_end:
            create_review(files, start=min_start,
                end=max_end,
                num_plays=args.num_plays[0],
                num_copies=args.num_copies[0],
                num_files_per_group=args.num_files_per_group[0],
                to_mp3=to_mp3,
                log=log,
                log_tracks=log_tracks,
                artist=artist,
                album=album,
                silence_padding=args.padding[0],
                name=name)
