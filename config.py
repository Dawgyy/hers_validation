import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("token")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
