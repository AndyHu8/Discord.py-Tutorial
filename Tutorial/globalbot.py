from discord import Message
from discord import Guild
from discord import TextChannel
from discord.ext import commands
import discord
import os
import json

bot = commands.Bot(command_prefix = '!') #alle Nachrichten mit Präfix: !

if os.path.isfile("servers.json"): #wenn Datei existiert
    with open('servers.json', encoding = 'utf-8') as file:
        servers = json.load(file)
else: #wenn Datei nicht exisitiert
    servers = {'servers': []}
    with open('servers.json', 'w') as file:
        json.dump(servers, file, indent = 4)

#############################################################################
#Zur Global Serverliste hinzufügen
@bot.command()
async def addGlobal(ctx):
    if ctx.author.guild_permissions.administrator: #wenn der User Admin ist
        if not guild_exists(ctx.guild.id): #wenn Server nicht drin ist
            server = {
                'guildId': ctx.guild.id,
                'channelId': ctx.channel.id,
                'invite': f'{(await ctx.channel.create_invite()).url}'
            }
            servers['servers'].append(server) #Zur Serverliste hinzufügen
            with open('servers.json', 'w') as file:
                json.dump(servers, file, indent = 4)
            await ctx.send('Erstellt / Zur Serverliste hinzugefügt.')

#Vom Global Serverliste löschen
@bot.command()
async def removeGlobal(ctx):
    if ctx.author.guild_permissions.administrator:
        if guild_exists(ctx.guild.id): #wenn Server drin ist
            globalid = get_globalchat_id(ctx.guild.id)
            if globalid != -1:
                servers['servers'].pop(globalid)
                with open('servers.json', 'w') as file:
                    json.dump(servers, file, indent = 4)
                await ctx.send('Gelöscht / Vom Serverliste gelöscht.')

#############################################################################
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.content.startswith('!'):
        if get_globalchat(message.guild.id, message.channel.id):
            await sendAll(message)

    await bot.process_commands(message)

async def sendAll(message: Message):
    embed: discord.Embed(description = message.content)
    embed.set_footer(text = f'Gesendet von {message.author.display_name} auf {message.guild.name}')
    for server in servers['servers']: #nachricht schicken an alle Server
        guild: Guild = bot.get_guild(int(server['guildid']))
        if guild:
            channel: TextChannel = guild.get_channel(int(server['channelid']))
            if channel:
                await channel.send(embed = embed)

    await message.delete()

#############################################################################
#Hilfsfunktionen
def guild_exists(guildId): #schauen ob Server schon exisistiert
    for server in servers['servers']:
        if int(server['guildId']) == int(guildId):
            return True
    return False

def get_globalchat(guildId, channelId = None):
    globalchat = None
    for server in servers['servers']:
        if int(server['guildId']) == int(guildId):
            if channelId:
                if int(server['channelId']) == int(channelId):
                    globalchat = server
            else:
                globalchat = server
    return globalchat

#ChannelId zurückgeben
def get_globalchat_id(guildId):
    globalchat = -1
    i = 0
    for server in servers['servers']:
        if int(server['guildId']) == int(guildId):
            globalchat = i
        i += 1
    return globalchat

#############################################################################
bot.run('')