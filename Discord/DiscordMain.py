from Discord.Bot import Bot, bot
from Discord.bots import bots
from config import DiscordCFG
from DB.DB import *


class Aliases:
    def __init__(self):
        self.p = ['play', 'P', 'Play', 'PLAY']
        self.np = ['NP', 'Np']
        self.q = ['q', 'Q']
        self.fs = ['skip', 'Fs', 'FS', 'Skip', "SKIP"]
        self.loop = ['loop', 'Loop']


async def check_bot(ctx):
    if bots:
        for i in range(len(bots)):
            if bots[i].server == ctx.message.guild:
                return True, i
    return False, -1


async def func_start(command, ctx, text=""):
    already_is, bot_index = await check_bot(ctx)
    if already_is:
        num = bot_index
    else:
        bots.append(Bot(len(bots), ctx))
        ServerDB().reg(ctx.guild)
        num = len(bots) - 1
    match command:
        case "fs":
            await bots[num].fs(ctx)
        case "p":
            await bots[num].p(ctx, text)
        case "leave":
            await bots[num].leave(ctx)
        case "stop":
            await bots[num].stop(ctx)
        case "pause":
            await bots[num].pause(ctx)
        case "resume":
            await bots[num].resume(ctx)
        case "pp":
            await bots[num].play_in_pos(ctx, text)
        case "pn":
            await bots[num].play_now(ctx, text)
        case "np":
            await bots[num].np(ctx)
        case "queue":
            await bots[num].queue1(ctx)
        case "vk":
            await bots[num].vk(ctx, text)
        case "connect":
            await bots[num].connect(ctx)
        case "channel":
            await bots[num].channel(ctx, text)
        case "v":
            pass
        case "pack":
            await bots[num].pack(ctx, text)
        case "ss":
            await bots[num].skip_parameters(ctx, text)
        case "pl":
            await bots[num].play_loop(ctx, text)
        case "key":
            await ctx.send(ServerDB().get_key(ctx.guild.id))


@bot.command(pass_context=False, aliases=Aliases().fs)
async def fs(ctx):
    await func_start("fs", ctx)


@bot.command(pass_context=True, aliases=Aliases().p)
async def p(ctx, *, text):
    await func_start("p", ctx, text)


@bot.command(pass_context=False)
async def leave(ctx):
    await func_start("leave", ctx)


@bot.command(pass_context=False)
async def stop(ctx):
    await func_start("stop", ctx)


@bot.command(pass_context=False)
async def pause(ctx):
    await func_start("pause", ctx)


@bot.command(pass_context=False)
async def resume(ctx):
    await func_start("resume", ctx)


@bot.command(pass_context=True)
async def pp(ctx, *, text):
    await func_start("pp", ctx, text)


@bot.command(pass_context=True)
async def pn(ctx, *, text):
    await func_start("pn", ctx, text)


@bot.command(pass_context=False, aliases=Aliases().np)
async def np(ctx):
    await func_start("np", ctx)


@bot.command(pass_context=False, aliases=Aliases().q)
async def queue(ctx):
    await func_start("queue", ctx)


@bot.command(pass_context=False)
async def vk(ctx, *, text):
    await func_start("vk", ctx, text)


@bot.command(pass_context=False)
async def connect(ctx):
    await func_start("connect", ctx)


@bot.command(pass_context=True)
async def channel(ctx, *, text):
    await func_start("channel", ctx, text)


@bot.command(pass_context=True)
async def v(ctx, *, text):
    await func_start("v", ctx, text)


@bot.command(pass_context=True)
async def pack(ctx, *, text):
    await func_start("pack", ctx, text)


@bot.command(pass_context=True)
async def ss(ctx, *, text):
    await func_start("ss", ctx, text)


@bot.command(pass_context=True, aliases=Aliases().loop)
async def pl(ctx, *, text):
    await func_start("pl", ctx, text)


@bot.command(pass_context=False)
async def key(ctx):
    await func_start("key", ctx)


def DiscordStart():
    bot.run(DiscordCFG().BOT_TOKEN)
