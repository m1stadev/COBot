import asyncio
from os import getenv

import asqlite
from aiopath import AsyncPath
from discord import Intents
from dotenv import load_dotenv

from cobot.bot import COBot

load_dotenv()

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
            # admin_guild_id=842189018523631658,
            extensions=['cobot.ext.events'],
        ) as bot:
            bot.start(token=getenv('COBOT_TOKEN'))


def main():
    asyncio.run(_main())
