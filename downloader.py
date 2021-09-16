import os
import pytube

songs = {}

class Downloader():
    def __init__(self, queue):
        self.queue = queue
    
    def analyze(self, text):
        self.__download_from_yt_url(text)
    
    def __download_from_yt_url(self, url):
        youtube = pytube.YouTube(url)
        mp3 = youtube.streams.filter(only_audio=True).first()
        mp3.download('./music/queue')
        for file in os.listdir("./music/queue"):
            if file.endswith(".mp4"):
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
    
    def __download_from_yt_name(self):
        pass
    
    def __download_from_spotify_url(self):
        pass
    
    