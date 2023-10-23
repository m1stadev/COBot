from typing import Optional

import asqlite
from discord import AllowedMentions, Guild, Object, Role
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
            allowed_mentions=AllowedMentions.none(),
            *args,
            **kwargs
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
            guild = Object(id=self._admin_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def get_role_from_db(self, guild: Guild) -> Optional[Role]:
        await self.db.execute('SELECT role FROM roles WHERE guild = ?', (guild.id,))
        data = await self.db.fetchone()

        if len(data) == 0:
            return None

        return guild.get_role(data[0])


#    async def update_role_db(self, guild: Guild, role: Role) -> None:
#        await self.db.execute('UPDATE roles WHERE guild = ?', (guild.id,))
#        data = await self.db.fetchone()
#
#        if len(data) == 0:
#            return None
#
#        return guild.get_role(data[0])
