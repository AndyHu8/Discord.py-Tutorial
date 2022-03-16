from dis import disco
import os
from unicodedata import name
import discord
from discord.ext import commands
import youtube_dl

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'play')
    async def play(self, ctx, url):
        voicec = ctx.author.voice

        if voicec: #wenn User im Voicechannel drin ist
            channel = voicec.channel

            if channel:
                songname = f'songs/{ctx.guild.id}_current.mp3'
                song_there = os.path.isfile(songname) #ob ein Song schon da ist

                try:
                    if song_there:
                        os.remove(songname) #aktueller Song entfernen
                        print('Remove ols song file.')
                except PermissionError:
                    print('Trying to delete song file, but its being player')
                    await ctx.send('Error: Music playing')
                    return

                #Song von YT runterladen
                voice = await channel.connect()
                yt_opts = {
                    'format': 'bestaudio/best',
                    'postprocessor': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                    }]
                }

                with youtube_dl.YoutubeDL(yt_opts) as ydl:
                    print('Downloading audio now\n')
                    ydl.download([url])

                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        print(f'Renamed File: {file}\n')
                        os.rename(file, songname)

                voice.play(discord.FFmpegPCMAudio(songname), after = lambda e: print('Song zuende.'))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                print('Ok.')

#############################################################################################################
def setup(bot):
    bot.add_cog(PlayCommand(bot))