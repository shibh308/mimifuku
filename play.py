import pathlib
import random
import time
import pydub
import pydub.playback

OUTPUT_ROOT_DIR = pathlib.Path(__file__).parent / 'output'
PAPERS_DIR = OUTPUT_ROOT_DIR / 'papers'
CTF_DIR = OUTPUT_ROOT_DIR / 'ctf'
HASH_FILE = OUTPUT_ROOT_DIR / 'hash.txt'


def play_shuffled_mp3s(directory: pathlib.Path):
    mp3_files = list(directory.glob('*.mp3'))
    while True:
        random.shuffle(mp3_files)
        for mp3_file in mp3_files:
            print(mp3_file)
            audio = pydub.AudioSegment.from_mp3(mp3_file)
            pydub.playback.play(audio)
            time.sleep(1)

def main():
    play_shuffled_mp3s(PAPERS_DIR)

if __name__ == '__main__':
    main()