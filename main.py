import discord
from discord.gateway import DiscordWebSocket
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
import threading
import time
import pyglet
import asyncio

from downloader import *
from embeds import Embeds

client = discord.Client()
bot = commands.Bot(command_prefix='$')

queue = -1
isp = False
current_song = -1
ctx = None
lock = threading.Lock()
stop_thread = False
stop_voice = False
ctime = 0

kick_checker_bool = False
    
def clear(path):
    if [] != os.listdir(path):
            try:
                for file in os.listdir(path):
                    if file.endswith(".mp3"):
                        os.remove(f"{path}/{file}")
            except:
                pass

class cleaner3000(threading.Thread):
    def __init__(self):
        super().__init__()
        self.already_deleted = []
        
    def run(self):
        global isp, current_song
        print("cleaner started")
        while True:
            if current_song > 0:
                for i in range(current_song-1):
                    if i not in self.already_deleted:
                        try:
                            os.remove(f"./music/queue/song{i}.mp3")
                            self.already_deleted.append(i)
                        except Exception as ex:
                            print(f"Can't delete, exception {ex}")
            time.sleep(180)
                    
                    
class kick_checker(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        print("kickchecker started")
        global ctx
        while True:
            
            voice = get(bot.voice_clients, guild=ctx.guild)
            if voice and not voice.is_connected():
                self.__stopper()
            time.sleep(5)
            
    def __stopper(self):
        global queue, current_song, stop_voice, urls, names, numbers, long
        global ctx, isp
        urls, names, numbers, long = [], [], [], []
        time.sleep(1)
        clear("./music/queue")
        queue = -1
        current_song = -1
        isp = False
           
async def sender():
    global names, current_song, ctx
    while True:
        if ctx:
            await ctx.send(f"aaa")
           # await ctx.send(f"`{names[current_song]}` играет сейчас!")
        await asyncio.sleep(2)
            
class player(threading.Thread):
    def __init__(self, voice):
        super().__init__()
        self.voice = voice
        
    def run(self):
        print("runned")
        global ctx, stop_thread, stop_voice, ctime
        global isp, queue, current_song
        voice = self.voice
        #if lock.locked():
            #lock.release() 
        for file in range(len(os.listdir("./music/queue"))):
            try:
                current_song += 1
                if current_song > queue:
                    current_song-=1; break
                voice.stop()
                #os.rename("")
                dur = pyglet.media.load(f"./music/queue/song{current_song}.mp3").duration
                long.append(dur)
                voice.play(discord.FFmpegPCMAudio(f"./music/queue/song{current_song}.mp3"))
                ctime = 0
                for i in range(int(dur)+3):
                    #lock.acquire()
                    try:
                        if stop_thread is True:
                            voice.stop()
                            stop_thread = False
                            print("stopped")
                            self.run()
                            break
                        if stop_voice is True:
                            voice.stop()
                            stop_voice = False
                            break
                    finally:
                        pass
                        #lock.release()
                    ctime += 1
                    time.sleep(1)
                if current_song <= queue:
                    self.run()
            except Exception as ex:
                print(ex) 
        isp = False


@bot.command(pass_context=False)
async def fs(ctxx):
    global ctx
    ctx = ctxx
    global current_song, stop_thread
    stop_thread = True


@bot.command(pass_context=True)
async def p(ctxx, *, text): # play
   # await ctx.send(arg)
    global queue, isp, np, ctx, thread, kick_checker_bool
    ctx = ctxx
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Я не подключен к каналу")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f"Подключен к #{channel}")
    dw = Downloader(queue, ctx)
    th = threading.Thread(target=dw.analyze(text))
    th.start()
    while th.is_alive():
        time.sleep(1)
    queue = dw.queue            
    if isp:
        """
        Отправка виджета
        """
        pass
    else:
        pass
        
    if not kick_checker_bool:
        kick_checker().start()
        kick_checker_bool = True    
    if not isp:
        thread = player(voice)
        #print("isp changed")    
        isp = True
        try:
            thread.start()
        except RuntimeError:
            #print("excepted")
            thread.join()
            thread = player(voice)
            thread.start()
            
    
@bot.command(pass_context=False)    
async def leave(ctxx):
    global queue, current_song, stop_voice, urls, names, numbers, long
    global ctx, isp
    ctx = ctxx
    stop_voice = True
    time.sleep(1)
    clear("./music/queue")
    queue = -1
    current_song = -1
    urls, names, numbers, long = [], [], [], []
    isp = False
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Покинул канал: {channel}")
    else:
        await ctx.send("Я не подключен к каналу")
    
@bot.command(pass_context=False)    
async def stop(ctxx):
    global queue, current_song, stop_voice, urls, names, numbers, long
    global ctx, isp
    ctx = ctxx
    stop_voice = True
    time.sleep(1)
    clear("./music/queue")
    urls, names, numbers, long = [], [], [], []
    queue = -1
    current_song = -1
    isp = False
    
@bot.command(pass_context=False)
async def pause(ctxx):
    ctx = ctxx
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        voice.pause()
        
@bot.command(pass_context=False)
async def resume(ctxx):
    ctx = ctxx
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.resume()
    
@bot.command(pass_context=False)
async def np(ctxx):
    global ctx, current_song, ctime, long, names
    ctx = ctxx
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        if isp:
            await ctx.send(embed=Embeds().NPEmbed(title=names[current_song], url=urls[current_song], time1 = ctime, time2 = long[current_song],  ctx = ctxx))
        else:
            await ctx.send("В данный момент ничего не играет")
    else:
        await ctx.send("Я не подключен к каналу")


cleaner3000().start()
bot.run('ODg3MzEwNDk0MjIwODQwOTkx.YUCSSw.eBXeRPhKIyhdF6_epRN6aTlAbZc')
