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

        await self.bot.db_add_role(guild, role)

    @Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        await self.bot.wait_until_ready()

        #TODO: Can't delete roles after bot leaves server, figure out some workaround (check guild logs for who kicked me & send a message saying to delete role?)
        await self.bot.db_remove_role(guild)

    @Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()

        if role.id == await self.bot.db_get_role(role.guild):
            async for log in role.guild.audit_logs(
                action=discord.AuditLogAction.role_delete, limit=1
            ):
                with contextlib.suppress(discord.errors.Forbidden):
                    await log.user.send("hey, don't do that")

                role = await role.guild.create_role(
                    name='Chronically Online',
                    reason=f'Used by COBot (previous role was deleted by deleted by {log.user.name}).',
                )
                await self.bot.db_update_role(role.guild, role)


async def setup(bot: COBot) -> None:
    await bot.add_cog(EventsCog(bot))
