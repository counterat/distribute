import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
client_id = '8ccffb84f0984afb8645f880e838023d'
secret = 'f33cc4ff360c44be966881ef91d71614'

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)


def search_tracks_in_spotify(text:str):
    list_of_tracks = []
    for i in (spotify.search(f'{text}', limit=50))['tracks']['items']:
        name_of_artist = (i['artists'][0]['name'])
        track_title = i['name']
        list_of_tracks.append(f'{name_of_artist} - {track_title}')
    return  list_of_tracks
def download_video_from_yt(text:str, folder_name):
    videosSearch = VideosSearch(text, limit=1)
    yt = YouTube(videosSearch.result()['result'][0]['link'])
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Скачайте аудио в текущую директорию

    audio_stream.download(filename_prefix=f'''{folder_name}\\''', filename=f'{text}.mp4')

