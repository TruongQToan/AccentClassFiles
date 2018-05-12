from mixtracks import mix
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Make Accent/Grammer files from a list of tracks")
    parser.add_argument('num_files_per_group', type=int)
    parser.add_argument('num_plays', type=int)
    parser.add_argument('num_copies', type=int)
    parser.add_argument('--name', '-n', required=True, nargs=1)
    parser.add_argument('--to_mp3', '-m', required=False, nargs='*')
    parser.add_argument('--padding', '-o', required=False, nargs=1)
    parser.add_argument('--list_of_tracks', '-l', nargs='+', required=True, type=str, help='List of tracks to combine. Ex: -l 6 9 10')
    parser.add_argument("--shuffled", '-s', nargs=1, required=False)
    args = parser.parse_args()
    to_mp3 = not (args.to_mp3 is None)
    if to_mp3 and len(args.to_mp3) == 2:
        artist = args.to_mp3[0]
        album = args.to_mp3[1]
    mix(args.list_of_tracks, args.num_files_per_group, 
        args.num_plays, args.num_copies, args.name[0], to_mp3, args.shuffled[0], args.padding[0])
