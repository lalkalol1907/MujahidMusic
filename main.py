import discord
import os
from discord.ext import commands
from discord.utils import get
import asyncio
from downloader import *
from embeds import Embeds

client = discord.Client()
bot = commands.Bot(command_prefix='$')

queue = -1
isp = False
current_song = -1
ctx = None
stop_thread = False
stop_voice = False
ctime = 0
kick_checker_bool = False
allower = False    
cleaner_bool = False
fscount = 0
sss = 0   

class Soprogs:
    def __init__(self):
        pass
    
    async def clear(self, path):
        if [] != os.listdir(path):
                try:
                    for file in os.listdir(path):
                        if file.endswith(".mp3"):
                            os.remove(f"{path}/{file}")
                except: pass
                
    async def cleaner(self):
        global current_song
        already_deleted = []
        print("cleaner started")
        while True:
            if current_song > 0:
                for i in range(0, current_song):
                    if i not in already_deleted:
                        try:
                            os.remove(f"./music/queue/song{i}.mp3")
                            already_deleted.append(i)
                        except Exception as ex:
                            print(f"Can't delete, exception {ex}")
                            if "song0" in str(ex):
                                already_deleted.append(0)
            await asyncio.sleep(30)  
     
    async def MusicPlayer(self, voice, s = 0):
        print("runned")
        global stop_thread, stop_voice, ctime, isp, queue, current_song, songs, ctx, sss
        print(len(songs))
        for ss in range(s, len(songs)): 
            sss = ss
            try:
                current_song += 1
                if current_song > queue:
                    current_song-=1; break
                voice.stop()
                song = songs[ss]
                print(song)
                dur = song.long
                voice.play(discord.FFmpegPCMAudio(f"./music/queue/song{ss}.mp3"))
                await ctx.send(embed=Embeds().playing(song.name, song.url, int(dur), ctx))
                ctime = 0
                for i in range(int(dur)+3):
                    try:
                        if stop_thread is True:
                            voice.stop()
                            stop_thread = False
                            print("stopped")
                            ss+=1
                            await self.MusicPlayer(voice, ss)
                            break
                        if stop_voice is True:
                            voice.stop()
                            stop_voice = False
                            break
                    finally:
                        pass
                    ctime += 1
                    await asyncio.sleep(1)
                if current_song <= queue:
                    ss+=1
                    await self.MusicPlayer(voice, ss)
            except Exception as ex:
                print(ex) 
        else:
            sss = s+1
        isp = False
        
    async def kick_checker(self, ctx):
        global queue, current_song, stop_voice, songs, isp, allower, sss
        print("kickchecker started")
        sp = Soprogs()
        while True:
            voice = get(bot.voice_clients, guild=ctx.guild)
            if not voice and allower:
                queue, current_song, isp, sss = -1, -1, False, 0
                await asyncio.sleep(1)
                await sp.clear("./music/queue")
                songs.clear()
                allower = True
            await asyncio.sleep(2)

class Bot:
    @staticmethod
    @bot.command(pass_context=False, aliases = ['skip', 'Fs', 'FS', 'SKIP', 'Skip'])
    async def fs(ctxx):
        global ctx
        ctx = ctxx
        global current_song, stop_thread, fscount
        stop_thread = True
        fscount += 1
        
    @staticmethod
    @bot.command(pass_context=True, aliases = ['play', 'P', 'Play', 'PLAY'])
    async def p(ctxx, *, text): # play
   # await ctx.send(arg)
        global queue, isp, kick_checker_bool, songs, allower, cleaner_bool, ctx, sss
        ctx = ctxx
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f"Connected to `#{channel}`")
        dw = Downloader(queue, ctx)
        await dw.analyze(text)
        queue = dw.queue        
        sp = Soprogs()    
        if isp:
            song = songs[queue]
            await ctx.send(embed=Embeds().added_to_queue(song.name, song.url, int(song.long), ctx, queue, current_song))
            pass
        if not kick_checker_bool:
            asyncio.get_event_loop().create_task(sp.kick_checker(ctx))
            kick_checker_bool = True
            allower = True    
        if not isp:
            #print("isp changed")    
            isp = True
            asyncio.get_event_loop().create_task(sp.MusicPlayer(voice, sss))
            print("after")
        if not cleaner_bool:
            asyncio.get_event_loop().create_task(sp.cleaner())
            cleaner_bool = True
            
    @staticmethod
    @bot.command(pass_context = True)
    async def vk(ctxx, *, text):
        global ctx
        ctx = ctxx
        await ctx.send("In development =)")
        return
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f"Connected to `#{channel}`")
        
        voice.play(discord.FFmpegOpusAudio("https://cs1-82v4.vkuseraudio.net/p24/2d8c304bd0442e.mp3?extra=cfihgRks4dKdRugxjILr-nIzgJowmNzJGLcTRVpAcLVluOiQGm7y8qvaG7OVyFiSM1P8TDfzOgmzsztIeHjvtqMT5APOHu_SWQOKYUpy6bm5FCqGjgK7gVFTsdrcF1BHGMjTyVe_MhVpTdFe336phVNUvw&long_chunk=1"))
            
    @staticmethod        
    @bot.command(pass_context=False)    
    async def leave(ctxx):
        global queue, current_song, stop_voice, songs, ctx, isp, sss
        ctx = ctxx
        stop_voice = True
        queue, current_song, isp, sss = -1, -1, False, 0
        channel = ctx.message.author.voice.channel
        await asyncio.sleep(1)
        await ("./music/queue")
        stop_voice = False
        songs.clear()
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Left `{channel}`")
        else: 
            await ctx.send("Not connected to the channel")
    
    @staticmethod
    @bot.command(pass_context=False)    
    async def stop(ctxx):
        global queue, current_song, stop_voice, songs, ctx, isp, sss
        ctx = ctxx
        stop_voice = True
        await asyncio.sleep(1)
        await Soprogs().clear("./music/queue")
        queue, current_song, isp, sss = -1, -1, False, 0
        songs.clear()
        stop_voice = False
    
    @staticmethod
    @bot.command(pass_context=False)
    async def pause(ctxx):
        ctx = ctxx
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused(): 
            voice.resume()
        else: 
            voice.pause()
        
    @staticmethod    
    @bot.command(pass_context=False)
    async def resume(ctxx):
        ctx = ctxx
        voice = get(bot.voice_clients, guild=ctx.guild)
        voice.resume()
    
    @staticmethod
    @bot.command(pass_context=False, aliases = ['NP', 'Np'])
    async def np(ctxx):
        global ctx, current_song, ctime, long, songs
        ctx = ctxx
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            if isp: 
                song = songs[current_song]
                await ctx.send(embed=Embeds().NPEmbed(title=song.name, url=song.url, time1 = ctime, time2 = song.long,  ctx = ctxx))
            else: 
                await ctx.send("Nothing is playing now")
        else: 
            await ctx.send("Not connected to the channel")
        
    @staticmethod    
    @bot.command(pass_context=True)
    async def loop(ctxx, *, text):
        await ctxx.send("`This function is being developed now`")
    
    @staticmethod
    @bot.command(pass_context=False)
    async def queue(ctxx):
        global ctx, current_song, songs, queue, fscount
        ctx = ctxx
        if queue == 0:
            await ctx.send("There is nothing to play!")
        elif not isp:
            await ctx.send("Nothing is playing now!")
        else: 
            await ctx.send(embed = Embeds().queue(songs, current_song, queue, ctxx, ctime))
            
    
bot.run('ODg3MzEwNDk0MjIwODQwOTkx.YUCSSw.eBXeRPhKIyhdF6_epRN6aTlAbZc')