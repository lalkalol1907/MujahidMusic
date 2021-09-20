import discord
import random, math
from youtube_search import YoutubeSearch

class Embeds:
    def __init__(self):
        pass
    
    def NPEmbed(self, title, url, time1, time2, ctx): 
        def __time_format(time1, time2):
            time1, time2 = int(math.floor(time1)), int(math.floor(time2))
            d = [str(time1//3600), str(time2//3600), str(time1%3600//60), str(time2%3600//60), str(time1%60), str(time2%60)]
            for i in range(len(d)):
                if len(d[i]) == 1:
                    d[i] = f"0{d[i]}"
            return f"{d[0]}:{d[2]}:{d[4]}", f"{d[1]}:{d[3]}:{d[5]}"
        embed = discord.Embed(title=title, url=url, description=f"{self.__formated_line(time1, time2)}", color=0xFF00FF)
        embed.set_author(name="Now Playing:", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(url=self.__get_tb(title))
        time = __time_format(time1, time2)
        embed.add_field(name="Duration:", value=f"`{time[0]} / {time[1]}`")
        return embed
    
    def added_to_queue(self, title, url, time, ctx, queue, current_song):
        def __time_format(time):
            d = [str(time//3600), str(time%3600//60), str(time%60)]
            for i in range(len(d)):
                if len(d[i]) == 1:
                    d[i] = f"0{d[i]}"
            return f"{d[0]}:{d[1]}:{d[2]}"
        embed = discord.Embed(title=title, url=url, color=0x5CFF61)
        embed.set_author(name="Added to queue:", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(url=self.__get_tb(title))
        embed.add_field(name="Duration:", value=f"`{__time_format(time)}`", inline=True)
        embed.add_field(name="Position in queue:", value=f"`{queue-current_song}`", inline=True)
        return embed
    
    def playing(self, title, url, time, ctx):
        def __time_format(time):
            d = [str(time//3600), str(time%3600//60), str(time%60)]
            for i in range(len(d)):
                if len(d[i]) == 1:
                    d[i] = f"0{d[i]}"
            return f"{d[0]}:{d[1]}:{d[2]}"
        embed = discord.Embed(title=title, url=url, color=0x1200DA)
        embed.set_author(name="Playing:", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(url=self.__get_tb(title))
        embed.add_field(name="Duration:", value=f"`{__time_format(time)}`", inline=True)
        return embed
    
    def __formated_line(self, time1, time2):
        def_str = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        pos = time1*(len(def_str)/time2)
        def_str = def_str[:int(pos)] + "🔘" + def_str[int(pos)+1:]
        return def_str
    
    def __get_tb(self, title):
        return YoutubeSearch(title, max_results=1).to_dict()[0]['thumbnails'][0]
    
    def queue(self, songs, current_song, queue, ctx, ctime):
        def __time_format1(time):
            d = [str(time//3600), str(time%3600//60), str(time%60)]
            for i in range(len(d)):
                if len(d[i]) == 1:
                    d[i] = f"0{d[i]}"
            return f"{d[0]}:{d[1]}:{d[2]}"
        
        embed = discord.Embed(title=f"1) {songs[current_song].name}", url=f"{songs[current_song].url}", description=f"{self.__formated_line(ctime, songs[current_song].long)}\n`Elapsed: {__time_format1(int(songs[current_song].long - ctime))}`", color=0x5C02C2)
        embed.set_thumbnail(url=self.__get_tb(songs[current_song].name))
        embed.set_author(name = "Queue:", icon_url=ctx.author.avatar_url)
        for i in range(current_song+1, len(songs)):
            if i == len(songs)-1:
                embed.add_field(name=f"`{i-current_song+1}) {songs[i].name}`", value=f"   Duration: `{__time_format1(int(songs[i].long))}`", inline=False)
            else:
                embed.add_field(name=f"`{i-current_song+1}) {songs[i].name}`", value=f"   Duration: `{__time_format1(int(songs[i].long))}`\n", inline=False)
        return embed