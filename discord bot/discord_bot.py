import discord
import re
import json
import twitch_api as twitch

from discord.ext import commands

def load_messages():
    with open("messages.json", "r") as file:
        data = json.load(file)

    return data

# For Discord Bot
DISCORD_TOKEN = 'YOUR DISCORD TOKEN'
list_of_guilds = {}
messages = load_messages()

client = commands.Bot(command_prefix="!")
client.remove_command('help')


# Functions for Discord API
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('!help | !commands'))
    async for guild in client.fetch_guilds():
        list_of_guilds[guild.name] = [] # initialize to empty list

    print('Bot is ready')


@client.command()
async def help(context):
    await context.send('\n'.join(messages['help']))


@client.command()
async def commands(context):
    await context.send('```{}```'.format('\n'.join(messages['commands'])))


@client.command()
async def add(context, *args):
    guild_name = context.guild.name
    message_list = []
    message = '\n'

    if len(args) == 0:
        await context.send('```You didn\'t specify a streamer.```')
        return

    if len(args) >= 1:
        for name in args:
            list_of_guilds[guild_name].append(name)
            message_list.append('Added "{0}" to the list.'.format(name))

        message += message.join(message_list)
        await context.send('```' + message + '```')


@client.command()
async def remove(context, *args):
    guild_name = context.guild.name
    message_list = []
    message = '\n'

    if len(args) == 0:
        await context.send('```You didn\'t specify a streamer.```')
        return

    if len(args) >= 1:
        for name in args:
            list_of_guilds[guild_name].remove(name)
            message_list.append('Removed "{0}" from the list.'.format(name))

        message += message.join(message_list)
        await context.send('```' + message + '```')


@client.command()
async def remove_all(context):
    guild_name = context.guild.name
    list_of_guilds[guild_name].clear()
    await context.send('```Removed all streamers from list```')


@client.command()
async def list(context):
    guild_name = context.guild.name
    message_list = []
    message = '\n'

    if len(list_of_guilds[guild_name]) == 0:
        await context.send('```There are no streamers in the list.```')
        return

    for streamer in list_of_guilds[guild_name]:
        message_list.append('{0}'.format(streamer))

    message += message.join(message_list)
    await context.send('```' + message + '```')


async def make_embed(context, item):
    embed = discord.Embed(title="https://www.twitch.tv/{}".format(item['user_name']), url="https://www.twitch.tv/{}".format(item['user_name']), color=0x8000ff)
    embed.set_author(name="{} is live!".format(item['user_name']))
    embed.set_thumbnail(url=item['thumbnail_url'].format(width=1000, height=800))
    embed.add_field(name="{}".format(item['title']), value="{} is {} with {} viewers!".format(item['user_name'], item['type'], item['viewer_count']), inline=False)
    embed.add_field(name="Playing", value="{}".format(twitch.get_game_title(item['game_id'])), inline=True)
    embed.add_field(name="Started", value="{}".format(item['started_at']), inline=True)
    return embed


@client.command()
async def live(context):
    guild_name = context.guild.name
    streamer_info = twitch.get_streamer_info(list_of_guilds[guild_name])
    message_list = []
    message = '\n'
    embed = []

    for counter, data in enumerate(streamer_info):
        dataIsEmpty = not bool(data['data'])
        if dataIsEmpty:
            message_list.append('{} is not live'.format(list_of_guilds[guild_name][counter]))
            continue
        for item in data['data']:
            embed = await make_embed(context, item)
            await context.send(embed=embed)

    message += message.join(message_list)
    await context.send('```' + message + '```')


client.run(DISCORD_TOKEN)