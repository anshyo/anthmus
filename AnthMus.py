from pytube import YouTube
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from moviepy.editor import *
import os
import validators
import shutil as secos

def convert(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

def tubeSearch(name):
    o = {}
    for i in VideosSearch(name).result()["result"]:
        if len(o)==5:
            break
        else:
            o[i["title"]] = i["link"]
    return o

def spotifyName(spotify_link):
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
    while True:
        pathData = '\\data\\'
        pathVideos = '\\videos\\'
        a = input("link/name of song/video: ")
        if a == "q":
            break
        else:
            b = a
            if b[0:5] == "http":
                b = "http://" + b

            if validators.url(b):
                k = int(input("videos/audio[1/2]: "))
                try:
                    if k == 1:
                        YouTube(a).streams.get_highest_resolution().download(pathVideos)
                    if k == 2:
                        YouTube(a).streams.get_audio_only().download(pathData)
                except:
                    pass
                try:
                    l = None
                    for i in range(3):
                        s = VideosSearch(spotifyName(a)).result()['result'][i]['link']
                        if "https:" in s:
                            l = s
                            break
                        else:
                            continue
                    if k == 1:
                        YouTube(l).streams.get_highest_resolution().download(pathVideos)
                    if k == 2:
                        YouTube(l).streams.get_audio_only().download(pathData)
                except:
                    pass
                
                    
            else:
                p , x , y = {} , 0 , tubeSearch(a)
                for i in y.keys():
                    x += 1
                    p[x] = i
                    print(str(x)+". "+i)
                z = input("1-5: ")
                if int(z) >= 1 and int(z) <=5:
                    u = input("video/audio[1/2]: ")
                    if int(u) == 1:
                        YouTube(y[p[int(z)]]).streams.get_highest_resolution().download(pathVideos)
                    if int(u) == 2:
                        YouTube(y[p[int(z)]]).streams.get_audio_only().download(pathData)
        os.system("cls")

    for i in os.listdir("\\data"):
        convert(pathData+i,"\\musics\\"+i[0:-1]+"3")
    secos.rmtree(pathData)
input()