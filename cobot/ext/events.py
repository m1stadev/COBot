import contextlib

import discord
from discord.ext.commands import Cog

from cobot.bot import COBot


class EventsCog(Cog):
    def __init__(self, bot: COBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        await self.bot.wait_until_ready()
        try:
            role = await guild.create_role(
                name='Chronically Online', reason='Used by COBot.'
            )
        except discord.errors.Forbidden:  # Invited with incorrect permissions
            await guild.leave()

        await self.bot.db.execute(
            'INSERT INTO roles(guild, role) VALUES(?, ?)', (guild.id, role.id)
        )
        await self.bot.db.commit()

    # TODO: Can't delete roles after bot leaves server, figure out some workaround (check guild logs for who kicked me & send a message saying to delete role?)
    @Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        await self.bot.wait_until_ready()
        await self.bot.get_role_from_db(guild).delete(reason='Bot left server.')

    @Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        if role.name.casefold() == 'chronically online':
            async for log in role.guild.audit_logs(
                action=discord.AuditLogAction.role_delete, limit=1
            ):
                with contextlib.suppress(discord.errors.Forbidden):
                    await log.user.send("hey, don't do that")

                await role.guild.create_role(
                    name='Chronically Online', reason='Required for COBot to function.'
                )


async def setup(bot: COBot) -> None:
    await bot.add_cog(EventsCog(bot))
