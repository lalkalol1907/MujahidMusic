import discord
import os
from discord.ext import commands
from discord.utils import get
import asyncio
from Discord.downloader import Song, Downloader
from Discord.embeds import Embeds
import math
import datetime
import validators
from pytube import Playlist
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SpotifyCFG
from DB.DB import UserDB

bot = commands.Bot(command_prefix='$')


class Bot:
    class TG:
        new_tg = False
        user_pic_url = ""
        
    def __init__(self, num, ctx):
        self.queue = -1
        self.isp = False
        self.current_song = -1
        self.ctx = ctx
        self.stop_thread = False
        self.stop_voice = False
        self.stop_voice_2 = False
        self.skip_param = False
        self.skip_size = 1
        self.ctime = 0
        self.kick_checker_bool = False
        self.allower = False
        self.cleaner_bool = False
        self.fscount = 0
        self.sss = 0
        self.already_played_mp3 = []
        self.songs = []
        self.idle_checker_bool = False
        self.last_channel = None

        self.current_song_loop = 0

        self.bot_number = num
        self.server = ctx.message.guild
        self.guild_id = ctx.message.guild.id
        asyncio.get_event_loop().create_task(self.activate_tg())
        
    async def __soprogs_start(self):
        if not self.kick_checker_bool:
            asyncio.get_event_loop().create_task(self.kick_checker())
            self.kick_checker_bool = True
            self.allower = True
        if not self.cleaner_bool:
            asyncio.get_event_loop().create_task(self.cleaner())
            self.cleaner_bool = True
        if not self.idle_checker_bool:
            asyncio.get_event_loop().create_task(self.idle_checker())
            self.idle_checker_bool = True
            
    async def __voice_connector(self, channel):
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        if voice and voice.is_connected():
            try:
                await voice.move_to(channel)
            except:
                await self.ctx.send("Can't connect")
        else:
            try:
                voice = await channel.connect()
                await self.ctx.send(f"Connected to `#{channel}`")
            except:
                try:
                    await voice.move_to(channel)
                except:
                    await self.ctx.send("Can't connect")

    def __log(self, arg=""):
        try:
            arg += f"\nqueue: {self.queue}\nisp: {self.isp}\ncursong: {self.current_song}\nsss: {self.sss}\nsongs: {self.songs[self.queue].name}\nbools: self.stop_thread: {self.stop_thread} self.stop_voice: {self.stop_voice} "
            print(f"{datetime.datetime.now()}\n{self.bot_number}-Bot: {arg}\n\n")
        except:
            arg += f"\nqueue: {self.queue}\nisp: {self.isp}\ncursong: {self.current_song}\nsss: {self.sss}\nbools: self.stop_thread: {self.stop_thread} self.stop_voice: {self.stop_voice} "
            print(f"{datetime.datetime.now()}\n{self.bot_number}-Bot: {arg}\n\n")

    async def fs(self, ctx):
        self.__log("Skipped")
        self.ctx = ctx
        if self.isp:
            self.stop_thread = True
            self.fscount += 1
        else:
            await self.ctx.send("There's nothing to skip")

    async def connect(self, ctx):
        self.ctx = ctx
        try:
            channel = self.ctx.message.author.voice.channel
        except AttributeError:
            await self.ctx.send("You are not connected to any channel, connecting to default channel")
            return
        self.__log(f"Connected channel = {channel}")
        await self.__voice_connector(channel)
        
    async def channel(self, ctx, ch):
        self.ctx = ctx
        await self.__voice_connector(ch)

    async def p(self, ctx, text):  # play
        self.ctx = ctx
        def __packcheck():
            arr = text.split()
            url_flag = True
            flag2 = ';' in text
            try:
                c = int(arr[0])
            except:
                return False
            for i in range(1, len(arr)):
                url_flag = validators.url(arr[i])
                if not url_flag:
                    break
            return flag2 or url_flag

        if __packcheck():
            await self.pack(ctx, text)
            return

        if 'playlist' in text and validators.url(text):
            asyncio.get_event_loop().create_task(self.__playlist(ctx, text))
            return
        try:
            channel = self.ctx.message.author.voice.channel
        except AttributeError:
            await self.ctx.send("You're not connected to any channel!")
            return
        self.__log(f"Bot: p: channel = {channel}")
        await self.__voice_connector(channel)
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        await self.ctx.send(f"Searching and downloading: `{text}`...")
        dw = Downloader(self.queue, self.ctx, self.bot_number)
        stat = await dw.analyze(text)
        if stat == "ok":
            if self.isp:
                song = self.songs[self.queue]
                await self.ctx.send(
                    embed=Embeds().added_to_queue(song.name, song.url, int(song.long), self.ctx, self.queue,
                                                  self.current_song))
                self.__log(f"song {song.name} added to queue, {song.url}")
                pass
            else:
                self.isp = True
                asyncio.get_event_loop().create_task(self.MusicPlayer(voice, self.sss))
            await self.__soprogs_start()
        elif stat == "empty":
            await ctx.send("No results for your query((")
        elif stat == "link":
            await ctx.send("There's an error. Your link is incorrect. May be this video is age restricted")
        elif stat == "age":
            await ctx.send("This video is age restricted, try to use link/another link")

    async def play_loop(self, ctx, input_str):
        self.ctx = ctx
        try:
            c = int(input_str.split(' ')[0])
            if c == 1:
                temp = 1
            else:
                temp = math.floor(math.log10(c))
            text = input_str[temp + 2:]
            if text[0] == ' ':
                text = text[1:]
        except Exception as ex:
            splitted = input_str.split()
            try:
                c = int(splitted[len(splitted)-1])
                if c == 1: 
                    temp = 1
                else: 
                    temp = math.floor(math.log10(c))
                text = input_str[temp + 2:]
                if text[0] == ' ':
                    text = text[1:]
            except:
                print(ex)
                await ctx.send('Type "$pl <loop counter>; <name or url>"')
                return
            
        if 'playlist' in text and validators.url(text):
            await ctx.send("Can't playing playlists in a loop")
            return
        try:
            channel = self.ctx.message.author.voice.channel
        except AttributeError:
            await self.ctx.send("You're not connected to any channel!")
            return
        self.__log(f"Bot: p: channel = {channel}")
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        await self.__voice_connector(channel)
        await self.ctx.send(f"Searching and downloading: `{text}`...")
        dw = Downloader(self.queue, self.ctx, self.bot_number)
        stat = await dw.analyze(text, loop=c)
        if stat == "ok":
            if self.isp:
                song = self.songs[self.queue]
                await self.ctx.send(
                    embed=Embeds().added_to_queue(song.name, song.url, int(song.long), self.ctx, self.queue,
                                                  self.current_song, song.loop))
                self.__log(f"song {song.name} added to queue, {song.url}")
                pass
            else:
                self.isp = True
                asyncio.get_event_loop().create_task(self.MusicPlayer(voice, self.sss))
            await self.__soprogs_start()
        elif stat == "empty":
            await ctx.send("No results for your querry((")
        elif stat == "link":
            await ctx.send("There's an error. Your link is incorrect. May be this video is age restricted")
        elif stat == "age":
            await ctx.send("This video is age restricted, try to use link/another link")

    async def play_in_pos(self, ctx, input_str, send_key=True):
        self.ctx = ctx

        def splitter():
            c = int(input_str.split(' ')[0])
            if c == 1:
                temp = 1
            else:
                temp = math.floor(math.log10(c))
            t = input_str[temp + 1:]
            while t[0] == ' ':
                t = t[1:]
            return c, t

        pos, text = splitter()
        if pos > len(self.songs):
            await self.ctx.send("Yours track position is bigger than songs list. Adding to the end of the queue.")
            await self.p(ctx, text)
            return
        try:
            channel = self.ctx.message.author.voice.channel
        except AttributeError:
            await self.ctx.send("You're not connected to any channel!")
            return
        self.__log(f"Bot: p: channel = {channel}")
        await self.__voice_connector(channel)
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        if send_key:
            await self.ctx.send(f"Searching and downloading: `{text}`...")
        else:
            await self.ctx.send(f"Searching and playing now, please wait: `{text}`...")
        dw = Downloader(self.queue, self.ctx, self.bot_number, self.sss)
        stat = await dw.analyze(text, pos=pos)
        if stat == "ok":
            if self.isp:
                song = self.songs[self.sss + pos]
                if send_key:
                    await self.ctx.send(
                        embed=Embeds().added_to_queue(song.name, song.url, int(song.long), self.ctx, self.sss + pos,
                                                      self.current_song))
                self.__log(f"song {song.name} added to queue, {song.url}")
                pass
            else:
                self.isp = True
                asyncio.get_event_loop().create_task(self.MusicPlayer(voice, self.sss))
            await self.__soprogs_start()
        elif stat == "empty":
            await ctx.send("No results for your querry((")
        elif stat == "link":
            await ctx.send("There's an error. Your link is incorrect. May be this video is age restricted")
        elif stat == "age":
            await ctx.send("This video is age restricted, try to use link/another link")

    async def play_now(self, ctx, input_str):
        self.ctx = ctx
        try:
            voice = get(bot.voice_clients, guild=self.ctx.guild)
            voice.pause()
        except:
            await self.p(ctx, input_str)
            return
        await self.play_in_pos(ctx, f"1 {input_str}", False)
        await self.fs(ctx)
        voice.resume()

    async def __playlist(self, ctx, text):
        self.ctx = ctx
        splitter = lambda txt: txt.split()
        full = False
        tracks = 15
        if len(splitter(text)) != 1:
            text, tracks = splitter(text)
            try:
                tracks = int(tracks)
            except:
                tracks, text = splitter(text)
                try:
                    tracks = int(tracks)
                except:
                    if '-f' in text:
                        full = True
        try:
            channel = self.ctx.message.author.voice.channel
        except AttributeError:
            await self.ctx.send("You're not connected to any channel!")
            return
        self.__log(f"Bot: p: channel = {channel}")
        await self.__voice_connector(channel)
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        urls = []
        if 'youtube' in text or 'youtu.be' in text:
            playlist = Playlist(text)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            urls = playlist.video_urls
        elif "spotify" in text:
            session = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=SpotifyCFG().CLIENT_ID,
            client_secret=SpotifyCFG().CLIENT_SECRET))
            pl = session.playlist(text)
            for track in pl['tracks']['items']:
                urls.append(track['track']['external_urls']['spotify'])
        else:
            await self.ctx.send("Error, neither spotify nor yt source!")
            return
        sq = self.queue
        await self.__soprogs_start()
        added_songs = []
        i = 0
        for url in urls:
            if tracks and i >= tracks and not full: break
            if validators.url(url):
                dw = Downloader(self.queue, self.ctx, self.bot_number)
                stat = await dw.analyze(url)
                print(self.queue)
                if stat == "ok":
                    added_songs.append(self.songs[self.queue])
                    if not self.isp:
                        self.isp = True
                        print(self.isp)
                        asyncio.get_event_loop().create_task(self.MusicPlayer(voice, self.sss))
                    await asyncio.sleep(2)
                elif stat == "empty":
                    await ctx.send("No results for your querry((")
                elif stat == "link":
                    await ctx.send("There's an error. Try another querry")
                elif stat == "age":
                       await ctx.send("One of those videos is age restricted, can't download")
            i+=1
            if added_songs:
                await self.ctx.send(embed=Embeds().added_to_queue_pack(self.ctx, added_songs, url))
            else:
                await self.ctx.send("Error while adding playlist")
                
    async def pack(self, ctx, text):
        self.ctx = ctx
        urls = text.split()
        try:
            channel = self.ctx.message.author.voice.channel
        except AttributeError:
            await self.ctx.send("You're not connected to any channel!")
            return
        self.__log(f"Bot: p: channel = {channel}")
        await self.__voice_connector(channel)
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        await self.ctx.send(f"Adding to queue your pack...")
        await self.__soprogs_start()
        added_songs = []
        for url in urls:
            if validators.url(url):
                dw = Downloader(self.queue, self.ctx, self.bot_number)
                stat = await dw.analyze(url)
                if stat == "ok":
                    added_songs.append(self.songs[self.queue])
                    if not self.isp:
                        self.isp = True
                        asyncio.get_event_loop().create_task(self.MusicPlayer(voice, self.sss))
                    await asyncio.sleep(2)
                elif stat == "empty":
                    await ctx.send("No results for your querry((")
                elif stat == "link":
                    await ctx.send("There's an error. Try another querry")
                elif stat == "age":
                    await ctx.send("One of those videos is age restricted, can't download")
            else:
                await self.ctx.send("This function can play only urls")
        if added_songs:
            await self.ctx.send(embed=Embeds().added_to_queue_pack(self.ctx, added_songs))
        else:
            await self.ctx.send("Error while adding pack")

    async def vk(self, ctxx, text):
        self.ctx = ctxx
        await self.ctx.send("In development =)")
        return
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await self.ctx.send(f"Connected to `#{channel}`")
        voice.play(discord.FFmpegOpusAudio(
            "https://cs1-82v4.vkuseraudio.net/p24/2d8c304bd0442e.mp3?extra=cfihgRks4dKdRugxjILr-nIzgJowmNzJGLcTRVpAcLVluOiQGm7y8qvaG7OVyFiSM1P8TDfzOgmzsztIeHjvtqMT5APOHu_SWQOKYUpy6bm5FCqGjgK7gVFTsdrcF1BHGMjTyVe_MhVpTdFe336phVNUvw&long_chunk=1"))

    async def leave(self, ctxx):
        self.__log("leave")
        self.ctx = ctxx
        self.stop_voice = True
        self.queue, self.current_song, self.isp, self.sss = -1, -1, False, 0
        channel = self.ctx.message.author.voice.channel
        await asyncio.sleep(1)
        await self.clear("./music/queue")
        self.stop_voice = False
        self.songs.clear()
        self.already_played_mp3.clear()
        self.current_song_loop = 0
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        try:
            if voice and voice.is_connected():
                await voice.disconnect()
                await self.ctx.send(f"Left `{channel}`")
            else:
                await self.ctx.send("Not connected to the channel")
        except AttributeError:
            await self.ctx.send("I'm not connected")

    async def stop(self, ctxx):
        self.__log("stop")
        self.ctx = ctxx
        self.stop_voice = True
        await asyncio.sleep(1)
        await self.clear("./music/queue")
        self.queue, self.current_song, self.isp, self.sss = -1, -1, False, 0
        self.stop_voice = False
        self.songs.clear()
        self.already_played_mp3.clear()
        self.current_song_loop = 0

    async def pause(self, ctxx):
        self.__log("pause")
        self.ctx = ctxx
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
            else:
                voice.pause()
        except AttributeError:
            await self.ctx.send("I'm not connected")

    async def resume(self, ctxx):
        self.__log("resume")
        self.ctx = ctxx
        try:
            voice = get(bot.voice_clients, guild=self.ctx.guild)
            voice.resume()
        except AttributeError:
            await self.ctx.send("I'm not connected")

    async def np(self, ctxx):
        self.__log("now playing")
        self.ctx = ctxx
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        try:
            if voice.is_connected():
                if self.isp:
                    song = self.songs[self.current_song]
                    await self.ctx.send(
                        embed=Embeds().NPEmbed(title=song.name, url=song.url, time1=self.ctime, time2=song.long,
                                               ctx=self.ctx, loop=song.loop, curloop=self.current_song_loop))
                else:
                    await self.ctx.send("Nothing is playing now")
            else:
                await self.ctx.send("Not connected to the channel")
        except AttributeError:
            await self.ctx.send("I'm not connected")

    async def queue1(self, ctxx):
        self.__log("queue")
        self.ctx = ctxx
        if self.queue == -1:
            await self.ctx.send("There is nothing to play!")
        elif not self.isp:
            await self.ctx.send("Nothing is playing now!")
        else:
            await self.ctx.send(
                embed=Embeds().queue(self.songs, self.current_song, self.ctx, self.ctime, self.current_song_loop))

    async def clear(self, path):
        if os.listdir(path):
            try:
                for file in os.listdir(path):
                    if self.bot_number > 0:
                        ln = math.ceil(math.log10(self.bot_number))
                    else:
                        ln = 1
                    if file.endswith(".mp3") and int(file[0:ln]) == self.bot_number:
                        os.remove(f"{path}/{file}")
            except:
                pass

    async def cleaner(self):
        already_deleted = []
        while True:
            if self.current_song > 0:
                for i in self.already_played_mp3:
                    if i not in already_deleted and i != self.current_song:
                        try:
                            os.remove(f"./music/queue/{self.bot_number}-song{i}.mp3")
                            already_deleted.append(i)
                            self.__log("cleaner try")
                        except Exception as ex:
                            print(f"Can't delete, exception {ex}")
                            if f"{self.bot_number}-song" in str(ex):
                                already_deleted.append(i)
                            self.__log("cleaner except")
            await asyncio.sleep(30)
            
    async def author(self, ctx, text):
        def splitter(t):
            splitted = t.split()
            if len(splitted) == 1:
                return 5, t
            try:
                quota = int(splitted[0])
                t = t.replace(f"{quota}", " ")
                while t[0] == ' ': 
                    t = t[1:]
                return quota, t
            except:
                return 5, t
        # TODO: Создать эту функцию
        count, text = splitter(text)
        
    async def MusicPlayer(self, voice, s=0):
        self.stop_voice_2 = False
        self.__log()
        iter = 0
        self.current_song_loop = 0
        for ss in range(s, len(self.songs)):
            self.sss = ss
            try:
                self.current_song = ss
                if self.current_song > self.queue:
                    self.current_song -= 1
                    break
                voice.stop()
                try:
                    song = self.songs[ss]
                except IndexError:
                    await self.ctx.send("Error with queue, restarting")
                    self.last_channel = voice
                    await self.leave(self.ctx)
                    await self.channel(self.ctx, self.last_channel)
                EmbedSent = False
                for j in range(int(song.loop)):
                    print("songloop", song.loop)
                    if song.is_mp3:
                        dur = song.long
                        data = discord.FFmpegPCMAudio(source=f"./music/queue/{self.bot_number}-song{song.number}.mp3")
                        voice.play(data)
                        self.current_song_loop += 1
                        self.__log(f"{self.bot_number} playing {song.name}")
                        self.already_played_mp3.append(ss)
                    else:
                        pass
                    self.__log(f"iter = \n{iter}")
                    if song.loop == 1:
                        if song.source != "tg":
                            await song.requestctx.send(
                                embed=Embeds().playing(song.name, song.url, int(dur), song.requestctx))
                        else:
                            await self.ctx.send(embed=Embeds().TG_playing(song.name, int(dur), song.TGAva))
                    elif not EmbedSent:
                        await song.requestctx.send(
                            embed=Embeds().playing(song.name, song.url, int(dur), song.requestctx, song.loop))
                        EmbedSent = True
                    self.ctime = 0
                    for i in range(int(dur)):
                        try:
                            if self.stop_thread is True:
                                voice.stop()
                                self.stop_thread = False
                                ss += 1
                                await self.MusicPlayer(voice, ss)
                                self.isp = False
                                return
                            if self.stop_voice is True:
                                voice.stop()
                                self.stop_voice = False
                                self.stop_voice_2 = True
                                break
                            if self.skip_param is True:
                                voice.stop()
                                self.skip_param = False
                                ss += self.skip_size
                                await self.MusicPlayer(voice, ss)
                                self.isp = False
                                return
                        finally:
                            pass
                        self.ctime += 1
                        await asyncio.sleep(1)
                    await asyncio.sleep(1)
                if self.stop_voice_2:
                    self.stop_voice_2 = False
                    self.isp = False
                    self.sss = ss
                    return
                if self.current_song <= self.queue:
                    ss += 1
                    await self.MusicPlayer(voice, ss)
                    self.isp = False
                    return
            except Exception as ex:
                print(ex)
        else:
            self.sss = s
            self.isp = False
            return
        self.isp = False
        return

    async def delete(self, ctx, text):
        pass

    async def skip_parameters(self, ctx, param):
        self.ctx = ctx
        if self.isp:
            try:
                self.skip_param, self.skip_size = True, int(param)
                self.fscount += int(param)
            except ValueError:
                await ctx.send("Incorrect querry, please type an integer")
        else:
            await self.ctx.send("There's nothing to skip")

    async def kick_checker(self):
        while True:
            voice = get(bot.voice_clients, guild=self.ctx.guild)
            if not voice and self.allower:
                self.queue, self.current_song, self.isp, self.sss = -1, -1, False, 0
                await asyncio.sleep(1)
                await self.clear("./music/queue")
                self.songs.clear()
                self.already_played_mp3.clear()
                self.allower = True
                self.current_song_loop = 0
            await asyncio.sleep(1)

    async def idle_checker(self):
        counter = 0
        while True:
            voice = get(bot.voice_clients, guild=self.ctx.guild)
            if self.isp:
                counter = 0
            elif counter < 100:
                counter += 1
            else:
                if voice and voice.is_connected():
                    await voice.disconnect()
                    await self.ctx.send(f"Disconnected due to inactivity")
                counter = 0
            await asyncio.sleep(3)
        
    async def activate_tg(self):
        while True:
            if not self.TG.new_tg:
                await asyncio.sleep(2)
                continue
            def find_song():
                for i in range(len(self.songs) - 1, -1, -1):
                    if self.songs[i].source == 'tg':
                        return i
            print('aboba')
            try:
                song = self.songs[find_song()]
                if self.isp:
                    await self.ctx.send(embed=Embeds().added_tg(song.name, song.long, self.queue, self.current_song, self.TG.user_pic_url))
                    self.TG.new_tg = False
                else:
                    self.TG.new_tg = False
                    voice = get(bot.voice_clients, guild=self.ctx.guild)
                    if voice and voice.is_connected():
                        self.isp = True
                        await self.__soprogs_start()
                        asyncio.get_event_loop().create_task(self.MusicPlayer(voice, self.sss))
                    else:
                        await self.ctx.send("To play TG song type $connect in discord and send audio again!")
            except TypeError:
                self.TG.new_tg = False
            await asyncio.sleep(2)