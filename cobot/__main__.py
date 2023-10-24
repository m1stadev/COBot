import asyncio
import logging
from os import getenv

import asqlite
import coloredlogs
from aiopath import AsyncPath
from discord import Intents
from dotenv import load_dotenv

from cobot.bot import COBot

load_dotenv()

coloredlogs.install(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Make this configurable (CLI option?)
DB_PATH = 'roles.db'


async def _main():
    intents = Intents(guilds=True, members=True, guild_messages=True)
    async with asqlite.connect(AsyncPath(DB_PATH)) as db:
        await db.execute(
            '''
            CREATE TABLE IF NOT EXISTS roles(
            guild INTEGER,
            role INTEGER
            )
            '''
        )
        await db.commit()

        async with COBot(
            db=db,
            intents=intents,
            # admin_guild_id=729946499102015509,
            extensions=['cobot.ext.events', 'cobot.ext.cmds'],
        ) as bot:
            await bot.start(token=getenv('COBOT_TOKEN'))


def main():
    asyncio.run(_main())
