import discord
import math
from youtube_search import YoutubeSearch


class Embeds:
    @staticmethod
    def __time_format1(time):
            d = [str(time // 3600), str(time % 3600 // 60), str(time % 60)]
            for i in range(len(d)):
                if len(d[i]) == 1:
                    d[i] = f"0{d[i]}"
            return f"{d[0]}:{d[1]}:{d[2]}"
        
    @staticmethod    
    def __time_format2(time1, time2):
            time1, time2 = int(math.floor(time1)), int(math.floor(time2))
            d = [str(time1 // 3600), str(time2 // 3600), str(time1 % 3600 // 60), str(time2 % 3600 // 60),
                 str(time1 % 60), str(time2 % 60)]
            for i in range(len(d)):
                if len(d[i]) == 1:
                    d[i] = f"0{d[i]}"
            return f"{d[0]}:{d[2]}:{d[4]}", f"{d[1]}:{d[3]}:{d[5]}"
    
    def NPEmbed(self, title, url, time1, time2, ctx, loop, curloop) -> discord.Embed:
        embed = discord.Embed(title=title, url=url, description=f"{self.__formatted_line(time1, time2)}",
                              color=0xF05C3B)
        embed.set_author(name="Now Playing:", icon_url=f"{ctx.author.avatar_url}")
        try:
            embed.set_thumbnail(url=self.__get_tb(title))
        except:
            pass
        time = self.__time_format2(time1, time2)
        embed.add_field(name="Duration:", value=f"`{time[0]} / {time[1]}`")
        if loop != 1:
            embed.add_field(name="Loop:", value=f"`{curloop}/{loop}`")
        return embed

    def added_to_queue(self, title, url, time, ctx, queue, current_song, loop=1) -> discord.Embed:
        def __time_format(time):
            d = [str(time // 3600), str(time % 3600 // 60), str(time % 60)]
            for i in range(len(d)):
                if len(d[i]) == 1:
                    d[i] = f"0{d[i]}"
            return f"{d[0]}:{d[1]}:{d[2]}"

        embed = discord.Embed(title=title, url=url, color=0xA2D5C6)
        embed.set_author(name="Added to queue:", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(url=self.__get_tb(title))
        embed.add_field(name="Duration:", value=f"`{__time_format(time)}`", inline=True)
        embed.add_field(name="Position in queue:", value=f"`{queue - current_song}`", inline=True)
        if int(loop) != 1:
            embed.add_field(name="Loop:", value=f"`{int(loop)}`")
        return embed
    
    def added_tg(self, title, time, queue, current_song):
        embed = discord.Embed(title=title, color=0xA2D5C6)
        embed.set_author(name="Added to queue from TG:") # TODO: Добавить аву автора из дс или тг
        embed.add_field(name="Duration:", value=f"`{self.__time_format1(time)}`", inline=True)
        embed.add_field(name="Position in queue:", value=f"`{queue - current_song}`", inline=True)

    def added_to_queue_pack(self, ctx, songsarray, url="") -> discord.Embed:
        title = "User playlist"
        if url == "":
            embed = discord.Embed(title=title, color=0xA2D5C6)
        else:
            embed = discord.Embed(title=title, url=url, color=0xA2D5C6)
        embed.set_thumbnail(url=self.__get_tb(songsarray[0].title))
        embed.set_author(name="Added to queue:", icon_url=f"{ctx.author.avatar_url}")
        dur = 0
        for song in songsarray:
            embed.add_field(name="", value=f"`{song.name}`", inline=False)
            dur += song.long
        embed.add_field(name=f"Duration:", value=f"`{self.__time_format1(int(dur))}`", inline=True)
        embed.add_field(name=f"Number:", value=f"`{len(songsarray)}`", inline=True)
        return embed

    def playing(self, title, url, time, ctx, loop=None) -> discord.Embed:
        embed = discord.Embed(title=title, url=url, color=0x077B8A)
        embed.set_author(name="Playing:", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(url=self.__get_tb(title))
        embed.add_field(name="Duration:", value=f"`{self.__time_format1(time)}`", inline=True)
        if loop:
            embed.add_field(name="Loop: ", value=f"`{int(loop)}`", inline=True)
        return embed

    @staticmethod
    def __formatted_line(time1, time2) -> str:
        def_str = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        pos = time1 * (len(def_str) / time2)
        def_str = def_str[:int(pos)] + "🔘" + def_str[int(pos) + 1:]
        return def_str

    @staticmethod
    def __get_tb(title):
        return YoutubeSearch(title, max_results=1).to_dict()[0]['thumbnails'][0]

    def queue(self, songs, current_song, ctx, ctime, curloop) -> discord.Embed:
        desc = f"{self.__formatted_line(ctime, songs[current_song].long)}\n`Elapsed: {self.__time_format1(int(songs[current_song].long - ctime))}`" + f"\n`Loop: {curloop}{int(songs[current_song.loop])}`" * (int(songs[current_song].loop) != 1)
        embed = discord.Embed(title=f"1) {songs[current_song].name}", url=f"{songs[current_song].url}", description=desc, color=0x5C3C92)
        try:
            embed.set_thumbnail(url=self.__get_tb(songs[current_song].name))
        except:
            pass
        embed.set_author(name="Queue:", icon_url=ctx.author.avatar_url)
        for i in range(current_song + 1, len(songs)):
            value = f"   Duration: `{self.__time_format1(int(songs[i].long))}`" + f"\nLoop: `{int(songs[i].loop)}`" * (int(songs[i].loop) != 1) + '\n' * (i != len(songs) - 1)
            embed.add_field(name=f"`{i - current_song + 1}) {songs[i].name}`", value=value, inline=False)
        return embed