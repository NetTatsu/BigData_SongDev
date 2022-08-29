from similarity import get_similarity_result as get_result
from similarity import get_songnames as sn
import pandas as pd


def preprocessing_song(DATA_DIR):
    import song as s

    dir = s.Dir(DATA_DIR)
    dir.__mkdir__()
    cnv = s.ConvertMP3ToWAV(DATA_DIR)
    cnv.convert()
    sp = s.SplitSong(DATA_DIR)
    sp.split()
    so = s.Song(DATA_DIR, 'wav')
    songs = so.get_songs()
    return songs


def get_mfcc_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveMfccVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_centroid_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveCentroidVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_fourier_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveFourierVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_rolloff_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveRolloffVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_harm_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveHarmVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_perc_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SavePercVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_bandwidth_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveBandwidthVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_rms_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveRMSVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_beat_vector(SAVE_DIR, songs):
    import save_data as sd

    save = sd.SaveBeatVectorData(SAVE_DIR, songs)
    save.save_data()
    del save


def get_mean_var_data(SAVE_DIR, songs):
    import save_data as sd
    save = sd.SaveMeanVarData(SAVE_DIR, songs)
    save.save_data()
    del save


def save_datas(SAVE_DIR, songs):
    get_mean_var_data(SAVE_DIR, songs)
    get_mfcc_vector(SAVE_DIR, songs)
    get_centroid_vector(SAVE_DIR, songs)
    # get_fourier_vector(SAVE_DIR, songs)
    get_rolloff_vector(SAVE_DIR, songs)
    # get_harm_vector(SAVE_DIR, songs)
    # get_perc_vector(SAVE_DIR, songs)
    get_bandwidth_vector(SAVE_DIR, songs)
    # get_rms_vector(SAVE_DIR, songs)
    # get_beat_vector(SAVE_DIR, songs)


# def add_header(SAVE_DIR):
#     import preprocessing_csv as pc
#     filenames = ['Bandwidth_SongData.csv', 'Centroid_SongData.csv', 'Fourier_SongData.csv',
#                  'Harm_SongData.csv', 'MFCC_SongData.csv', 'Perc_SongData.csv', 'RMS_SongData.csv', 'Rolloff_SongData.csv']

#     for file in (filenames):
#         r = pc.ReadCSV(SAVE_DIR, file, None)
#         df = r.get_data()
#         df = df.dropna()
#         pointer = 0
#         names = []
#         songname = df.iloc[pointer, 0]

#         for idx, data in enumerate(range(len(df))):
#             if songname != df.iloc[idx, 0]:
#                 pointer = idx
#             songname = df.iloc[pointer, 0]
#             names.append(pointer)
#         df['song_start'] = names
#         new_filename = f'New_{file}'
#         s = pc.SaveCSV(SAVE_DIR, new_filename, df)
#         s.save_data()
#         del r
#         del s

def get_result_name(result) :
    result = result.to_dict()
    dic_key = result.keys()
    tmp = None

    for i in dic_key :
        tmp = result.get(i)
    tmp2 = []

    for i in tmp.keys():
        tmp2.append(i)

    return tmp2

if __name__ == '__main__':

    SONG_DIR = '.\\Song\\'
    DATA_DIR = '.\\data\\'
    SAVE_DIR = '.\\db_data\\'
    songs = preprocessing_song(SONG_DIR)
    save_datas(DATA_DIR, songs)
    user_name, db_name = sn(DATA_DIR, SAVE_DIR)
    result = get_result(DATA_DIR, SAVE_DIR)
    print(result)
    names = get_result_name(result)

    for i in names :
        if i < len(db_name) :
            print(db_name[i])