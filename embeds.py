import discord
import random, math
from youtube_search import YoutubeSearch

class Embeds:
    def __init__(self):
        pass
    
    def NPEmbed(self, title, url, time1, time2, ctx): 
        
        embed = discord.Embed(title=title, url=url, description=f"{self.__formated_line(time1, time2)}", color=0xFF00FF)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(url=self.__get_tb(title))
        time = self.__time_format(time1, time2)
        embed.add_field(name="Продолжительность:", value=f"`{time[0]} / {time[1]}`")
        return embed
    
    def added_to_queue(self):
        pass
    
    def __formated_line(self, time1, time2):
        def_str = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"

        pos = time1*(len(def_str)/time2)
        def_str = def_str[:int(pos)] + "🔘" + def_str[int(pos)+1:]
        return def_str
    
    def __get_tb(self, title):
        tb = YoutubeSearch(title, max_results=1).to_dict()[0]['thumbnails'][0]
        #print(tb)
        #print(YoutubeSearch(title, max_results=1).to_dict()[0])
        return tb
    
    def __time_format(self, time1, time2):
        time1, time2 = int(math.floor(time1)), int(math.floor(time2))
        d = [str(time1//3600), str(time2//3600), str(time1%3600//60), str(time2%3600//60), str(time1%60), str(time2%60)]
        for i in range(len(d)):
            if len(d[i]) == 1:
                d[i] = f"0{d[i]}"
        return f"{d[0]}:{d[2]}:{d[4]}", f"{d[1]}:{d[3]}:{d[5]}"
    