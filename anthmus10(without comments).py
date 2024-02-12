from pytube import YouTube
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from moviepy.editor import *
import os
import validators
import shutil as secos

playlist_title = ''

def convert(mp4, mp3):
    # Convert video file (mp4) to audio file (mp3) using MoviePy
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

def get_script_directory():
    # Get the directory where the script is currently running
    return os.getcwd()

def create_directories():
    global path_data, path_videos, path_music, path_playlist_data, path_playlist_music
    # Create necessary directories for data, videos, and music
    script_directory = get_script_directory()
    path_data = os.path.join(script_directory, 'data')
    path_videos = os.path.join(script_directory, 'videos')
    path_music = os.path.join(script_directory, 'musics')
    path_playlist_data = os.path.join(script_directory, f'playlist_data {playlist_title}')
    path_playlist_music = os.path.join(script_directory, f'playlist_music {playlist_title}')

    for path in [path_data, path_videos, path_music, path_playlist_data, path_playlist_music]:
        os.makedirs(path, exist_ok=True)

    return path_data, path_videos, path_music, path_playlist_data, path_playlist_music

path_data, path_videos, path_music, path_playlist_data, path_playlist_music = create_directories()

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
    try:
        o = {}
        for i in VideosSearch(name).result()["result"]:
            if len(o) == 10:
                break
            else:
                x = i["title"]+f"   ({i["duration"]} , {i["publishedTime"]})"
                o[x] = i["link"]
        return o
    except ConnectionError:
        print("Connection error try again later")

def spotify_name(spotify_link):
    # Extract the song name from a Spotify link using web scraping
    response = requests.get(spotify_link)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract song name
        song_name_element = soup.find('meta', property='og:title')
        if song_name_element:
            song_name = song_name_element['content']
        else:
            print('Song name not found on the page.')
            return None

        # Extract singer information
        singer_element = soup.find('meta', property='og:description')
        if singer_element:
            singer_name = singer_element['content'].split(' - ')[-1]
        else:
            print('Singer information not found on the page.')
            singer_name = None

        return song_name+"  "+singer_name

    else:
        print(f'Error: {response.status_code}')
        return None
    
def resolution(link):
    while True:
        ask = input('Select the resolution ("720p", "480p", "360p", "240p", "144p"): ')
        try:
            if ask == "144p" or ask == "240p" or ask == "360p" or ask == "480p" or ask == "720p":
                print(f"({YouTube(link).title})downloading in progress....")
                YouTube(link).streams.get_by_resolution(ask).download(path_videos)
                print("done....")
                print(f"Video downloaded in {ask} resolution.")
                return True
            else:
                print("Invalid resolution. Please choose a valid resolution.")
                return False
        except:
            print("Resolution not available")
            return False

def get_spotify_playlist_musics_name(spotify_playlist_url):
    global playlist_title
    # Extract playlist information from Spotify webpage
    response = requests.get(spotify_playlist_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        playlist_title_element = soup.find('meta', property='og:title')
        if playlist_title_element:
            playlist_title = playlist_title_element['content']
            print(f"Playlist Title: {playlist_title}")

            # Find all song names and artists
            song_meta_tags = soup.find_all('meta', attrs={"name" : "music:song"})
            song_links = []
            for meta_tag in song_meta_tags:
                song_link = meta_tag['content']
                song_links.append(song_link)
            song_names = []
            for i in song_links:
                song_names.append(str(spotify_name(i)))
            
            y = 0 
            for i in song_names:
                y += 1
                print("Songs in the playlist: ")
                print(f"{y}. {i}")
            return(song_names)
            
        else:
            print('Playlist title not found on the page.')
    else:
        print(f'Error: {response.status_code}')

def youtube_downloader_video_link(link):
    while True:
        a = resolution(link) 
        if a:
            break
        
        
def youtube_downloader_audio_link_playlist(link):
    print(f"({YouTube(link).title})downloading in progress....")
    YouTube(link).streams.get_audio_only().download(path_playlist_data)
    print("done...")

def youtube_downloader_audio_link(link):
    print(f"({YouTube(link).title})downloading in progress....")
    YouTube(link).streams.get_audio_only().download(path_data)
    print("done...")

def youtube_download_video_name(name):
    a = tube_search(name)
    b = 0
    for i in a.keys():
        b += 1
        print(f"{b}. {i}")

    ask = input("1-10: ")
    if 0 < int(ask) < 11 :
        c = 0
        for i in a.keys():
            c += 1
            if c == int(ask):
                youtube_downloader_video_link(a[i])
                break

def youtube_download_audio_name(name):
    a = tube_search(name)
    b = 0
    for i in a.keys():
        print(f"{b}. {i}")
        b += 1
    ask = input("1-10['c' to cancel]: ")
    if 0 < ask > 11 :
        c = 0
        for i in a.keys():
            if c == ask:
                youtube_downloader_audio_link(a[i])
                break
            c += 1
    if ask == "c":
        print("task is cancelled")
        main()
    else:
        print("invalid input")

def youtube_download_audio_name_playlist(name):
    a = tube_search(name)
    b = 0
    for i in a.values():
        if b < 1:
            youtube_downloader_audio_link_playlist(i)
        else:
            break
        b += 1

def youtube_download_audio_name_1st(name):
    a = tube_search(name)
    b = 0
    for i in a.values():
        if b < 1:
            youtube_downloader_audio_link(i)
        else:
            break
        b += 1

def check_link(link):
    a = True
    l = str(link)
    if "http" or "https" in l[0:10]:
        pass
        if validators.url(link):
            pass
        else:
            a = False
    else:
        a = False
    return a
        
def spotify_playlist_download(link):
    a = get_spotify_playlist_musics_name(link)
    path_data, path_videos, path_music, path_playlist_data, path_playlist_music = create_directories()

    for i in a:
        youtube_download_audio_name_playlist(i)
    
    for i in os.listdir(path_playlist_data):
        convert(os.path.join(path_playlist_data, i), os.path.join(path_playlist_music, i[0:-1] + "3"))
    secos.rmtree(path_playlist_data)

def main():
    print("'q' for quit | 'h' for help")
    while True:
        ask = input("Task: ")

        if ask == "h":
            print("""
Make your spotify offline experince thrifty by stepping up with Anthmus!
                  
The cost effective way to listen to your favorite songs or podcast wherever you enjoy.
With anthmus you can download songs and videos directly from popular streaming platforms youtube and spotify

1. "sp" to show up spotify downloader prompt
2. "yt" to show up youtube downloader prompt
                  
you can enter "q" to cancel any operation
            """)

        elif ask == "q":
            break

        elif ask == "yt":
            while True:
                os.system("cls")
                linkname = input("yt: ")
                opt = input("audio/video[1/2]: ")
                if check_link(linkname):
                    if opt == "1":
                        youtube_downloader_audio_link(linkname)
                    elif opt == "2":
                        youtube_downloader_video_link(linkname)
                    elif opt == "q":
                        break
                    else:
                        print("invalid input")
                else:
                    if opt == "1":
                        youtube_download_audio_name(linkname)
                    elif opt == "2":
                        youtube_download_video_name(linkname)
                    elif opt == "q":
                        break
                    else:
                        print("invalid input")

        elif ask == "sp":
            print("links only.....")
            while True:
                os.system("cls")
                while True:
                    a = input("playlist/song[1/2]: ")
                    if a == "1" or  a == "2":
                        break
                    elif a == "q":
                        break
                    else:
                        print("invalid input!")
                while True:
                    link = input("sp: ")
                    if validators.url(link):
                        break
                    elif link == "q":
                        break
                    else:
                        print("invalid input!")
                if a == "1":
                    spotify_playlist_download(link)
                elif a == "2":
                    youtube_download_audio_name_1st(spotify_name(link))
                elif a == "q":
                    break
                else:
                    print("invalid input!")
                    
if __name__ == "__main__":
    main()
    path_data, path_videos, path_music, path_playlist_data, path_playlist_music = create_directories()
    for i in os.listdir(path_data):
        convert(os.path.join(path_data, i), os.path.join(path_music, i[0:-1] + "3"))
    secos.rmtree(path_data)