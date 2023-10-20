from os import getenv

from discord import Intents
from dotenv import load_dotenv

from cobot.bot import COBot

load_dotenv()


def main():
    intents = Intents(guilds=True, members=True, guild_messages=True)
    bot = COBot(
        intents=intents,
        admin_guild_id=842189018523631658,
        extensions=['cobot.ext.events'],
    )
    bot.run(token=getenv('COBOT_TOKEN'))
