import os
import os.path
from pydub import AudioSegment
from glob import glob
import librosa


class Dir:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def __del__(self):
        print('Dir DELETE')

    def __mkdir__(self):
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def __showdir__(self):
        print('dir = {0}'.format(self.data_dir))


class Song:
    def __init__(self, data_dir, now_extension):
        self.data_dir = data_dir
        self.now_extension = now_extension
        self.songs = glob(self.data_dir + '*.' + self.now_extension)
        self.sample_rate = 44100

    def __del__(self):
        print('Song DELETE')

    def show_all(self):
        for song in self.songs:
            print(song)

    def show_mp3(self):
        for song in self.songs:
            if song.split('.')[-1] == 'mp3':
                print(song)

    def show_wav(self):
        for song in self.songs:
            if song.split('.')[-1] == 'wav':
                print(song)

    def get_songs(self):
        return self.songs


class ConvertMP3ToWAV(Song):
    def __init__(self, data_dir):
        Song.__init__(self, data_dir, 'mp3')
        self.after_extension = 'wav'

    def __del__(self):
        print('ConvertMP3ToWAV DELETE')

    def convert(self):
        for song in self.songs:
            if song.split('.')[-1] == self.now_extension:
                name = song.rstrip('.{0}'.format(self.now_extension))
                dst = f'{name}.{self.after_extension}'
                audio = AudioSegment.from_mp3(song)
                audio.export(dst, format=self.after_extension)
            os.remove(song)


class SplitSong(Song):
    def __init__(self, data_dir):
        Song.__init__(self, data_dir, 'wav')

    def __del__(self):
        print('SplitSong DELETE')

    def split(self):
        for song in self.songs:
            if song.split('.')[-1] == self.now_extension:
                new_song = AudioSegment.from_wav(song)
                y, sr = librosa.load(song, self.sample_rate)
                fin = len(y) / sr
                count = 0
                name = song.rstrip('.{0}'.format(self.now_extension))

                while True:
                    if fin >= 60:
                        if fin // ((count + 1) * 60) < 1:
                            break
                    else:
                        break
                    pointer = 60 * count
                    start = pointer * 1000
                    finish = (pointer + 60) * 1000
                    dst = '{0}_{1}.{2}'.format(name, count, self.now_extension)
                    count += 1

                    save_song = new_song[start: finish]
                    save_song.export(dst, format=self.now_extension)
                os.remove(song)
