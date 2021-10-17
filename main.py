from Discord.DiscordMain import DiscordStart
from TG.TGBot import TgBotRun
import asyncio
import threading


if __name__ == '__main__':
    discord = threading.Thread(target=DiscordStart)
    discord.start()
    
    asyncio.run(TgBotRun())