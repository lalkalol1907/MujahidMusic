import os
import pytube
import validators
from youtube_search import YoutubeSearch
import pyglet

numbers = []
urls = []
names = []
long = []


class Downloader():
    def __init__(self, queue, ctx):
        self.queue = queue
        self.ctx = ctx
    
    def analyze(self, text):
        if validators.url(text):
            if "spotify" in text: self.__download_from_spotify_url(text)
            elif "youtube" in text or "youtu.be" in text: self.__download_from_yt_url(text)
        else: self.__download_from_yt_url(f"https://www.youtube.com{YoutubeSearch(text, max_results=1).to_dict()[0]['url_suffix']}")
        
    def __download_from_yt_url(self, url):
        global songs
        youtube = pytube.YouTube(url)
        mp3 = youtube.streams.filter(only_audio=True).first()
        mp3.download('./music')
        for file in os.listdir("./music"):
            if file.endswith(".mp4"):
                name = file
                if self.queue != -1:
                    try:
                        os.rename(f"./music/{file}", f"./music/queue/song{self.queue+1}.mp3")
                        self.queue+=1
                    except FileExistsError:
                        for file1 in os.listdir("./music/queue"):
                            if file1.endswith(".mp3"):
                                try:
                                    os.remove(f"./music/queue/{file1}")
                                except FileNotFoundError:
                                    pass
                        os.rename(f"./music/{file}", f"./music/queue/song{self.queue+1}.mp3")
                        self.queue+=1         
                else:
                    try:
                        os.rename(f"./music/{file}", './music/queue/song0.mp3')
                        self.queue = 0
                    except FileExistsError:
                        for file1 in os.listdir("./music/queue"):
                            if file1.endswith(".mp3"):
                                try:
                                    os.remove(f"./music/queue/{file1}")
                                except FileNotFoundError:
                                    pass
                        os.rename(f"./music/{file}", './music/queue/song0.mp3')
                        self.queue = 0
                names.append(f"{name[:-4]}")
                urls.append(url)
                numbers.append(self.queue)
    
    def __download_from_spotify_url(self, url):
        pass
    
    