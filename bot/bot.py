import os
import random
import discord
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from util import privileges

from aws import util
from util import messages

load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('SHR1MP'))
    print('Logged in as')
    print('Name: {}'.format(client.user.name))
    print('ID: {}'.format(client.user.id))
    print('------------')
    factorio_channel = await messages.clear_factorio_text_channel(client)
    if factorio_channel is not None:
        await messages.factorio_status_message(factorio_channel)


@client.event
async def on_member_join(member):
    print(f'{member} joined the SHR1MP Clan!')


@client.event
async def on_member_remove(member):
    print(f'{member} left the SHR1MP Clan...')


# Error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await messages.perror(ctx, "Invalid command used")


@client.command()
async def shrimp(ctx):
    await ctx.send(f'shromp (latency: {round(client.latency * 1000)} ms)')


@client.command(aliases=['8ball', 'przepowiednia'])
async def _8ball(ctx, *, question):
    responses = ['+1 byczku',
                 '+0.7 byczku',
                 'Si si toro',
                 'To jest niemozliwe do przewidzenia',
                 'Ooooj tak',
                 'Nie ma chuja',
                 'Ta ta jasne',
                 'We zapytaj jeszcze raz',
                 'Matematyczna szansa']
    await ctx.send(f'{random.choice(responses)}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number: int):
    await messages.clear(ctx, number + 1)


# Error handling for clear (when there will be no specified int value given)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('This command requires additional information.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use this command")


@client.command()
@commands.check(privileges.nuke_priv)
async def nuke(ctx):
    await messages.reset_channel(ctx)


# LOADING / UNLOADING COGS

@client.command()
async def load(extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

###########################################################

client.run(TOKEN)
