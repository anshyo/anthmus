from pytube import YouTube
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from moviepy.editor import *
import os
import validators
import shutil as secos

def convert(mp4, mp3):
    # Convert video file (mp4) to audio file (mp3) using MoviePy
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

def get_script_directory():
    # Get the directory where the script is currently running
    return os.getcwd()

def create_directories():
    # Create necessary directories for data, videos, and music
    script_directory = get_script_directory()
    path_data = os.path.join(script_directory, 'data')
    path_videos = os.path.join(script_directory, 'videos')
    path_music = os.path.join(script_directory, 'musics')

    for path in [path_data, path_videos, path_music]:
        os.makedirs(path, exist_ok=True)

    return path_data, path_videos, path_music

def path_find():
    # Find the absolute path of the script
    a = os.path.abspath(__file__)[::-1]
    b = False
    c = ""
    for i in a:
        if i == "\\":
            b = True
        if b:
            c += i
    d = str(c[::-1])
    if "dist" in d:
        d = d[:-5]
    return d

def tube_search(name):
    # Search for videos on YouTube using the youtubesearchpython library
    o = {}
    for i in VideosSearch(name).result()["result"]:
        if len(o) == 5:
            break
        else:
            o[i["title"]] = i["link"]
    return o

def spotify_name(spotify_link):
    # Extract the song name from a Spotify link using web scraping
    response = requests.get(spotify_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        song_name_element = soup.find('meta', property='og:title')
        if song_name_element:
            return song_name_element['content']
        else:
            print('Song name not found on the page.')
            return None
    else:
        print(f'Error: {response.status_code}')
        return None

if __name__ == "__main__":
    # Create directories for data, videos, and music
    path_data, path_videos, path_music = create_directories()

    while True:
        a = input("link/name of song/video: ")
        if a.lower() == "q":
            break
        else:
            b = a
            if b[0:5] == "http":
                b = "http://" + b

            if validators.url(b):
                k = int(input("videos/audio[1/2]: "))
                try:
                    if k == 1:
                        # Download the highest resolution video
                        YouTube(a).streams.get_highest_resolution().download(path_videos)
                    if k == 2:
                        # Download audio only
                        YouTube(a).streams.get_audio_only().download(path_data)
                except Exception as e:
                    print(f"Error downloading: {e}")
                    pass

                try:
                    l = None
                    # Attempt to find a Spotify link and download from there
                    for i in range(3):
                        s = VideosSearch(spotify_name(a)).result()['result'][i]['link']
                        if "https:" in s:
                            l = s
                            break
                        else:
                            continue
                    if k == 1:
                        # Download the highest resolution video from Spotify
                        YouTube(l).streams.get_highest_resolution().download(path_videos)
                    if k == 2:
                        # Download audio only from Spotify
                        YouTube(l).streams.get_audio_only().download(path_data)
                except Exception as e:
                    print(f"Error downloading from Spotify: {e}")
                    pass
            else:
                p, x, y = {}, 0, tube_search(a)
                for i in y.keys():
                    x += 1
                    p[x] = i
                    print(str(x) + ". " + i)
                z = input("1-5: ")
                if int(z) >= 1 and int(z) <= 5:
                    u = input("video/audio[1/2]: ")
                    if int(u) == 1:
                        # Download the highest resolution video from the search results
                        YouTube(y[p[int(z)]]).streams.get_highest_resolution().download(path_videos)
                    if int(u) == 2:
                        # Download audio only from the search results
                        YouTube(y[p[int(z)]]).streams.get_audio_only().download(path_data)

    # Convert downloaded audio files to MP3 and remove the temporary data directory
    for i in os.listdir(path_data):
        convert(os.path.join(path_data, i), os.path.join(path_music, i[0:-1] + "3"))
    secos.rmtree(path_data)

input()
