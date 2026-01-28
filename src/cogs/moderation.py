import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from utils.helpers import parse_duration, is_admin
import io

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.describe(
        user="User to ban",
        duration="Duration (e.g. 1d, 2w, 1m)",
        reason="Reason for ban",
        delete_days="Days of messages to delete (0 or 7)"
    )
    @app_commands.check(is_admin)
    async def ban(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        duration: str = None,
        reason: str = None,
        delete_days: int = 0
    ):
        try:
            await interaction.guild.fetch_ban(user)
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Already Banned",
                    description=f"{user.mention} is already banned.",
                    color=self.bot.config.embed_color
                ),
                ephemeral=True
            )
        except discord.NotFound:
            pass
        
        until = None
        if duration:
            delta = parse_duration(duration)
            if delta:
                until = discord.utils.utcnow() + delta
        
        await interaction.guild.ban(
            user,
            reason=reason,
            delete_message_days=min(delete_days, 7)
        )
        
        embed = discord.Embed(title="User Banned", color=self.bot.config.embed_color)
        
        if until:
            embed.description = f"{user.mention} banned until <t:{int(until.timestamp())}:F>"
        else:
            embed.description = f"{user.mention} permanently banned"
        
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="timeout", description="Timeout a user")
    @app_commands.describe(
        user="User to timeout",
        duration="Duration (e.g. 30min, 2h, 1d)",
        reason="Reason for timeout"
    )
    @app_commands.check(is_admin)
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        duration: str = "1h",
        reason: str = None
    ):
        delta = parse_duration(duration)
        if not delta:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid Duration",
                    description="Use format like: 30min, 2h, 1d",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        timeout_until = discord.utils.utcnow() + delta
        await user.timeout(timeout_until, reason=reason)
        
        embed = discord.Embed(
            title="User Timed Out",
            description=f"{user.mention} until <t:{int(timeout_until.timestamp())}:F>",
            color=self.bot.config.embed_color
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="removetimeout", description="Remove timeout from a user")
    @app_commands.describe(user="User to remove timeout from")
    @app_commands.check(is_admin)
    async def removetimeout(self, interaction: discord.Interaction, user: discord.Member):
        """Remove timeout from a user"""
        if not user.is_timed_out():
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description=f"{user.mention} is not timed out.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        await user.timeout(None)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Timeout Removed",
                description=f"Timeout removed from {user.mention}",
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="lock", description="Lock a channel")
    @app_commands.describe(channel="Channel to lock")
    @app_commands.check(is_admin)
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Lock a channel to prevent messages"""
        target = channel or interaction.channel
        await target.set_permissions(interaction.guild.default_role, send_messages=False)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"🔒 {target.mention} Locked",
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="unlock", description="Unlock a channel")
    @app_commands.describe(channel="Channel to unlock")
    @app_commands.check(is_admin)
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Unlock a channel"""
        target = channel or interaction.channel
        await target.set_permissions(interaction.guild.default_role, send_messages=True)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"🔓 {target.mention} Unlocked",
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="slowmode", description="Set channel slowmode")
    @app_commands.describe(
        channel="Channel to modify",
        seconds="Slowmode delay in seconds (0 to disable)"
    )
    @app_commands.check(is_admin)
    async def slowmode(
        self,
        interaction: discord.Interaction,
        seconds: int,
        channel: discord.TextChannel = None
    ):
        """Set slowmode for a channel"""
        target = channel or interaction.channel
        
        try:
            await target.edit(slowmode_delay=seconds)
            
            if seconds == 0:
                msg = f"Slowmode disabled in {target.mention}"
            else:
                msg = f"Slowmode set to {seconds}s in {target.mention}"
            
            await interaction.response.send_message(
                embed=discord.Embed(title=msg, color=self.bot.config.embed_color)
            )
        except discord.HTTPException:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Failed to set slowmode",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="purge", description="Bulk delete messages")
    @app_commands.describe(
        amount="Number of messages to delete (max 350)",
        user="Only delete messages from this user"
    )
    @app_commands.check(is_admin)
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: int,
        user: discord.Member = None
    ):
        if not 1 <= amount <= self.bot.config.purge_max:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid Amount",
                    description=f"Amount must be between 1 and {self.bot.config.purge_max}",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        await interaction.response.defer(ephemeral=True)
        
        def check(m):
            if user:
                return m.author == user
            return True
        
        deleted = await interaction.channel.purge(limit=amount, check=check)
        log_channel_id = self.bot.config.log_channel_id
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                log_content = "\n".join(
                    f"[{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{msg.author.display_name}: {msg.clean_content}"
                    for msg in reversed(deleted)
                )
                
                embed = discord.Embed(
                    title="Purge Log",
                    description=(
                        f"**Moderator:** {interaction.user.mention}\n"
                        f"**Channel:** {interaction.channel.mention}\n"
                        f"**Messages Deleted:** {len(deleted)}"
                    ),
                    color=self.bot.config.embed_color,
                    timestamp=datetime.utcnow()
                )
                
                try:
                    await log_channel.send(
                        embed=embed,
                        file=discord.File(
                            io.StringIO(log_content),
                            filename=f"purge_{interaction.channel.name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
                        )
                    )
                except:
                    pass
        
        await interaction.followup.send(
            embed=discord.Embed(
                title="Messages Purged",
                description=f"Deleted {len(deleted)} message(s)",
                color=self.bot.config.embed_color
            ),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
