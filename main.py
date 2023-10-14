import asyncio
from pydoc import cli
from re import M
import discord 
from discord import client
from discord import member
from discord import message
from discord import channel
from discord.ext import commands
from discord import app_commands
import string, json
import os, sqlite3
from discord.ext.commands import bot
from discord.flags import Intents
import json
import random
import os
#from dotenv import load_dotenv
#from webserver import keep_alive

# !test ( Префикс у команд )
client = commands.Bot( command_prefix = '!', intents = discord.Intents.all())
# Оповещение в консоли, что бот присоединился
@client.event
async def on_ready():
    print('Бот подключился к серверу')
    try : 
        synced = await client.tree.sync()
        print(f"Синхронизированно {len(synced)} команд")
    except Exception as e:
        print(e)

# Очистка чата для администратора + кол-во сообщений
@client.command( pass_context = True)
@commands.has_permissions( administrator = True )
async def очистить( ctx, amount = 100 ):
    await ctx.channel.purge(limit = amount + 1)

# Автовыдача роли, при присоединении на сервер
@client.event
async def on_member_join(member):
    for ch in client.get_guild(member.guild.id).channels:
        if ch.name == "приветствие":
            await client.get_channel(ch.id).send(f"{member.mention} будь как дома. Сначала загляни сюды: <#859764991489081374>")
            role = discord.utils.get(member.guild.roles, name="Гост")#Название РОЛИ
            await member.add_roles(role)


# Удаление Мата
@client.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.content.split(' ')}.intersection(set(json.load(open('badwords.json')))) != set():
        author = message.author
        await message.channel.send(f'{author.mention}, шыть отседа')
        await message.delete()
    await client.process_commands(message)


# ephemeral — True / False  Только 1 пользователь видит
# Слэш команды
@client.tree.command(name="привет", description=str("Выводит приветствие"))
async def hello(interaction: discord.Interaction):
 await interaction.response.send_message(f"Дарова {interaction.user.mention}", ephemeral = False)

@client.tree.command(name="монета", description=str("Орёл или Решка"))
async def moneta(interaction: discord.Interaction):
    number = random.randint(1,2)
    if number == 1:
        await interaction.response.send_message(f"{interaction.user.mention}, ОрЁль!", ephemeral=False)
    if number == 2:
        await interaction.response.send_message(f"{interaction.user.mention}, оРешка!", ephemeral=False)


############### ВЫДАЧА РОЛИ ПО ЭМОДЗИ
@client.event
async def reaction_add(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.client:
        return
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = client.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.bot:
        return
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = client.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)
                role1 = discord.utils.get(guild.roles, name="Гост")
                await payload.member.remove_roles(role1)

@client.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(
                emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = client.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                member = await(guild.fetch_member(payload.user_id))
                if member is not None:
                    await member.remove_roles(role)
                    role1 = discord.utils.get(member.guild.roles, name="Гост")
                    await member.add_roles(role1)


#load_dotenv()
#keep_alive()
client.run(os.environ["DISCORD_TOKEN"])