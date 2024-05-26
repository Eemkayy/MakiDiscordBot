import discord
from discord.ext import commands
import requests
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

LIBRETRANSLATE_URL = "https://libretranslate.de/translate"


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def translate(ctx, *args):
    """
    Translates a given sentence to the specified language using LibreTranslate API.
    Usage: !translate <target_language_code> <sentence>
    Example: !translate es Hello, how are you?
    """
    if len(args) == 0:
        await ctx.send("""Usage of the command: 
        !translate <target_language_code> <sentence>

        Note: source language is only English as of right now""")
        return

    if len(args) == 1 and args[0].lower() == "help":
        await ctx.send("""
        Available languages:
        Arabic (ar)
        Chinese (zh)
        Czech (cs)
        Dutch (nl)
        English (en)
        Esperanto (eo)
        Finnish (fi)
        French (fr)
        German (de)
        Greek (el)
        Hebrew (he)
        Hindi (hi)
        Hungarian (hu)
        Indonesian (id)
        Irish (ga)
        Italian (it)
        Japanese (ja)
        Korean (ko)
        Persian (fa)
        Polish (pl)
        Portuguese (pt)
        Russian (ru)
        Spanish (es)
        Swedish (sv)
        Turkish (tr)
        Ukrainian (uk)
        Vietnamese (vi)
        """)
        return

    if len(args) < 2:
        await ctx.send("Usage: !translate <target_language_code> <sentence>")
        return

    target = args[0]
    sentence = " ".join(args[1:])

    try:
        payload = {
            "q": sentence,
            "source": "en",
            "target": target,
            "format": "text"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(LIBRETRANSLATE_URL,
                                 data=payload,
                                 headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            await ctx.send(f"Error: {response_data['error']['message']}")
            return

        translated_text = response_data['translatedText']
        await ctx.send(translated_text)
    except Exception as e:
        await ctx.send(f'Error: {e}')


token = os.getenv('DISCORD_BOT_TOKEN')

if token:
    bot.run(token)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable is not set.")
