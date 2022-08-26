from msilib.schema import Class
from re import L
import librosa
import pandas as pd
import numpy as np
from pydub import AudioSegment
from glob import glob
from sklearn.preprocessing import minmax_scale

import song as s


class Data:
    def __init__(self, song):
        self.song = song
        self.sample_rate = 44100
        self.y, self.sr = librosa.load(self.song, sr=self.sample_rate)
        self.song_length = len(self.y) / self.sr
        self.name = self.song.split('_')[0].split('\\')[-1]
        self.pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))
    
    def normalize(x, axis=0):
        return minmax_scale(x, axis=axis)

    def get_name(self, lst):
        lst.append(self.name)


class GetCentroid(Data):
    def __init__(self, song):
        Data.__init__(self, song)
        self.centroids = librosa.feature.spectral_centroid(self.y, self.sr)[0]

    def get_vector(self):
        # pad_centroid = self.pad2d(self.centroids, 60)
        return self.centroids


class GetCentroidMeanVar(GetCentroid) :
    def __init__(self, song, lst) :
        GetCentroid.__init__(self, song)
        self.lst = lst
    def get_mean(self):
        mean = self.centroids.mean()
        self.lst.append(mean)

    def get_var(self):
        var = self.centroids.var()
        self.lst.append(var) 
          
class GetFourier(Data):
    def __init__(self, song):
        Data.__init__(self, song)
        self.D = np.abs(librosa.stft(self.y, n_fft=2048, hop_length=512))

    def get_vector(self):
        # pad_fourier = self.pad2d(self.D, 60)
        return self.D

class GetFourierMeanVar(GetFourier) :
    def __init__(self, song, lst) :
       GetFourier.__init__(self, song)
       self.lst = lst
       
    def get_mean(self):
        mean = self.D.mean()
        self.lst.append(mean)

    def get_var(self):
        var = self.D.var()
        self.lst.append(var)
   
class GetRolloff(Data):
    def __init__(self, song):
        Data.__init__(self, song)
        self.rolloff = librosa.feature.spectral_rolloff(self.y, self.sr)[0]
        self.rolloff_scaled = Data.normalize(self.rolloff)

    def get_vector(self):
        return self.rolloff_scaled


class GetTempo(Data):
    def __init__(self, song, lst):
        Data.__init__(self, song)
        self.tempo, _ = librosa.beat.beat_track(self.y, self.sr)
        self.lst = lst

    def get_tempo(self):
        self.lst.append(self.tempo)


class GetBeats(Data) :
    def __init__(self, song) :
        Data.__init__(self, song)
        _, self.beats = librosa.beat.beat_track(self.y, self.sr)
        
    def get_beats(self) :
        return self.beats
    
class GetRMS(Data):
    def __init__(self, song):
        Data.__init__(self, song)
        self.rms = librosa.feature.rms(self.y)

    def get_vector(self):
        return self.rms


class GetHarmPerc(Data):
    def __init__(self, song):
        Data.__init__(self, song)
        self.harm, self.perc = librosa.effects.hpss(self.y)

    def get_harm_vector(self):
        # pad_harm = self.pad2d(self.harm, 60)
        return self.harm
        # return pad_harm
    
    def get_perc_vector(self):
        # pad_perc = self.pad2d(self.perc, 60)
        return self.perc
        # return pad_perc
    
class GetHarmPercMeanVar(GetHarmPerc) :
    def __init__(self, song, lst):
        GetHarmPerc.__init__(self, song)
        self.lst = lst
    
    def get_mean(self):
        h_mean = self.harm.mean()
        p_mean = self.perc.mean()
        self.lst.append(h_mean)
        self.lst.append(p_mean)

    def get_var(self):
        h_var = self.harm.var()
        p_var = self.perc.var()
        self.lst.append(h_var)
        self.lst.append(p_var)
        

class GetBandwidth(Data):
    def __init__(self, song):
        Data.__init__(self, song)
        self.bandwidth = librosa.feature.spectral_bandwidth(self.y, self.sr)[0]

    def get_vector(self):
        # pad_bandwidth = self.pad2d(self.bandwidth, 60)
        return self.bandwidth


class GetMfccVector(Data):
    def __init__(self, song):
        Data.__init__(self, song)
        self.mfcc = librosa.feature.mfcc(
            self.y, self.sr, n_mfcc=200, n_fft=1100, hop_length=441)
        self.mfcc_scaled = Data.normalize(self.mfcc, 1)
        

    def get_vector(self):
        pad_mfcc = self.pad2d(self.mfcc_scaled, 60)
        return pad_mfcc


class GetMfccMeanVar(Data):
    def __init__(self, song, lst):
        Data.__init__(self, song)
        self.lst = lst

    def get_mean_var_s(self, sec):
        count = 1

        while count < (self.song_length / sec):
            pointer = count
            start = pointer * sec * 1000
            finish = (pointer + 1) * sec * 1000
            mfcc = librosa.feature.mfcc(self.y[start: finish], self.sr)
            mfcc_scaled = Data.normalize(mfcc, 1)
            m_mean = mfcc_scaled.mean()
            m_var = mfcc_scaled.var()
            self.lst.append(m_mean)
            self.lst.append(m_var)
            count += 1
