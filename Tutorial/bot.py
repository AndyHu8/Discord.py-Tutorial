import asyncio
from turtle import color
from unicodedata import name
import discord
from discord import Member

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print('Ich bin eingeloggt als User: {}'.format(client.user.name))
    client.loop.create_task(status_task())

async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('CB8 11.03.22 Gibt euch!'), status=discord.Status.online)
        await asyncio.sleep(3)
        await client.change_presence(activity=discord.Game('Berlin lebt Brrrrraa!'), status=discord.Status.online)
        await asyncio.sleep(3)

@client.event
async def on_message(message):
    if message.author.bot: #Wenn User ein Bot ist
        return
    await message.channel.send('Du nervst mit dieser Nachricht: {}'.format(message.content))

    if '!help' in message.content:
        await message.channel.send('**Hilfe zum PythonBot**\r\n'
                                    '!help - Zeigt diese Hilfe an')

    if message.content.startswith('!userinfo'):
        args = message.content.split(' ') #zB !userinfo Andy
        if len(args) == 2: #wenn 2 Wörter sind
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members) #sucht alle member + vergleicht mit Andy
            if member: #wenn member vorhanden ist
                embed = discord.Embed(title='UserInfo für {}'.format(member.name),
                                        description='Dies ist eine Userinfo für den User {}'.format(member.mention),
                                        color=0X22A7F0)

                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default(): #nicht @everyone
                        rollen += '{} \r\n'.format(role.mention)
                
                if rollen: #wenn rollen nicht leer sind
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url) #Avatar holen
                embed.set_footer(text='Ich bin ein Embed Footer')
                mess = await message.channel.send(embed = embed) #wird als Embed geschickt, nicht normaler Text
                await mess.add_reaction('😀') #Reactions hinzufügen

client.run('OTUxMjE5MDI0OTgzODk2MTA0.YikRwA.U1DGVt3pun_xFgnarf2q5giTR30')