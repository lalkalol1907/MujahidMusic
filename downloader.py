import pytube
import pytube.exceptions
import validators
from youtube_search import YoutubeSearch
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import vk_api
from vk_api.audio import VkAudio
import pafy
import http

class Song:
    def __init__(self, number, url, name, long, is_mp3, source, ctx, loop):
        self.number = number
        self.url = url
        self.name = name
        self.long = long
        self.is_mp3 = is_mp3
        self.source = source
        self.requestctx = ctx
        self.loop = loop

class Downloader():
    def __init__(self, queue, ctx, num, cs=0) -> None:
        self.queue = queue
        self.ctx = ctx
        self.bot = num
        self.current_song = cs
    
    async def analyze(self, text, songs, loop = 1, pos=0):
        if validators.url(text):
            if "spotify" in text: 
                return await self.__download_from_spotify_url(text, songs, int(pos), loop)
            elif "youtube" in text or "youtu.be" in text: 
                return await self.__download_from_yt_url(text, "youtube", songs, int(pos), loop)
        else:
            try: 
                return await self.__download_from_yt_url(f"https://www.youtube.com{YoutubeSearch(text, max_results=1).to_dict()[0]['url_suffix']}", "youtube", songs, int(pos), loop)
            except IndexError: 
                return songs, "empty"
            except:
                return songs, "age"
        
    async def __download_from_yt_url(self, url, source, songs, pos, loop = 1):
        try:
            youtube = pytube.YouTube(url)
        except: 
            return songs, "link"
        try: 
            f = youtube.streams.filter(only_audio=True).first()
        except http.client.IncompleteRead:
            try:  
                f = youtube.streams.filter(only_audio=True).first()
            except: 
                return songs, "link"
        except pytube.exceptions.AgeRestrictedError:
            return songs, "age"
        except: 
            return songs, "link"
        def a():
            counter = 0
            while counter < 10:
                try:
                    f.download(output_path="./music/queue", filename=f"{self.bot}-song{self.queue+1}.mp3", skip_existing=False)
                    return True
                except:
                    counter += 1
            return False
        stat = a()
        if not stat:
            return songs, "link"
        self.queue += 1
        try:
            h, m, s = map(int, pafy.new(url).duration.split(":"))
            duration = h*3600 + m*60 + s
        except:
            return songs, "link"
        if pos != 0:
            print(pos + self.current_song)
            try:
                songs.insert(self.current_song + pos, Song(self.queue, url, f"{pafy.new(url).title}", duration, True, source, self.ctx, loop))
                
            except Exception as ex:
                print(ex)
                #songs.append(Song(self.queue, url, f"{pafy.new(url).title}", duration, True, source, self.ctx, loop))
        else:
            songs.append(Song(self.queue, url, f"{pafy.new(url).title}", duration, True, source, self.ctx, loop))
        return songs, "ok"
    
    async def __download_from_spotify_url(self, url, songs, pos, loop = 1):
        session = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="6a3124a2b3df4275a177a80104f534d0", client_secret="86870ba523f2494c9705a5e9a1ac1f90"))
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
        return await self.__download_from_yt_url(f"https://www.youtube.com{YoutubeSearch(text, max_results=1).to_dict()[0]['url_suffix']}", "spotify", songs, pos, loop)
        
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