from discord.ext import commands
from discord.utils import get   
import asyncio
from Bot import Bot, bot

class Aliases:
    def __init__(self):
        self.p = ['play', 'P', 'Play', 'PLAY']
        self.np = ['NP', 'Np']
        self.q = ['q', 'Q']
        self.fs = ['skip', 'Fs', 'FS', 'SKIP', 'Skip']
    
bots = []
status = False

async def check_bot(ctx):
    if bots != []:
        for i in range(len(bots)):
            if bots[i].server == ctx.message.guild:
                return True, i
    return False, -1

@bot.command(pass_context=False, aliases = Aliases().fs)
async def fs(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].fs(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].fs(ctx)

@bot.command(pass_context=True, aliases = Aliases().p)
async def p(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].p(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].p(ctx, text)
     
@bot.command(pass_context=False)    
async def leave(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].leave(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].leave(ctx)

@bot.command(pass_context=False)   
async def stop(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].stop(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].stop(ctx)

@bot.command(pass_context=False)
async def pause(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].pause(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].pause(ctx)

@bot.command(pass_context=False)
async def resume(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].resume(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].resume(ctx)

@bot.command(pass_context=False, aliases=Aliases().np)
async def np(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].np(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].np(ctx)

@bot.command(pass_context=False, aliases = Aliases().q)
async def queue(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].queue1(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].queue1(ctx)

@bot.command(pass_context = False)
async def vk(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].vk(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].vk(ctx, text)
        
@bot.command(pass_context = False)
async def loop(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].loop(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].loop(ctx, text)
        
while True:        
    print("bot restarted")
    asyncio.get_event_loop().run_until_complete(bot.start('ODg3MzEwNDk0MjIwODQwOTkx.YUCSSw.eBXeRPhKIyhdF6_epRN6aTlAbZc'))
    print("bot died")