from discord.ext import commands
import discord

bot = commands.Bot(command_prefix = '!') #alle Nachrichten mit Präfix: !

def caps_pls(text):
    return text.upper()

#Text wiedergeben
@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)

@say.error #Error Handling für Say
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Bitte gebe an, was ich sagen soll.')

#Text in Caps wiedergeben
@bot.command()
async def caps(ctx, *, arg: caps_pls):
    await ctx.send(arg)

@caps.error
async def caps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Bitte gebe an, was ich schreien soll.')

#Member töten
@bot.command()
async def kill(ctx, member: discord.Member):
    await ctx.send(f'{member.display_name} wurde gekillt.')

@kill.error
async def kill_error(ctx, error):
    if isinstance(error, commands.BadArgument): #BadArgument: zb wenn User nicht auf Server ist
        await ctx.send('Ich kann diesen Member nicht finden.')

bot.run('')