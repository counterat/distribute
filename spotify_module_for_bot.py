import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pytube import YouTube
from youtubesearchpython import VideosSearch
import requests
from mutagen.mp3 import MP3
from io import BytesIO
import youtube_dl
import os

client_id = '8ccffb84f0984afb8645f880e838023d'
secret = 'f33cc4ff360c44be966881ef91d71614'

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)


def search_tracks_in_spotify(text:str, limit = 10):
    list_of_tracks = []
    for i in (spotify.search(f'{text}', limit=limit))['tracks']['items']:
        name_of_artist = (i['artists'][0]['name'])
        track_title = i['name']
        list_of_tracks.append(f'{name_of_artist} - {track_title}')
    return  list_of_tracks
def download_video_from_yt(text:str, folder_name, inline_query = False):
    videosSearch = VideosSearch(text, limit=1)
    yt = YouTube(videosSearch.result()['result'][0]['link'])
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Скачайте аудио в текущую директорию
    if not inline_query:
        audio_stream.download(filename_prefix=f'''{folder_name}\\''', filename=f'{text}.mp4')
    else:
        return audio_stream.url
def download_video_from_yt_by_link(link:str, folder_name:str):
    yt = YouTube(link)
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Скачайте аудио в текущую директорию

    audio_stream.download(filename_prefix=f'''{folder_name}\\''', filename=f'{yt.title}.mp4')

    return  yt.title


def get_audio_link_from_video(text):
    try:

        videosSearch = VideosSearch(text, limit=1)
        youtube_url = videosSearch.result()['result'][0]['link']
        # Создаем объект YouTube
        yt = YouTube(youtube_url)




        # Получаем аудиопоток
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Возвращаем ссылку на аудио
        print(audio_stream.url)
        return audio_stream.url
    except Exception as e:
        print(f"Error: {e}")
        return None


def download_soundcloud_track(track_url):
    # Отправляем GET-запрос к странице трека
    response = requests.get(track_url)

    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    # Находим тег с аудио-файлом
    audio_tag = soup.find('meta', {'property': 'og:audio'})
    print(audio_tag)
    if audio_tag:
        # Получаем URL аудио-файла
        audio_url = audio_tag['content']

        print(audio_url)

    else:
        print("Аудио-файл не найден.")
        return None




