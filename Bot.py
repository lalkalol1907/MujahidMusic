import discord
import os
from discord.ext import commands
from discord.utils import get
import asyncio
from downloader import *
from embeds import Embeds
import math

bot = commands.Bot(command_prefix='$')   

class Bot:
    def __init__(self, num, ctx):
        self.queue = -1
        self.isp = False
        self.current_song = -1
        self.ctx = ctx
        self.stop_thread = False
        self.stop_voice = False
        self.ctime = 0
        self.kick_checker_bool = False
        self.allower = False    
        self.cleaner_bool = False
        self.idle_bool = False
        self.fscount = 0
        self.sss = 0
        self.already_played_mp3 = []
        self.songs = []
        
        self.bot_number = num
        self.server = ctx.message.guild  
    
    async def fs(self, ctx):
        self.ctx = ctx
        if self.isp:
            self.stop_thread = True
            self.fscount += 1
        else:
            await self.ctx.send("There's nothing to skip")
        
    async def p(self, ctx, text): # play
        self.ctx = ctx
        channel = self.ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            try:
                voice = await channel.connect()
                await self.ctx.send(f"Connected to `#{channel}`")
            except:
                await voice.move_to(channel)
        dw = Downloader(self.queue, self.ctx, self.bot_number, self.ctx)
        self.songs, stat = await dw.analyze(text, self.songs)
        if stat == "ok":
            self.queue = dw.queue        
            if self.isp:
                song = self.songs[self.queue]
                await self.ctx.send(embed=Embeds().added_to_queue(song.name, song.url, int(song.long), self.ctx, self.queue, self.current_song))
                print(f"song {song.name} added to queue, {song.url}")
                pass
            if not self.kick_checker_bool:
                asyncio.get_event_loop().create_task(self.kick_checker())
                self.kick_checker_bool = True
                self.allower = True    
            if not self.isp:   
                self.isp = True
                asyncio.get_event_loop().create_task(self.MusicPlayer(voice, self.sss))
            if not self.cleaner_bool:
                asyncio.get_event_loop().create_task(self.cleaner())
                self.cleaner_bool = True
            if not self.idle_bool:
                asyncio.get_event_loop().create_task(self.idle_checker())
                self.idle_bool = True
        elif stat == "empty":
            await ctx.send("No results for your querry((")
        elif stat == "link":
            await ctx.send("There's an error. Your link is incorrect")
            
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
        
        voice.play(discord.FFmpegOpusAudio("https://cs1-82v4.vkuseraudio.net/p24/2d8c304bd0442e.mp3?extra=cfihgRks4dKdRugxjILr-nIzgJowmNzJGLcTRVpAcLVluOiQGm7y8qvaG7OVyFiSM1P8TDfzOgmzsztIeHjvtqMT5APOHu_SWQOKYUpy6bm5FCqGjgK7gVFTsdrcF1BHGMjTyVe_MhVpTdFe336phVNUvw&long_chunk=1"))
            
    async def leave(self, ctxx):
        self.ctx = ctxx
        self.stop_voice = True
        self.queue, self.current_song, self.isp, self.sss = -1, -1, False, 0
        channel = self.ctx.message.author.voice.channel
        await asyncio.sleep(1)
        await self.clear("./music/queue")
        self.stop_voice = False
        self.songs.clear()
        self.already_played_mp3.clear()
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
        self.ctx = ctxx
        self.stop_voice = True
        await asyncio.sleep(1)
        await self.clear("./music/queue")
        self.queue, self.current_song, self.isp, self.sss = -1, -1, False, 0
        self.stop_voice = False
        self.songs.clear()
        self.already_played_mp3.clear()
    
    async def pause(self, ctxx):
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
        self.ctx = ctxx
        try:
            voice = get(bot.voice_clients, guild=self.ctx.guild)
            voice.resume()
        except AttributeError:
            await self.ctx.send("I'm not connected")
    
    async def np(self, ctxx):
        self.ctx = ctxx
        voice = get(bot.voice_clients, guild=self.ctx.guild)
        try:
            if voice.is_connected():
                if self.isp: 
                    song = self.songs[self.current_song]
                    await self.ctx.send(embed=Embeds().NPEmbed(title=song.name, url=song.url, time1 = self.ctime, time2 = song.long,  ctx = self.ctx))
                else: 
                    await self.ctx.send("Nothing is playing now")
            else: 
                await self.ctx.send("Not connected to the channel")
        except AttributeError:
            await self.ctx.send("I'm not connected")
             
    async def loop(self, ctxx, text):
        self.ctx = ctxx
        await ctxx.send("`This function is being developed now`")
    
    async def queue1(self, ctxx):
        self.ctx = ctxx
        if self.queue == -1:
            await self.ctx.send("There is nothing to play!")
        elif not self.isp:
            await self.ctx.send("Nothing is playing now!")
        else: 
            await self.ctx.send(embed = Embeds().queue(self.songs, self.current_song, self.queue, self.ctx, self.ctime))
            
    async def clear(self, path):
        if [] != os.listdir(path):
                try:
                    for file in os.listdir(path):
                        if file.endswith(".mp3") and int(file[0:math.ceil(math.log10(self.bot_number))]) == self.bot_number:
                            os.remove(f"{path}/{file}")
                except: pass
                
    async def cleaner(self):
        already_deleted = []
        print("cleaner started")
        while True:
            if self.current_song > 0:
                for i in self.already_played_mp3:
                    if i not in already_deleted and i != self.current_song:
                        try:
                            os.remove(f"./music/queue/{self.bot_number}-song{i}.mp3")
                            already_deleted.append(i)
                        except Exception as ex:
                            print(f"Can't delete, exception {ex}")
                            if f"{self.bot_number}-song" in str(ex):
                                already_deleted.append(i)
            await asyncio.sleep(30)  
     
    async def MusicPlayer(self, voice, s = 0):
        self.stop_voice_2 = False
        print(len(self.songs))
        for ss in range(s, len(self.songs)): 
            self.sss = ss
            try:
                self.current_song += 1
                if self.current_song > self.queue:
                    self.current_song-=1; break
                voice.stop()
                song = self.songs[ss]
                if song.is_mp3:
                    dur = song.long
                    try:
                        voice.play(discord.FFmpegPCMAudio(f"./music/queue/{self.bot_number}-song{ss}.mp3"))
                    except:
                        await song.requestctx.send("Sorry, I have an error while playing :(")
                        ss+=1
                        await self.MusicPlayer(voice, ss)
                        self.isp = False
                        return
                    print(f"{self.bot_number} playing {song.name}")
                    self.already_played_mp3.append(ss)
                else:
                    pass
                await song.requestctx.send(embed=Embeds().playing(song.name, song.url, int(dur), song.requestctx))
                self.ctime = 0
                print(dur)
                for i in range(int(dur)):
                    try:
                        if self.stop_thread is True:
                            voice.stop()
                            self.stop_thread = False
                            ss+=1
                            print(f"{self.bot_number} force skipped song {song.name}")
                            await self.MusicPlayer(voice, ss)
                            self.isp = False
                            return
                        if self.stop_voice is True:
                            voice.stop()
                            self.stop_voice = False
                            self.stop_voice_2 = True
                            break
                    finally:
                        pass
                    self.ctime += 1
                    await asyncio.sleep(1)
                if self.stop_voice_2:
                    self.stop_voice_2 = False
                    self.isp = False
                    self.sss = ss
                    return
                if self.current_song <= self.queue:
                    ss+=1
                    print("rec2")
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
        
    async def kick_checker(self):
        print("kickchecker started")
        while True:
            voice = get(bot.voice_clients, guild=self.ctx.guild)
            if not voice and self.allower:
                self.queue, self.current_song, self.isp, self.sss = -1, -1, False, 0
                await asyncio.sleep(1)
                await self.clear("./music/queue")
                self.songs.clear()
                self.already_played_mp3.clear()
                self.allower = True
            await asyncio.sleep(2)
            
    async def idle_checker(self):
        counter = 0
        while True:
            if self.isp: 
                counter = 0
            elif counter >= 120:
                counter+=1
                asyncio.sleep(1)
            else:
                voice = get(bot.voice_clients, guild=self.ctx.guild)
                if voice:
                    if voice.is_connected():
                        voice.disconnect()
                        await self.ctx.send("Disconnected due to inactivity")