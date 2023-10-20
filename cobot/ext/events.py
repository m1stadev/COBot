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
        for role in guild.roles:
            if role.name.casefold() == 'chronically online':
                await role.delete(
                    reason="Removing any previous role created by COBot (that wasn't deleted for some reason?)"
                )

        await guild.create_role(
            name='Chronically Online', reason='Required for COBot to function.'
        )

    @Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        if role.name.casefold() == 'chronically online':
            async for log in role.guild.audit_logs(
                action=discord.AuditLogAction.role_delete, limit=1
            ):
                with contextlib.suppress(discord.errors.HTTPException):
                    await log.user.send("hey, don't do that")
                await role.guild.create_role(
                    name='Chronically Online', reason='Required for COBot to function.'
                )

    @Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        if role.name.casefold() == 'chronically online':
            async for log in role.guild.audit_logs(
                action=discord.AuditLogAction.role_create, limit=1
            ):
                if log.user == self.bot.user:
                    return

                with contextlib.suppress(discord.errors.HTTPException):
                    await log.user.send("hey, don't do that")
                await role.delete()


async def setup(bot: COBot) -> None:
    await bot.add_cog(EventsCog(bot))
