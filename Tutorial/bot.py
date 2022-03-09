import asyncio
import discord

client = discord.Client()


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

client.run('OTUxMjE5MDI0OTgzODk2MTA0.YikRwA.VfsbFybmFugNFekulEtW6p_ryu4')