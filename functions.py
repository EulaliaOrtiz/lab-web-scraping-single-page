
import numpy as np
import pandas as pd
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import *

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                         client_secret= client_secret))

def search_song_ids(df, stepsize=20):
    
    song_ids = []
    
    for number in range(0,len(df),stepsize):
        print("Getting the song ids for the chunk:",number)
        print()
        for index in list(range(len(df)))[number:number+stepsize]:
            artist = df.iloc[index,1]
            title = df.iloc[index,0]
            try:
                results = sp.search(q="track:"+title+" artist:"+artist,limit=1)
                song_id = results['tracks']['items'][0]['id']
                song_ids.append(song_id)
            except:
                print("The song: {} of artist: {} is not on Spotify".format(title, artist))
                song_ids.append(np.nan)
        sleep(20)
        print()
        print()
    return song_ids

def get_audio_features(df, stepsize=20):
    
    song_features = []
    for number in range(0,len(df),stepsize):
        print("Getting the features for the chunk:",number)
        print()
        for index in list(range(len(df)))[number:number+stepsize]:
            song_id = df.iloc[index,0]
            try:
                my_dict = sp.audio_features(song_id)[0]
                song_features.append(my_dict)
                
            except:
                print("The features for {} are not in spotify".format(song_id))
                my_new_dict = {}
                song_features.append(my_new_dict)
        
                
        sleep(20)
        print()
        print()
    song_features = pd.DataFrame(song_features)
    return song_features
def add_audio_features(df, audio_features_df):
    df_final = pd.concat([df.reset_index(), audio_features_df], axis=1)
    df_final.drop(columns=['index', 'id'], inplace=True)
    return df_final
