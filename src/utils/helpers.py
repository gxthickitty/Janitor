import discord
from typing import Optional
import re
from datetime import timedelta

async def get_user(ctx, user_input: str) -> Optional[discord.Member]:
    try:
        if user_input.startswith('<@') and user_input.endswith('>'):
            user_id = int(user_input[2:-1].replace('!', ''))
            return await ctx.guild.fetch_member(user_id)
        
        if user_input.isdigit():
            return await ctx.guild.fetch_member(int(user_input))
        
        return discord.utils.find(
            lambda m: user_input.lower() in m.name.lower() or 
                     (m.nick and user_input.lower() in m.nick.lower()),
            ctx.guild.members
        )
    except:
        return None

def parse_duration(duration_str: str) -> Optional[timedelta]:
    match = re.match(r'^(\d+)(min|h|d|w|m|y)$', duration_str.lower())
    if not match:
        return None
    
    amount = int(match.group(1))
    unit = match.group(2)
    
    multipliers = {
        'min': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800,
        'm': 2592000,
        'y': 31536000
    }
    
    if unit not in multipliers:
        return None
    
    return timedelta(seconds=amount * multipliers[unit])

def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        days = seconds // 86400
        return f"{days} day{'s' if days != 1 else ''}"

async def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.administrator
