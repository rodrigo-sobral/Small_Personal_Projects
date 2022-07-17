import discord
from os import environ
from threading import Thread
from discord.ext import commands


bot = commands.Bot(command_prefix='/', case_insensitive=True)

# def __init__(self):
	# self.intents = discord.Intents.default().members(True).priv_channels(True).presences(True).messages(True)
	# self.client = discord.Client(command_prefix='!', intents=self.intents, help_command='!sch help')
	# self.client.connect(True)

@bot.command()

def connect(self) -> bool:
	self.client.connect(True)
	return self.client.is_closed()
def disconnect(self) -> bool:
	self.client.close()
	return self.client.is_closed()
def threadClient(self):
	Thread(target=self.runClient).start()
def runClient(self):
	self.client.run(environ['SCHEDULING_BOT_TOKEN'])
# @Self.client.event
# async def on_ready(self):
