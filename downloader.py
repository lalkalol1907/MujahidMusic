import os
import pytube
import validators
from youtube_easy_api.easy_wrapper import *

songs = {}

class Downloader():
    def __init__(self, queue):
        self.queue = queue
    
    def analyze(self, text):
        if validators.url(text):
            self.__download_from_yt_url(text)
        else:
            self.__download_from_yt_name(text)
    
    def __download_from_yt_url(self, url):
        global songs
        youtube = pytube.YouTube(url)
        mp3 = youtube.streams.filter(only_audio=True).first()
        mp3.download('./music/queue')
        for file in os.listdir("./music/queue"):
            if file.endswith(".mp4"):
                name = file
                if self.queue != -1:
                    try:
                        os.rename(f"./music/queue/{file}", f"./music/queue/song{self.queue+1}.mp3")
                        self.queue+=1
                    except FileExistsError:
                        for file1 in os.listdir("./music/queue"):
                            if file1.endswith(".mp3"):
                                try:
                                    os.remove(f"./music/queue/{file1}")
                                except FileNotFoundError:
                                    pass
                        os.rename(f"./music/queue/{file}", f"./music/queue/song{self.queue+1}.mp3")
                        self.queue+=1         
                else:
                    try:
                        os.rename(f"./music/queue/{file}", './music/queue/song0.mp3')
                        self.queue = 0
                    except FileExistsError:
                        for file1 in os.listdir("./music/queue"):
                            if file1.endswith(".mp3"):
                                try:
                                    os.remove(f"./music/queue/{file1}")
                                except FileNotFoundError:
                                    pass
                        os.rename(f"./music/queue/{file}", './music/queue/song0.mp3')
                        self.queue = 0
                songs.update({self.queue:f"{name[:-4]}"})
    
    def __download_from_yt_name(self, text):
       # print(text)
        easy_wrapper = YoutubeEasyWrapper()
        easy_wrapper.initialize(api_key="AIzaSyCFtJa3RLtp1DhjzCxG2Ms8Ge2ygwhLhBs")
        results = easy_wrapper.search_videos(search_keyword=text,
                                     order='relevance')
        finres = results[0]
        """for res in results:
            if res['date']"""
        url = f"https://youtu.be/{finres['video_id']}"
        self.__download_from_yt_url(url)
    
    def __download_from_spotify_url(self, url):
        pass
    
    