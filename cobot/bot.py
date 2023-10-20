from typing import Optional

from discord import AllowedMentions, Object
from discord.ext import commands


class COBot(commands.Bot):
    def __init__(
        self,
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

        if extensions is None:
            self.init_extensions = []
        else:
            self.init_extensions = extensions

        self.admin_guild_id = admin_guild_id

    async def setup_hook(self) -> None:
        for ext in self.init_extensions:
            await self.load_extension(ext)

        if self.admin_guild_id is not None:
            guild = Object(id=self.admin_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
