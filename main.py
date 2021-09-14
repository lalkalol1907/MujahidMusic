import discord
import pytube
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from threading import Thread
import time
import pyglet


client = discord.Client()
bot = commands.Bot(command_prefix='$')

np = ""
queue = 0
isp = False

current_song = -1

def player(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    global isp, queue, current_song
    current_dir = os.listdir("./music")    
    for file in os.listdir("./music"):
        try:
            voice.play(discord.FFmpegPCMAudio(f"./music/{file}"))
            current_song += 1
            song = pyglet.media.load(f"./music/{file}")
            time.sleep(song.duration)
            if current_dir != os.listdir("./music"):
                os.remove(f"./music/{file}")
                player()
        except:
            print(Exception)
            
    isp = False
    queue = 0
    for file in os.listdir("./music"):
        os.remove(f"./music/{file}")
        
#th = Thread(target=player)

def start_playing(ctx):
    global isp
    if not isp:
        print("isp changed")    
        isp = True
        th = Thread(target=player, args=(ctx, ))
        th.start()
        
"""     
@bot.command(pass_context=False)
async def fs(ctx):
    global current_song
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    #os.remove(f"./music/song{current_song}.mp3")
    try:
        voice.play(discord.FFmpegPCMAudio(f"./music/song{current_song+1}.mp3"))
        current_song += 1
    except:
        pass
        """

@bot.command(pass_context=True)
async def p(ctx, url): # play
   # await ctx.send(arg)
    
    global queue, isp, np
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
    mp3.download('./music')
    
    for file in os.listdir("./music"):
        if file.endswith(".mp4"):
            if queue:
                try:
                    os.rename(f"./music/{file}", f"./music/song{queue}.mp3")
                    queue+=1
                except FileExistsError:
                    for file1 in os.listdir("./music"):
                        if file1.endswith(".mp3"):
                            os.remove(f"./music/{file1}")
                    os.rename(f"./music/{file}", f"./music/song{queue}.mp3")
                    queue+=1         
            else:
                try:
                    os.rename(f"./music/{file}", './music/song0.mp3')
                    queue = 1
                except FileExistsError:
                    for file1 in os.listdir("./music"):
                        if file1.endswith(".mp3"):
                            os.remove(f"./music/{file1}")
                    os.rename(f"./music/{file}", './music/song0.mp3')
                    queue = 1
    print(isp)
    start_playing(ctx)
    """
    def player():
        global isp, queue
        current_dir = os.listdir("./music")    
        for file in os.listdir("./music"):
            try:
                voice.play(discord.FFmpegPCMAudio(f"./music/{file}"))
                song = pyglet.media.load(f"./music/{file}")
                time.sleep(song.duration)
                if current_dir != os.listdir("./music"):
                    os.remove(f"./music/{file}")
                    player()
            except:
                print(Exception)
            
        isp = False
        queue = 0
        for file in os.listdir("./music"):
            os.remove(f"./music/{file}")
    if not isp:
        print("isp changed")    
        isp = True
        th = Thread(target=player)
        th.start()"""

@bot.command(pass_context=False)    
async def stop(ctx):
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
    
@bot.command(pass_context=False)
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        voice.pause()
        
@bot.command(pass_context=False)
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.resume()
    
bot.run('ODg3MzEwNDk0MjIwODQwOTkx.YUCSSw.eBXeRPhKIyhdF6_epRN6aTlAbZc')