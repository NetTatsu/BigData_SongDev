import data as d
import csv


class SaveVectorData():
    def __init__(self, SAVE_DIR, SAVE_NAME, songs, SAVE_TYPE):
        self.SAVE_DIR = SAVE_DIR
        self.songs = songs
        self.SAVE_NAME = SAVE_NAME
        self.SAVE_TYPE = SAVE_TYPE

    def save_data(self):
        f = open(f'{self.SAVE_DIR}{self.SAVE_NAME}',
                 'w', encoding='utf-8-sig', newline='')
        writer = csv.writer(f)

        for idx, song in enumerate(self.songs):
            lst = []
            da = d.Data(song)
            da.get_name(lst)
            print(lst)
            if self.SAVE_TYPE == 'GetCentroid':
                data = d.GetCentroid(song)
            elif self.SAVE_TYPE == 'GetFourier':
                data = d.GetFourier(song)
            elif self.SAVE_TYPE == 'GetRolloff':
                data = d.GetRolloff(song)
            elif self.SAVE_TYPE == 'GetBeats':
                data = d.GetBeats(song)
            elif self.SAVE_TYPE == 'GetRMS':
                data = d.GetRMS(song)
            elif self.SAVE_TYPE == 'GetBandwidth':
                data = d.GetBandwidth(song)
            elif self.SAVE_TYPE == 'GetMfccVector':
                data = d.GetMfccVector(song)

            if self.SAVE_TYPE != 'GetHarm' and self.SAVE_TYPE != 'GetPerc':
                if self.SAVE_TYPE != 'GetBeats':
                    tmp = data.get_vector()
                elif self.SAVE_TYPE == 'GetBeats':
                    tmp = data.get_beats()
                for t in tmp:
                    lst.append(t)
            else:
                data = d.GetHarmPerc(song)
                if self.SAVE_TYPE == 'GetHarm':
                    tmp = data.get_harm_vector()
                elif self.SAVE_TYPE == 'GetPerc':
                    tmp = data.get_perc_vector()
                lst.append(tmp)

            lst.append(idx)
            writer.writerow(lst)

        f.close()


class SaveCentroidVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Centroid_SongData.csv', songs, 'GetCentroid')

    def __del__(self):
        print('CentroidVector Delete')


class SaveFourierVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Fourier_SongData.csv', songs, 'GetFourier')

    def __del__(self):
        print('FourierVector Delete')


class SaveRolloffVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Rolloff_SongData.csv', songs, 'GetRolloff')

    def __del__(self):
        print('RolloffVector Delete')


class SaveBeatVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Beat_SongData.csv', songs, 'GetBeats')

    def __del__(self):
        print('BeatVector Delete')


class SaveRMSVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'RMS_SongData.csv', songs, 'GetRMS')

    def __del__(self):
        print('RMSVector Delete')


class SaveHarmVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Harm_SongData.csv', songs, 'GetHarm')

    def __del__(self):
        print('HarmVector Delete')


class SavePercVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Perc_SongData.csv', songs, 'GetPerc')

    def __del__(self):
        print('PercVector Delete')


class SaveBandwidthVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Bandwidth_SongData.csv', songs, 'GetBandwidth')

    def __del__(self):
        print('BandwidthVector Delete')


class SaveMfccVectorData(SaveVectorData):
    def __init__(self, SAVE_DIR, songs):
        SaveVectorData.__init__(
            self, SAVE_DIR, 'Mfcc_SongData.csv', songs, 'GetMfccVector')

    def __del__(self):
        print('MfccVector Delete')


class SaveMeanVarData():
    def __init__(self, SAVE_DIR, songs):
        self.SAVE_DIR = SAVE_DIR
        self.songs = songs
        self.SAVE_NAME = 'SongData.csv'

    def __del__(self):
        print('MeanVar Delete')

    def save_data(self):
        f = open(f'{self.SAVE_DIR}{self.SAVE_NAME}',
                 'w', encoding='utf-8-sig', newline='')
        writer = csv.writer(f)

        for song in self.songs:
            lst = []
            data = d.Data(song)
            data.get_name(lst)
            gc = d.GetCentroidMeanVar(song, lst)
            fo = d.GetFourierMeanVar(song, lst)
            tempo = d.GetTempo(song, lst)
            hp = d.GetHarmPercMeanVar(song, lst)
            mf = d.GetMfccMeanVar(song, lst)

            data_lst = [gc, fo, hp]

            for da_lst in data_lst:
                da_lst.get_mean()
                da_lst.get_var()

            tempo.get_tempo()
            mf.get_mean_var_s(3)
            mf.get_mean_var_s(2)
            writer.writerow(lst)

        f.close()
