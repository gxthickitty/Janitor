import discord
from discord import app_commands
from discord.ext import commands
import time
from datetime import datetime
import re

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.months = {
            "january": 1, "february": 2, "march": 3, "april": 4,
            "may": 5, "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12
        }
        self.date_pattern = re.compile(r"^(\d{1,2})(st|nd|rd|th)\s+([A-Za-z]+)$", re.IGNORECASE)
    
    @app_commands.command(name="help", description="Show bot information")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Janitor Bot Information",
            color=self.bot.config.embed_color
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        info = self.bot.config.bot_info
        embed.add_field(name="Developer", value=info.get('developer', 'Unknown'), inline=True)
        embed.add_field(name="Host", value=info.get('host_provider', 'Unknown'), inline=True)
        embed.add_field(name="Version", value=info.get('version', '1.0'), inline=True)
        embed.add_field(name="Description", value=info.get('description', 'A Discord bot'), inline=False)
        
        embed.add_field(
            name="Command Categories",
            value=(
                "Use `/commands` to see all available commands\n"
                "Commands are organized by category for easy access"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="commands", description="List all available commands")
    @app_commands.describe(category="Filter by category (admin/moderation/fun/info/games)")
    async def commands_list(self, interaction: discord.Interaction, category: str = None):
        command_categories = {
            "admin": {
                "Bot Management": [
                    "`/setpic` - Update bot avatar",
                    "`/setbanner` - Update bot banner",
                    "`/setusername` - Change bot username",
                    "`/setstatus` - Set custom status",
                    "`/setlog` - Configure log channel"
                ],
                "Roles": [
                    "`/clonerole` - Clone a role",
                    "`/removerole` - Delete a role"
                ]
            },
            "moderation": {
                "User Management": [
                    "`/ban` - Ban a user",
                    "`/timeout` - Timeout a user",
                    "`/removetimeout` - Remove timeout",
                    "`/mediarestrict` - Restrict media sending",
                    "`/mediaunrestrict` - Remove media restrictions"
                ],
                "Channel Management": [
                    "`/lock` - Lock a channel",
                    "`/unlock` - Unlock a channel",
                    "`/slowmode` - Set channel slowmode",
                    "`/purge` - Bulk delete messages"
                ],
                "Utility": [
                    "`/speech` - Send message as bot",
                    "`/delmsg` - Delete a specific message"
                ]
            },
            "fun": {
                "Random": [
                    "`/quote` - Get random quote from user",
                    "`/coinflip` - Flip a coin",
                    "`/8ball` - Ask the magic 8-ball",
                    "`/urban` - Urban Dictionary lookup",
                    "`/define` - Dictionary definition"
                ],
                "Interactive": [
                    "`/broomfight` - Challenge to broom fight",
                    "`/fork` - Fork duel game"
                ]
            },
            "info": {
                "User Info": [
                    "`/whois` - User information",
                    "`/duelstats` - View duel statistics",
                    "`/birthdays` - Show upcoming birthdays"
                ],
                "Bot Info": [
                    "`/ping` - Check bot latency",
                    "`/uptime` - Bot uptime",
                    "`/lyrics` - Get song lyrics"
                ]
            },
            "games": {
                "Duels": [
                    "`/rrd` - Russian Roulette duel",
                    "`/rrdleaderboard` - Duel leaderboard"
                ]
            }
        }
        
        if category and category.lower() in command_categories:
            selected = category.lower()
            embed = discord.Embed(
                title=f"{selected.capitalize()} Commands",
                description="Here are all the commands in this category:",
                color=self.bot.config.embed_color
            )
            
            for section, cmds in command_categories[selected].items():
                embed.add_field(
                    name=f"**{section}**",
                    value="\n".join(cmds),
                    inline=False
                )
        else:
            embed = discord.Embed(
                title="📜 Command Categories",
                description="Use `/commands [category]` to see specific commands",
                color=self.bot.config.embed_color
            )
            
            embed.add_field(
                name="🛠️ Admin",
                value="`/commands admin` - Bot & role management",
                inline=False
            )
            embed.add_field(
                name="🔨 Moderation",
                value="`/commands moderation` - User & channel moderation",
                inline=False
            )
            embed.add_field(
                name="🎮 Fun",
                value="`/commands fun` - Fun & interactive commands",
                inline=False
            )
            embed.add_field(
                name="ℹ️ Info",
                value="`/commands info` - Information commands",
                inline=False
            )
            embed.add_field(
                name="🎯 Games",
                value="`/commands games` - Game commands",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="whois", description="Get information about a user")
    @app_commands.describe(user="The user to lookup (member or ID)")
    async def whois(self, interaction: discord.Interaction, user: str = None):
        await interaction.response.defer()  
        if user is None:
            target = interaction.user
        else:
            target = None
            try:
                user_id = int(user.strip('<@!>'))
                try:
                    target = await self.bot.fetch_user(user_id)
                except:
                    if interaction.guild:
                        try:
                            target = await interaction.guild.fetch_member(user_id)
                        except:
                            pass
            except ValueError:
                if interaction.guild:
                    target = discord.utils.find(
                        lambda m: user.lower() in m.name.lower() or 
                                 (m.nick and user.lower() in m.nick.lower()),
                        interaction.guild.members
                    )
            
            if not target:
                return await interaction.followup.send(
                    embed=discord.Embed(
                        title="User Not Found",
                        description="Could not find that user. Try using their ID or mention.",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
        is_member = isinstance(target, discord.Member)
        
        embed = discord.Embed(
            title=f"User Information",
            color=self.bot.config.embed_color,
            timestamp=discord.utils.utcnow()
        )
        
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(
            name="👤 Username",
            value=f"{target.name}",
            inline=True
        )
        
        embed.add_field(
            name="🆔 User ID",
            value=f"`{target.id}`",
            inline=True
        )
        
        if is_member and target.nick:
            embed.add_field(
                name="📝 Nickname",
                value=target.nick,
                inline=True
            )
        
        embed.add_field(
            name="📅 Account Created",
            value=f"<t:{int(target.created_at.timestamp())}:F>\n(<t:{int(target.created_at.timestamp())}:R>)",
            inline=False
        )
        
        if is_member and target.joined_at:
            embed.add_field(
                name="📥 Server Join Date",
                value=f"<t:{int(target.joined_at.timestamp())}:F>\n(<t:{int(target.joined_at.timestamp())}:R>)",
                inline=False
            )
        
        flags = []
        public_flags = target.public_flags
        
        flag_emojis = {
            'staff': '<:staff:1234567890123456789>',
            'partner': '<:partner:1234567890123456789>',
            'hypesquad': '🏠',
            'hypesquad_bravery': '<:bravery:1234567890123456789>',
            'hypesquad_brilliance': '<:brilliance:1234567890123456789>',
            'hypesquad_balance': '<:balance:1234567890123456789>',
            'bug_hunter': '<:bug_hunter:1234567890123456789>',
            'bug_hunter_level_2': '<:bug_hunter_2:1234567890123456789>',
            'verified_bot_developer': '<:verified_dev:1234567890123456789>',
            'early_supporter': '<:early_supporter:1234567890123456789>',
            'active_developer': '<:active_dev:1234567890123456789>'
        }
        
        flag_names = {
            'staff': '🛡️ Discord Staff',
            'partner': '🤝 Partnered Server Owner',
            'hypesquad': '🏠 HypeSquad Events',
            'hypesquad_bravery': '🟣 HypeSquad Bravery',
            'hypesquad_brilliance': '🔴 HypeSquad Brilliance',
            'hypesquad_balance': '🟢 HypeSquad Balance',
            'bug_hunter': '🐛 Bug Hunter',
            'bug_hunter_level_2': '🐛 Bug Hunter Level 2',
            'verified_bot_developer': '✅ Verified Bot Developer',
            'early_supporter': '⭐ Early Supporter',
            'active_developer': '💻 Active Developer'
        }
        
        for flag_name, display_name in flag_names.items():
            if getattr(public_flags, flag_name, False):
                flags.append(display_name)
        
        if flags:
            embed.add_field(
                name="🎖️ Badges",
                value="\n".join(flags),
                inline=False
            )
        
        if target.bot:
            embed.add_field(
                name="🤖 Bot",
                value="Yes" + (" (Verified)" if public_flags.verified_bot else ""),
                inline=True
            )
        
        if is_member:
            roles = [role for role in target.roles if role.name != "@everyone"]
            if roles:
                roles.reverse()
                roles_text = ", ".join([role.mention for role in roles[:20]])
                if len(roles) > 20:
                    roles_text += f"\n... and {len(roles) - 20} more"
                embed.add_field(
                    name=f"🎭 Roles ({len(roles)})",
                    value=roles_text,
                    inline=False
                )
            
            if target.timed_out_until:
                embed.add_field(
                    name="⏰ Timed Out Until",
                    value=f"<t:{int(target.timed_out_until.timestamp())}:F>",
                    inline=False
                )
            
            if target.top_role.name != "@everyone":
                embed.color = target.top_role.color if target.top_role.color != discord.Color.default() else self.bot.config.embed_color
        
        if target.avatar:
            embed.add_field(
                name="🖼️ Avatar",
                value=f"[Link]({target.avatar.url})",
                inline=True
            )
        
        if is_member and target.guild_avatar:
            embed.add_field(
                name="🖼️ Server Avatar",
                value=f"[Link]({target.guild_avatar.url})",
                inline=True
            )
        
        try:
            full_user = await self.bot.fetch_user(target.id)
            if full_user.banner:
                embed.set_image(url=full_user.banner.url)
                embed.add_field(
                    name="🎨 Banner",
                    value=f"[Link]({full_user.banner.url})",
                    inline=True
                )
        except:
            pass
        
        embed.set_footer(
            text=f"{'Member' if is_member else 'User'} • Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="uptime", description="Show how long the bot has been running")
    async def uptime(self, interaction: discord.Interaction):
        """Display bot uptime"""
        uptime_seconds = int(time.time() - self.bot.start_time)
        start_timestamp = int(time.time() - uptime_seconds)
        
        embed = discord.Embed(
            title="🕐 Bot Uptime",
            description=f"Running since <t:{start_timestamp}:F>\nThat's <t:{start_timestamp}:R>",
            color=self.bot.config.embed_color
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Display bot latency"""
        latency_ms = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{latency_ms}ms**",
            color=self.bot.config.embed_color
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="birthdays", description="Show upcoming birthdays")
    @app_commands.describe(channel="Channel to send birthday list (admin only)")
    async def birthdays(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Show 3 closest upcoming birthdays and assign birthday role to today's celebrants"""
        guild = interaction.guild
        if not guild:
            return await interaction.response.send_message(
                "This command must be used in a server.",
                ephemeral=True
            )
        
        if channel is not None:
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Permission Denied",
                        description="Only administrators can send birthdays to a specific channel.",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
            target_channel = channel
        else:
            target_channel = interaction.channel
        
        await interaction.response.defer()
        
        today = datetime.now(datetime.now().astimezone().tzinfo).date()
        upcoming = []
        today_members = []
        
        for role in guild.roles:
            name = role.name.strip()
            m = self.date_pattern.match(name)
            if not m:
                continue
            
            day_str, _, month_name = m.groups()
            try:
                month = self.months[month_name.lower()]
                day = int(day_str)
            except (KeyError, ValueError):
                continue
            
            try:
                role_date = datetime(today.year, month, day).date()
            except ValueError:
                continue
            
            if role_date < today:
                role_date = datetime(today.year + 1, month, day).date()
            
            diff_days = (role_date - today).days
            members = role.members
            if not members:
                continue
            
            upcoming.append((role_date, diff_days, members, name))
            
            if diff_days == 0:
                today_members.extend(members)
        
        if not upcoming:
            return await interaction.followup.send(
                embed=discord.Embed(
                    title="No Birthdays Found",
                    description="No birthday roles found in this server.",
                    color=self.bot.config.embed_color
                ),
                ephemeral=True
            )
        
        upcoming.sort(key=lambda x: x[1])
        closest = upcoming[:3]
 
        embed = discord.Embed(
            title="🎂 Closest Upcoming Birthdays",
            color=self.bot.config.embed_color,
            timestamp=discord.utils.utcnow()
        )
        
        for role_date, diff, members, rolename in closest:
            dt_for_discord = datetime(
                role_date.year,
                role_date.month,
                role_date.day,
                tzinfo=datetime.now().astimezone().tzinfo
            )
            rel_ts = discord.utils.format_dt(dt_for_discord, style="R")
            label = "🎉 Today!" if diff == 0 else f"in {diff} day{'s' if diff != 1 else ''} ({rel_ts})"
            display_members = ", ".join(m.mention for m in members)
            embed.add_field(
                name=f"{rolename} — {label}",
                value=display_members,
                inline=False
            )
        await target_channel.send(
            embed=embed,
            allowed_mentions=discord.AllowedMentions.none()
        )

        if today_members:
            birthday_role_id = self.bot.config.birthday_role_id
            if birthday_role_id:
                special_role = guild.get_role(birthday_role_id)
                if special_role:
                    for member in today_members:
                        if special_role not in member.roles:
                            try:
                                await member.add_roles(
                                    special_role,
                                    reason="Birthday role assigned automatically"
                                )
                            except discord.Forbidden:
                                pass
                            except discord.HTTPException:
                                pass
        
        # Send confirmation if sent to different channel
        if channel is not None:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Birthday List Sent",
                    description=f"Sent birthday list to {target_channel.mention}",
                    color=self.bot.config.embed_color
                ),
                ephemeral=True
            )
        else:
            await interaction.delete_original_response()

async def setup(bot):
    await bot.add_cog(Info(bot))
