import asyncio
import discord
from discord import Member
from discord import Guild
from discord import User
import random

#Bot auf Server einladen
#AppId kopieren => https://melion.cloud/gen/

#Variablen
client = discord.Client(intents=discord.Intents.all())
antworten = ['Ja', 'Nein', 'Vielleicht', 'Eines Tages vielleicht', 'Frag doch einfach nochmal']
autoroles = {
    950881678606336061: {'memberroles': [953055172916023356, 953055416512811028], 'botroles': [953055416512811028]},

}

@client.event
async def on_ready():
    print('Ich bin eingeloggt als User: {}'.format(client.user.name))
    client.loop.create_task(status_task())

async def status_task():
    colors = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(), discord.Colour.blue(), discord.Colour.purple()]

    #Status vom Bot selbst + Farbe vom Bot
    while True:
        await client.change_presence(activity=discord.Game('mit Hulong'), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('mit dem Code'), status=discord.Status.online)
        await asyncio.sleep(5)
        guild: Guild = client.get_guild(950881678606336061)
        if guild: #wenn guild existiert
            role = guild.get_role(951558503938523266)
            if role: #wenn rolle existiert
                if role.position < guild.get_member(client.user.id).top_role.position:
                    await role.edit(colour = random.choice(colors)) #farbe der rolle ändert sich



def is_not_pinned(mess):
    return not mess.pinned #schaut ob Message angepinnt ist + schickt Gegenteil zurück

#Willkommensnachricht
@client.event
async def on_member_join(member):
    guild: Guild = member.guild

    if not member.bot:
        embed = discord.Embed(title = 'Willkommen {} Bratan!'.format(member.name), description = 'Wir heißen dich herzlich willkommen!', color = 0X22A7F0) #Nachricht
        try:
            if not member.dm_channel: #wenn noch kein Privatchannel => erstelle ein
                await member.create_dm()
            await member.dm_channel.send(embed = embed)
            
        except discord.errors.Forbidden: #wenn Dm bei dem aus ist
            print('Es konnte keine Willkommensnachricht an {} gesendet werden.'.format(member.name))
        
        autoguild = autoroles.get(guild.id)
        if autoguild and autoguild['memberroles']: #wenn guild und memberroles gibt
            for roleId in autoguild['memberroles']: #geht über alle in memberroles
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason = 'AutoRoles', atomic = True)

    else:
        autoguild = autoroles.get(guild.id)
        if autoguild and autoguild['botroles']:
            for roleId in autoguild['botroles']:
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason = 'AutoRoles', atomic = True)

@client.event
async def on_message(message):
    if message.author.bot: #Wenn User ein Bot ist
        return
    #await message.channel.send('Du nervst mit dieser Nachricht: {}'.format(message.content))

    #Hilfe anzeigen
    if '!help' in message.content:
        await message.channel.send('**Hilfe zum PythonBot**\r\n'
                                    '!help - Zeigt diese Hilfe an')
    
    #Ban
    if message.content.startswith('!ban') and message.author.guild_permissions.ban_member:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.ban()
                await message.channel.send(f'Member {member.name} gebannt.')
            else:
                await message.channel.send(f'Kein User mit dem Namen {args[1]} gefunden.')

    #Kick
    if message.content.startswith('!kick') and message.author.guild_permissions.kick_member:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.kick()
                await message.channel.send(f'Member {member.name} gekickt.')
            else:
                await message.channel.send(f'Kein User mit dem Namen {args[1]} gefunden.')
    
    #Unban
    if message.content.startswith('!unban') and message.author.guild_permissions.kick_member:
        args = message.content.split(' ')
        if len(args) == 2:
            user: User = discord.utils.find(lambda banentry: args[1] in banentry.user.name, await message.guild.bans()).user
            if user:
                await message.guild.unban(user)
                await message.channel.send(f'User {user.name} entbannt.')
            else:
                await message.channel.send(f'Kein User mit dem Namen {args[1]} gefunden.')

    #Userinfo anzeigen (Name, Rollen, Datum)
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

    #Letzten Nachrichten mit Anzahl löschen
    if message.content.startswith('!clear'):
        if message.author.permissions_in(message.channel).manage_messages: #schauen ob user löschen darf
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit(): #wenn 2. ist eine Zahl
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('{} Nachrichten gelöscht.'.format(len(deleted) - 1))

    #Magische Miesmuschel
    if message.content.startswith('!magischemiesmuschel'):
        args = message.content.split(' ')
        if len(args) >= 2:
            frage = ' '.join(args[1:]) #beginnt bei 1 (Wie) + nimmt den Rest der Frage
            mess = await message.channel.send('Ich versuche deine Frage `{0}` zu beantworten.'.format(frage))
            await asyncio.sleep(2)
            await mess.edit(content = 'Ich kontaktiere die magische Miesmuschel...')
            await asyncio.sleep(2)
            await mess.edit(content = 'Deine Antwort zur Frage `{0}` lautet: `{1}`'.format(frage, random.choice(antworten)))

client.run('')