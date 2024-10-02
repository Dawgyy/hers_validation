import os
from config import bot, TOKEN


async def load_cogs():
    """
    Loads all the command cogs from the 'cogs' directory.

    Cogs are modular extensions that contain groups of commands, and this function
    dynamically loads them at runtime so the bot can use them.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def load_events():
    """
    Loads all the event listeners from the 'events' directory.

    Events are triggers that the bot can respond to, such as messages or reactions,
    and this function dynamically loads them to handle various events during runtime.
    """
    for filename in os.listdir("./events"):
        if filename.endswith(".py"):
            await bot.load_extension(f"events.{filename[:-3]}")


@bot.event
async def on_ready():
    """
    Event handler called when the bot is ready.

    This function is triggered when the bot has successfully connected to Discord.
    It loads the command cogs and event listeners, and syncs the application commands
    (like slash commands) with Discord.
    """
    print(f"Connected: {bot.user}")
    await load_cogs()
    await load_events()
    await bot.tree.sync()


bot.run(TOKEN)
