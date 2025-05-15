import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🛰️")

bot.run(TOKEN)


@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=os.getenv("testing_Guild")))  # replace with your test guild ID
    print(f"Synced slash commands to dev guild.")
