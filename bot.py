import os
import discord
import random
import time
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("TESTING_GUILD"))
testroleid = int(os.getenv("TESTING_ROLE"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)  # commands.when_mentioned_or("!") is used to make the bot respond to !ping and @bot ping

async def setup_hook() -> None:  # This function is automatically called before the bot starts
    await bot.tree.sync()   # This function is used to sync the slash commands with Discord it is mandatory if you want to use slash commands

bot.setup_hook = setup_hook  # Not the best way to sync slash commands, but it will have to do for now. A better way is to create a command that calls the sync function.

@bot.event
async def on_ready() -> None:  # This event is called when the bot is ready
    print(f"Logged in as {bot.user}")

@bot.tree.command()
async def ping(inter: discord.Interaction) -> None:
    await inter.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command()
async def testalert(inter: discord.Interaction) -> None:
    """Send a test alert with a delay and timestamp"""
    await inter.response.send_message("Preparing test alert... ⏳")

    await asyncio.sleep(5)

    future_timestamp = int(time.time()) + 3600  # 1 hour from now
    timestamp_text = f"<t:{future_timestamp}:F>"  # Full datetime style

    embed = discord.Embed(
        title="⚠️ Structure Fuel Low",
        description=(
            "This is a test alert to demonstrate @everyone pings.\n\n"
            f"Estimated fuel depletion time: {timestamp_text} local time."
        ),
        color=discord.Color.red()
    )
    await inter.followup.send(
        content="@everyone",
        embed=embed,
        allowed_mentions=discord.AllowedMentions(everyone=True)
    )


@bot.tree.command(name="testalertrole")
async def testalertrole(inter: discord.Interaction) -> None:
    """Send a test alert mentioning a specific role"""
    await inter.response.send_message("Preparing role-based alert... ⏳")

    await asyncio.sleep(5)

    # Get the test role ID from .env or hardcode it
    TEST_ROLE_ID = testroleid

    future_timestamp = int(time.time()) + 3600
    timestamp_text = f"<t:{future_timestamp}:R>"  # e.g., "in 1 hour"

    role_mention = f"<@&{TEST_ROLE_ID}>"

    embed = discord.Embed(
        title="⛽ Structure Fuel Low",
        description=(
            f"{role_mention}\n"
            "This is a test structure fuel alert using a role mention.\n\n"
            f"Estimated fuel depletion: {timestamp_text}"
        ),
        color=discord.Color.orange()
    )

    await inter.followup.send(
        content=role_mention,
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )

bot.run(TOKEN)