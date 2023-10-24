import contextlib
from typing import Optional

import asqlite
import discord
from discord.ext import commands


class COBot(commands.Bot):
    def __init__(
        self,
        db: asqlite.Connection,
        extensions: Optional[list[str]] = None,
        admin_guild_id: Optional[int] = None,
        *args,
        **kwargs
    ):
        super().__init__(
            commands.when_mentioned,
            allowed_mentions=discord.AllowedMentions(roles=True),
            *args,
            **kwargs,
        )

        self.db = db

        self._init_extensions = ['jishaku']
        if extensions is not None:
            self._init_extensions += extensions

        self._admin_guild_id = admin_guild_id

    async def setup_hook(self) -> None:
        for ext in self._init_extensions:
            await self.load_extension(ext)

        if self._admin_guild_id is not None:
            guild = discord.Object(id=self._admin_guild_id)
            self.tree.copy_global_to(guild=guild)
            with contextlib.suppress(discord.errors.Forbidden):
                await self.tree.sync(guild=guild)

    async def db_get_role(self, guild: discord.Guild) -> Optional[discord.Role]:
        data = await self.db.fetchone(
            'SELECT role FROM roles WHERE guild = ?', (guild.id,)
        )

        if data is None:
            return None
        else:
            return guild.get_role(data[0])

    async def db_update_role(self, guild: discord.Guild, role: discord.Role) -> None:
        if role.guild != guild:
            pass  # TODO: Error

        await self.db.execute(
            'UPDATE roles SET role = ? WHERE guild = ?',
            (
                role.id,
                guild.id,
            ),
        )
        await self.db.commit()

    async def db_remove_role(self, guild: discord.Guild) -> None:
        await self.db.execute('DELETE FROM roles WHERE guild = ?', (guild.id,))
        await self.db.commit()

    async def db_add_role(self, guild: discord.Guild, role: discord.Role) -> None:
        if role.guild != guild:
            pass  # TODO: error

        await self.db.execute(
            'INSERT INTO roles(guild, role) VALUES(?, ?)', (guild.id, role.id)
        )
        await self.db.commit()
