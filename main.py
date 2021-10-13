from Discord.Bot import Bot, bot
from config import DiscordCFG

class Aliases:
    def __init__(self):
        self.p = ['play', 'P', 'Play', 'PLAY']
        self.np = ['NP', 'Np']
        self.q = ['q', 'Q']
        self.fs = ['skip', 'Fs', 'FS', 'Skip', "SKIP"]
        self.loop = ['loop', 'Loop']

bots = []

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
        
@bot.command(pass_context=True)        
async def pp(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].play_in_pos(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].play_in_pos(ctx, text)
        
@bot.command(pass_context=True)        
async def pn(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].play_now(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].play_now(ctx, text)

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
            
@bot.command(pass_context=False)
async def connect(ctx):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].connect(ctx)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].connect(ctx)
            
@bot.command(pass_context=True)
async def channel(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].channel(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].channel(ctx, text)
            
@bot.command(pass_context=True)
async def v(ctx, *, value):
    pass 

@bot.command(pass_context=True)
async def pack(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    await ctx.send("`You can play packs with usual $p function.`")
    if already_is:
        await bots[bot_index].pack(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].pack(ctx, text)
        
@bot.command(pass_context=True)
async def ss(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].skip_parameters(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].skip_parameters(ctx, text)

@bot.command(pass_context=True, aliases=Aliases().loop)
async def pl(ctx, *, text):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        await bots[bot_index].play_loop(ctx, text)
    else:
        bots.append(Bot(len(bots), ctx))
        await bots[len(bots)-1].play_loop(ctx, text)


bot.run(DiscordCFG().BOT_TOKEN)