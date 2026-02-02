import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import re

class Customize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Protected role IDs that cannot be customized
        self.protected_roles = [
            # EEDIT THESE FOR YOUR SERVER
            # 123456789012345678,  # Admin role
            # 234567890123456789,  # Moderator role
            # 345678901234567890,  # Member role
        ]
        self.max_custom_roles = 2
    
    def _parse_color(self, color_str: str) -> Optional[discord.Color]:
        color_str = color_str.lstrip('#').strip()
        if len(color_str) == 6:
            try:
                int(color_str, 16)
                return discord.Color(int(color_str, 16))
            except ValueError:
                pass
        if len(color_str) == 3:
            try:
                expanded = ''.join([c*2 for c in color_str])
                int(expanded, 16)
                return discord.Color(int(expanded, 16))
            except ValueError:
                pass
        
        color_names = {
            'red': discord.Color.red(),
            'blue': discord.Color.blue(),
            'green': discord.Color.green(),
            'yellow': discord.Color.yellow(),
            'orange': discord.Color.orange(),
            'purple': discord.Color.purple(),
            'pink': discord.Color.magenta(),
            'magenta': discord.Color.magenta(),
            'teal': discord.Color.teal(),
            'black': discord.Color(0x000000),
            'white': discord.Color(0xFFFFFF),
            'gold': discord.Color.gold(),
            'dark_blue': discord.Color.dark_blue(),
            'dark_green': discord.Color.dark_green(),
            'dark_red': discord.Color.dark_red(),
            'dark_purple': discord.Color.dark_magenta(),
        }
        
        return color_names.get(color_str.lower())
    
    async def _position_role_above_user_roles(
        self,
        role: discord.Role,
        member: discord.Member
    ) -> bool:
        try:
            bot_member = member.guild.get_member(self.bot.user.id)
            bot_top_position = bot_member.top_role.position
            member_roles = [r for r in member.roles if r.id != member.guild.default_role.id and r.id != role.id]
            
            if not member_roles:
                target_position = 1
            else:
                highest_role = max(member_roles, key=lambda r: r.position)
                target_position = highest_role.position + 1
            
            if target_position >= bot_top_position:
                target_position = bot_top_position - 1
            target_position = max(1, target_position)
            
            if role.position != target_position:
                await role.edit(position=target_position)
                return True
            
            return True
            
        except discord.HTTPException as e:
            print(f"Failed to position role: {e}")
            return False
        except discord.Forbidden:
            print("Bot lacks permissions to position role")
            return False
    
    async def _get_or_create_custom_role(
        self,
        member: discord.Member,
        role_to_edit: Optional[discord.Role] = None
    ) -> Optional[discord.Role]:
        if role_to_edit:
            if role_to_edit.id in self.protected_roles:
                return None
            
            if role_to_edit not in member.roles:
                return None
            
            user_custom_roles = self.bot.db.get_user_custom_roles(member.id)
            if role_to_edit.id not in [r[0] for r in user_custom_roles]:
                return None
            
            return role_to_edit
        

        user_custom_roles = self.bot.db.get_user_custom_roles(member.id)
        for role_id, _ in user_custom_roles:
            role = member.guild.get_role(role_id)
            if role and role in member.roles:
                return role

        active_custom_roles = [
            r for r in user_custom_roles 
            if member.guild.get_role(r[0]) is not None
        ]
        
        if len(active_custom_roles) >= self.max_custom_roles:
            return None
        
        try:
            new_role = await member.guild.create_role(
                name=f"{member.display_name}'s Role",
                color=discord.Color.default(),
                reason=f"Custom role created for {member}"
            )
            
            await member.add_roles(new_role)
            await self._position_role_above_user_roles(new_role, member)
            self.bot.db.add_custom_role(member.id, new_role.id)
            
            return new_role
            
        except discord.Forbidden:
            return None
        except discord.HTTPException:
            return None
    
    @app_commands.command(
        name="customize",
        description="Customize your personal role (name, color, or both)"
    )
    @app_commands.describe(
        role="Specific role to edit (leave empty to use/create your custom role)",
        name="New name for the role",
        color="Color (hex like #FF5733 or name like 'red')",
        nickname="Set your nickname at the same time"
    )
    async def customize(
        self,
        interaction: discord.Interaction,
        role: Optional[discord.Role] = None,
        name: Optional[str] = None,
        color: Optional[str] = None,
        nickname: Optional[str] = None
    ):

        if not any([role, name, color, nickname]):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Missing Parameters",
                    description=(
                        "You must provide at least one of the following:\n"
                        "• `role` - Role to customize\n"
                        "• `name` - New role name\n"
                        "• `color` - New role color\n"
                        "• `nickname` - New nickname\n\n"
                        "**Examples:**\n"
                        "`/customize name:Cool Person color:#FF5733`\n"
                        "`/customize nickname:Bob color:blue`\n"
                        "`/customize role:@MyRole name:New Name`"
                    ),
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        await interaction.response.defer(ephemeral=True)
        
        member = interaction.user
        changes_made = []
        
        if nickname:
            try:
                await member.edit(nick=nickname)
                changes_made.append(f"✅ Nickname set to **{nickname}**")
            except discord.Forbidden:
                changes_made.append("❌ Failed to change nickname (missing permissions)")
            except discord.HTTPException as e:
                changes_made.append(f"❌ Failed to change nickname: {str(e)}")
        
        if name or color or role:
            custom_role = await self._get_or_create_custom_role(member, role)
            
            if not custom_role:
                if role and role.id in self.protected_roles:
                    return await interaction.followup.send(
                        embed=discord.Embed(
                            title="Protected Role",
                            description="This role cannot be customized as it's protected by the bot.",
                            color=discord.Color.red()
                        ),
                        ephemeral=True
                    )
                elif role and role not in member.roles:
                    return await interaction.followup.send(
                        embed=discord.Embed(
                            title="Invalid Role",
                            description="You don't have this role!",
                            color=discord.Color.red()
                        ),
                        ephemeral=True
                    )
                elif self.bot.db.count_user_custom_roles(member.id) >= self.max_custom_roles:
                    return await interaction.followup.send(
                        embed=discord.Embed(
                            title="Custom Role Limit Reached",
                            description=(
                                f"You can only have **{self.max_custom_roles}** custom roles.\n"
                                "Contact an admin to remove one of your existing custom roles."
                            ),
                            color=discord.Color.red()
                        ),
                        ephemeral=True
                    )
                else:
                    return await interaction.followup.send(
                        embed=discord.Embed(
                            title="Error",
                            description="Failed to get or create custom role. Bot may lack permissions.",
                            color=discord.Color.red()
                        ),
                        ephemeral=True
                    )
            
            role_changes = {}
            
            if name:
                role_changes['name'] = name
                changes_made.append(f"✅ Role name set to **{name}**")
            
            if color:
                parsed_color = self._parse_color(color)
                if parsed_color:
                    role_changes['color'] = parsed_color
                    hex_value = f"#{parsed_color.value:06X}"
                    changes_made.append(f"✅ Role color set to **{hex_value}**")
                else:
                    changes_made.append(
                        f"❌ Invalid color: `{color}`\n"
                        "   Use hex format (e.g., `#FF5733` or `FF5733`) or color names (e.g., `red`, `blue`)"
                    )
            
            if role_changes:
                try:
                    await custom_role.edit(**role_changes)
                    await self._position_role_above_user_roles(custom_role, member)
                except discord.HTTPException as e:
                    changes_made.append(f"❌ Failed to edit role: {str(e)}")
        
        if changes_made:
            embed = discord.Embed(
                title="🎨 Customization Complete",
                description="\n".join(changes_made),
                color=self.bot.config.embed_color
            )
            if name or color:
                user_roles = self.bot.db.get_user_custom_roles(member.id)
                if user_roles:
                    embed.add_field(
                        name="Your Custom Roles",
                        value=f"{len(user_roles)}/{self.max_custom_roles} slots used",
                        inline=False
                    )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="No Changes Made",
                    description="No changes were applied.",
                    color=discord.Color.orange()
                ),
                ephemeral=True
            )
    
    @app_commands.command(
        name="mycustomroles",
        description="View your custom roles and their status"
    )
    async def my_custom_roles(self, interaction: discord.Interaction):
        user_roles = self.bot.db.get_user_custom_roles(interaction.user.id)
        
        if not user_roles:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Custom Roles",
                    description=(
                        f"You don't have any custom roles yet!\n"
                        f"Use `/customize` to create one."
                    ),
                    color=self.bot.config.embed_color
                ),
                ephemeral=True
            )
        
        embed = discord.Embed(
            title="🎨 Your Custom Roles",
            description=f"You have {len(user_roles)}/{self.max_custom_roles} custom role slots used.",
            color=self.bot.config.embed_color
        )
        
        for role_id, created_at in user_roles:
            role = interaction.guild.get_role(role_id)
            if role:
                embed.add_field(
                    name=role.name,
                    value=(
                        f"**Color:** {role.color}\n"
                        f"**Members:** {len(role.members)}\n"
                        f"**Created:** <t:{created_at}:R>"
                    ),
                    inline=True
                )
            else:
                embed.add_field(
                    name="Deleted Role",
                    value=f"Role ID: {role_id}\n*(Role no longer exists)*",
                    inline=True
                )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Customize(bot))
