import discord
from discord.gateway import DiscordWebSocket
import pytube
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
import threading
import time
import pyglet

from downloader import songs, Downloader

client = discord.Client()
bot = commands.Bot(command_prefix='$')

queue = -1
isp = False
current_song = -1
ctx = None
lock = threading.Lock()
stop_thread = False
stop_voice = False

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
        
    def run(self):
        global isp, current_song
        while True:
            for file in os.listdir("./music/queue"):
                if (file.name[18:len(file.name)-4] != current_song) and (isp):
                    try:
                        os.remove(f"./music/queue{file}")
                    except:
                        time.sleep(180)
            time.sleep(180)
                    
                    
class kick_checker(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        global ctx
        while True:
            voice = get(bot.voice_clients, guild=ctx.guild)
            if voice and not voice.is_connected():
                self.__stopper()
            time.sleep(5)
            
    def __stopper(self):
        global queue, current_song, stop_voice
        global ctx, isp
        np = ""
        time.sleep(1)
        clear("./music/queue")
        queue = -1
        current_song = -1
        isp = False
           
            
class player(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        print("runned")
        global ctx, stop_thread, stop_voice
        voice = get(bot.voice_clients, guild=ctx.guild)
        global isp, queue, current_song
        #if lock.locked():
            #lock.release()
        current_dir = os.listdir("./music/queue")    
        for file in range(len(os.listdir("./music/queue"))):
            try:
                current_song += 1
                if current_song > queue:
                    current_song-=1; break
                voice.stop()
                voice.play(discord.FFmpegPCMAudio(f"./music/queue/song{current_song}.mp3"))
                print(current_song)
                for i in range(int(pyglet.media.load(f"./music/queue/song{current_song}.mp3").duration)+3):
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
                    time.sleep(1)
                print(len(current_dir), "______", len(os.listdir("./music/queue")))
                print(len(current_dir) != len(os.listdir("./music/queue")))
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
async def p(ctxx, text): # play
   # await ctx.send(arg)
    
    global queue, isp, np, ctx, thread
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
    print("Someone wants to play music let me get that ready for them...")
    voice = get(bot.voice_clients, guild=ctx.guild)
    dw = Downloader(queue)
    dw.analyze(text)
    queue = dw.queue            
    print(isp)
    if not isp:
        thread = player()
        print("isp changed")    
        isp = True
        try:
            thread.start()
        except RuntimeError:
            print("excepted")
            thread.join()
            thread = player()
            thread.start()
    
@bot.command(pass_context=False)    
async def leave(ctxx):
    global queue, current_song
    global ctx
    ctx = ctxx
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Я не подключен к каналу")
    clear("./music/queue")
    queue = -1
    current_song = -1
    
@bot.command(pass_context=False)    
async def stop(ctxx):
    global queue, current_song, stop_voice
    global ctx, isp
    ctx = ctxx
    stop_voice = True
    time.sleep(1)
    clear("./music/queue")
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
    global ctx, current_song
    ctx = ctxx
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        if isp:
            await ctx.send(f"{songs[current_song]}")
        else:
            await ctx.send("В данный момент ничего не играет")
    else:
        await ctx.send("Я не подключен к каналу")
    
bot.run('ODg3MzEwNDk0MjIwODQwOTkx.YUCSSw.eBXeRPhKIyhdF6_epRN6aTlAbZc')
cleaner3000().start()
kick_checker().start()