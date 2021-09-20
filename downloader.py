import os
import pytube
import validators
from youtube_search import YoutubeSearch
import pyglet
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

songs = list()

class Song:
    def __init__(self, number, url, name, long):
        self.number = number
        self.url = url
        self.name = name
        self.long = long


class Downloader():
    def __init__(self, queue, ctx):
        self.queue = queue
        self.ctx = ctx
    
    async def analyze(self, text):
        if validators.url(text):
            if "spotify" in text: 
                await self.__download_from_spotify_url(text)
            elif "youtube" in text or "youtu.be" in text: 
                await self.__download_from_yt_url(text)
        else: 
            await self.__download_from_yt_url(f"https://www.youtube.com{YoutubeSearch(text, max_results=1).to_dict()[0]['url_suffix']}")
        
    async def __download_from_yt_url(self, url):
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
                        for file2 in os.listdir("./music/queue"):
                            try:
                                if "song" in file:
                                    os.remove(f"./music/queue/{file1}")
                            except FileNotFoundError: pass
                        os.rename(f"./music/{file}", './music/queue/song0.mp3')
                        self.queue = 0
                    except FileExistsError:
                        for file1 in os.listdir("./music/queue"):
                            if file1.endswith(".mp3"):
                                try:
                                    os.remove(f"./music/queue/{file1}")
                                except FileNotFoundError: pass
                        os.rename(f"./music/{file}", './music/queue/song0.mp3')
                        self.queue = 0
                songs.append(Song(self.queue, url, f"{name[:-4]}", pyglet.media.load(f"./music/queue/song{self.queue}.mp3").duration))
    
    async def __download_from_spotify_url(self, url):
        session = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="6a3124a2b3df4275a177a80104f534d0", client_secret="704142bf3e914d24b4a45bd5df087ed4"))
        track = session.track(url)
        artists = track['artists']
        text = ""
        if len(artists) == 1:
            text = f"{artists[0]['name']} - {track['name']}"
        else:
            for artist in artists:
                text+=f"{artist['name']}, "
            text = text[:len(text)-1] + f" - {track['name']}"
        print(text)
        await self.__download_from_yt_url(f"https://www.youtube.com{YoutubeSearch(text, max_results=1).to_dict()[0]['url_suffix']}")
        
    async def download_from_vk_url(self, text):
        pass
        
    
    