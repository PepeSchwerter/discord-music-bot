import os
from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands

import wavelink

from messages import get_comment

load_dotenv()

intents = nextcord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=";", intents = intents)

@bot.event
async def on_ready():
    print("Toy listo manito")
    bot.loop.create_task(node_connect())

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host="lavalink.oops.wtf", port=443, password="www.freelavalink.ga", https=True)

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
        await ctx.send(f"Colocando de nuevo \"`{track.title}`\"")
        return await vc.play(track)
    
    # if vc.queue.is_empty:
    #     return await vc.disconnect()

    if not vc.queue.is_empty:
        next_song =  vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"Colocando \"`{next_song.title}`\", {get_comment()}")

@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Primero unete a un chat de voz manito")
    elif not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and (not vc.track):
        await vc.play(search)
        await ctx.send(f"Colocando \"`{search.title}`\", {get_comment()}")
    else:
        await vc.queue.put_wait(search)
        await ctx.send(f"\"`{search.title}`\" añadido a la cola")
    
    vc.ctx = ctx
    setattr(vc, "loop", False)
    
@bot.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Como voy a pausar si no estoy tocando nada manito")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Primero unete a un chat de voz manito")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.pause()
    await ctx.send("Musica pausada manito")

@bot.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Que voy a devolver si no estoy tocando nada manito")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Primero unete a un chat de voz manito")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.resume()
    await ctx.send("La musica esta de vuelta manito")

@bot.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Que voy a parar si no estoy tocando nada manito")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Primero unete a un chat de voz manito")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.stop()
    await ctx.send("Ya apague la musica manito")

@bot.command()
async def disconnect(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Como me voy a ir si no he llegado manito")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Primero unete a un chat de voz manito")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.disconnect()
    await ctx.send("Adios manito")

@bot.command()
async def loop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Que voy a hacer si no he llegado manito")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Primero unete a un chat de voz manito")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    try:
        vc.loop = not vc.loop
    except:
        setattr(vc, "loop", True)
    if vc.loop:
        return await ctx.send("Loop activado manito")
    else:
        return await ctx.send("Loop desactivado manito")

bot.run(os.getenv("TOKEN"))