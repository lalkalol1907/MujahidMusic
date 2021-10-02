import os
import pytube
import validators
from youtube_search import YoutubeSearch
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import vk_api
from vk_api.audio import VkAudio
from pymediainfo import MediaInfo
import pafy

class Song:
    def __init__(self, number, url, name, long, is_mp3, source):
        self.number = number
        self.url = url
        self.name = name
        self.long = long
        self.is_mp3 = is_mp3
        self.source = source

class Downloader():
    def __init__(self, queue, ctx, num):
        self.queue = queue
        self.ctx = ctx
        self.bot = num
    
    async def analyze(self, text, songs):
        if validators.url(text):
            if "spotify" in text: 
                return await self.__download_from_spotify_url(text, songs)
            elif "youtube" in text or "youtu.be" in text: 
                return await self.__download_from_yt_url(text, "youtube", songs)
        else: 
            return await self.__download_from_yt_url(f"https://www.youtube.com{YoutubeSearch(text, max_results=1).to_dict()[0]['url_suffix']}", "youtube", songs)
        
    async def __download_from_yt_url(self, url, source, songs):
        if self.bot < 10:
            ln = 1
        elif self.bot < 100:
            ln = 2
        elif self.bot < 1000:
            ln = 3
        else: ln = 4
        youtube = pytube.YouTube(url)
        mp3 = youtube.streams.filter(only_audio=True).first()
        mp3.download('./music')
        h, m, s = map(int, pafy.new(url).duration.split(":"))
        duration = h*3600 + m*60 + s
        for file in os.listdir("./music"):
            if file.endswith(".mp4"):  
                name = file
                if self.queue != -1:
                    try:
                        os.rename(f"./music/{file}", f"./music/queue/{self.bot}-song{self.queue+1}.mp3")
                        self.queue+=1
                    except FileExistsError:
                        for file1 in os.listdir("./music/queue"):
                            if file1.endswith(".mp3") and int(file1[0:ln]) == self.bot:
                                try:
                                    os.remove(f"./music/queue/{file1}")
                                except FileNotFoundError: pass
                                except PermissionError as ex: print(ex)
                        os.rename(f"./music/{file}", f"./music/queue/{self.bot}-song{self.queue+1}.mp3")
                        self.queue+=1         
                else:
                    try:
                        for file2 in os.listdir("./music/queue"):
                            try:
                                if "song" in file and int(file2[0:ln]) == self.bot:
                                    os.remove(f"./music/queue/{file2}")
                            except FileNotFoundError: pass
                        os.rename(f"./music/{file}", f"./music/queue/{self.bot}-song0.mp3")
                        self.queue = 0
                    except FileExistsError:
                        for file1 in os.listdir("./music/queue"):
                            if file1.endswith(".mp3") and int(file1[0:ln]) == self.bot:
                                try:
                                    os.remove(f"./music/queue/{file1}")
                                except FileNotFoundError: pass
                                except PermissionError as ex: print(ex)
                        os.rename(f"./music/{file}", f"./music/queue/{self.bot}-song0.mp3")
                        self.queue = 0
                songs.append(Song(self.queue, url, f"{name[:-4]}", duration, True, source))
                return songs
    
    async def __download_from_spotify_url(self, url, songs):
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
        return await self.__download_from_yt_url(f"https://www.youtube.com{YoutubeSearch(text, max_results=1).to_dict()[0]['url_suffix']}", "spotify", songs)
        
    async def vk(self, text):
        login, password = 'login', 'password'
        vk_session = vk_api.VkApi(login, password)
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        vkaudio = VkAudio(vk_session)
        tracks = vkaudio.search(text, count=1)
        for n, track in enumerate(tracks, 1):
            print('{}. {} {}'.format(n, track['title'], track['url']))

        return track['url']