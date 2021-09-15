import discord
import pytube
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
import threading
import time
import pyglet


client = discord.Client()
bot = commands.Bot(command_prefix='$')

np = ""
queue = -1
isp = False
current_song = -1
ctx = None
lock = threading.Lock()
stop_thread = False

def clear(path):
    if [] != os.listdir(path):
            try:
                for file in os.listdir(path):
                    if file.endswith(".mp3"):
                        os.remove(f"{path}/{file}")
            except:
                pass

class player(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        print("runned")
        global ctx, stop_thread
        voice = get(bot.voice_clients, guild=ctx.guild)
        global isp, queue, current_song
        if lock.locked():
            lock.release()
        
        current_dir = os.listdir("./music/queue")    
        for file in range(len(os.listdir("./music/queue"))):
            try:
                current_song += 1
                if current_song >= len(os.listdir("./music/queue")):
                    current_song-=1; break
                voice.play(discord.FFmpegPCMAudio(f"./music/queue/song{current_song}.mp3"))
                print(current_song)
                #if current_song != 0:
                    #try:
                        #os.rename(f"./music/queue/song{current_song-1}.mp3", f"./music/played/song{current_song-1}.mp3")
                    #except FileExistsError:
                        #clear(f"./music/played")
                        #os.rename(f"./music/queue/song{current_song-1}.mp3", f"./music/played/song{current_song-1}.mp3")
                for i in range(int(pyglet.media.load(f"./music/queue/song{current_song}.mp3").duration)+1):
                    lock.acquire()
                    try:
                        if stop_thread is True:
                            voice.stop()
                            stop_thread = False
                            print("stopped")
                            self.run()
                            break
                    finally:
                        lock.release()
                    time.sleep(1)
                print(len(current_dir), "______", len(os.listdir("./music/queue")))
                print(len(current_dir) != len(os.listdir("./music/queue")))
                if len(current_dir) != len(os.listdir("./music/queue")):
                    
                    #os.rename(f"./music/queue/song{current_song}.mp3", f"./music/played/song{current_song}.mp3")
                    self.run()
                #else:
                    #try:
                        #os.rename(f"./music/queue/song{current_song}.mp3", f"./music/played/song{current_song}.mp3")
                    #except FileNotFoundError:
                        #print("already deleted")
                    
            except Exception as ex:
                print(ex) 
        isp = False
        """for file in os.listdir("./music/queue"):
            try:
                os.rename(f"./music/queue/song{current_song}.mp3", f"./music/played/song{current_song}.mp3")
            except FileNotFoundError:
                print("already deleted")
            except FileExistsError:
                clear(f"./music/played")
                os.rename(f"./music/queue/song{current_song-1}.mp3", f"./music/played/song{current_song-1}.mp3")"""

class checker(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        global ctx
        voice = get(bot.voice_clients, guild=ctx.guild)
        while True:
            time.sleep(120)
            if not voice.playing() and not voice.paused():
                self.deleter()
                
    def deleter(self):
        if [] != os.listdir("./music/played"):
            try:
                for file in os.listdir("./music/played"):
                    if file.endswith(".mp3"):
                        os.remove(f"./music/played/{file}")
            except:
                pass
            
checker_thread = checker()        

@bot.command(pass_context=False)
async def fs(ctxx):
    global ctx
    ctx = ctxx
    global current_song, stop_thread
    stop_thread = True

@bot.command(pass_context=True)
async def p(ctxx, url): # play
   # await ctx.send(arg)
    
    global queue, isp, np, ctx, thread
    ctx = ctxx
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Пидорас, подключись")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Connrcted to #{channel}")
    
    
    await ctx.send("1") #1
    print("Someone wants to play music let me get that ready for them...")
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    youtube = pytube.YouTube(url)
    mp3 = youtube.streams.filter(only_audio=True).first()
    mp3.download('./music/queue')
    
    for file in os.listdir("./music/queue"):
        if file.endswith(".mp4"):
            if queue != -1:
                try:
                    os.rename(f"./music/queue/{file}", f"./music/queue/song{queue+1}.mp3")
                    queue+=1
                except FileExistsError:
                    for file1 in os.listdir("./music/queue"):
                        if file1.endswith(".mp3"):
                            try:
                                os.remove(f"./music/queue/{file1}")
                            except FileNotFoundError:
                                pass
                    os.rename(f"./music/queue/{file}", f"./music/queue/song{queue+1}.mp3")
                    queue+=1         
            else:
                try:
                    os.rename(f"./music/queue/{file}", './music/queue/song0.mp3')
                    queue = 0
                except FileExistsError:
                    for file1 in os.listdir("./music/queue"):
                        if file1.endswith(".mp3"):
                            try:
                                os.remove(f"./music/queue/{file1}")
                            except FileNotFoundError:
                                pass
                    os.rename(f"./music/queue/{file}", './music/queue/song0.mp3')
                    queue = 0
    print(isp)
    if not isp:
        thread = player()
        print("isp changed")    
        isp = True
        #try:
        thread.start()
        #except RuntimeError:
            #print("excepted")
            #thread.join()
            #thread.start()
    
@bot.command(pass_context=False)    
async def leave(ctxx):
    global queue
    global ctx
    ctx = ctxx
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")
    try:
        for file in os.listdir("./music"):
            if file.endswith(".mp3"):
                os.remove(f"./music/{file}")
    except:
        pass
    np = ""
    queue = 0
    
@bot.command(pass_context=False)    
async def stop(ctxx):
    global queue, current_song
    global ctx
    ctx = ctxx
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.stop()
    await ctx.send(f"Left {channel}")
    try:
        for file in os.listdir("./music"):
            if file.endswith(".mp3"):
                os.remove(f"./music/{file}")
    except:
        pass
    np = ""
    queue = -1
    current_song = -1
    
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
    
bot.run('ODg3MzEwNDk0MjIwODQwOTkx.YUCSSw.eBXeRPhKIyhdF6_epRN6aTlAbZc')