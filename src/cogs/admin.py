import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import is_admin

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setlog", description="Set the logging channel")
    @app_commands.describe(channel="Channel for moderation logs")
    @app_commands.check(is_admin)
    async def setlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.bot.config.set_log_channel(channel.id)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Config Updated",
                description=f"Log channel set to {channel.mention}",
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="clearlog", description="Clear the logging channel")
    @app_commands.check(is_admin)
    async def clearlog(self, interaction: discord.Interaction):
        self.bot.config.set_log_channel(None)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Config Updated",
                description="Log channel cleared",
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="clonerole", description="Clone an existing role")
    @app_commands.describe(
        role="Role to clone",
        new_name="Name for the new role"
    )
    @app_commands.check(is_admin)
    async def clonerole(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        new_name: str
    ):
        try:
            new_role = await interaction.guild.create_role(
                name=new_name,
                permissions=role.permissions,
                color=role.color,
                hoist=role.hoist,
                mentionable=role.mentionable
            )
            
            await new_role.edit(position=role.position)
            
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Role Cloned",
                    description=f"Role {role.name} cloned as {new_role.mention}",
                    color=self.bot.config.embed_color
                )
            )
        except Exception as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description=f"Failed to clone role: {str(e)}",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="removerole", description="Delete a role")
    @app_commands.describe(role="Role to delete")
    @app_commands.check(is_admin)
    async def removerole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            role_name = role.name
            await role.delete()
            
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Role Removed",
                    description=f"Role '{role_name}' has been deleted",
                    color=self.bot.config.embed_color
                )
            )
        except Exception as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description=f"Failed to remove role: {str(e)}",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="speech", description="Send a message as the bot")
    @app_commands.describe(
        channel="Channel to send message in",
        content="Message content"
    )
    @app_commands.check(is_admin)
    async def speech(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        content: str
    ):
        """Send a message as the bot"""
        try:
            await channel.send(content)
            
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Message Sent",
                    description=f"Message sent to {channel.mention}",
                    color=self.bot.config.embed_color
                ),
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description=f"Failed to send message: {str(e)}",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="setpic", description="Update bot avatar")
    @app_commands.describe(image="New avatar image")
    @app_commands.check(is_admin)
    async def setpic(self, interaction: discord.Interaction, image: discord.Attachment):
        if not image.content_type.startswith('image/'):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid File",
                    description="Please attach an image file",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        try:
            img_data = await image.read()
            await self.bot.user.edit(avatar=img_data)
            
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Avatar Updated",
                    color=self.bot.config.embed_color
                )
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Failed to update avatar",
                    description=str(e),
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="setbanner", description="Update bot banner")
    @app_commands.describe(image="New banner image")
    @app_commands.check(is_admin)
    async def setbanner(self, interaction: discord.Interaction, image: discord.Attachment):
        if not image.content_type.startswith('image/'):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid File",
                    description="Please attach an image file",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        try:
            img_data = await image.read()
            await self.bot.user.edit(banner=img_data)
            
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Banner Updated",
                    color=self.bot.config.embed_color
                )
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Failed to update banner",
                    description=str(e),
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="setusername", description="Change bot username")
    @app_commands.describe(name="New username")
    @app_commands.check(is_admin)
    async def setusername(self, interaction: discord.Interaction, name: str):
        try:
            await self.bot.user.edit(username=name)
            
            await interaction.response.send_message(
                embed=discord.Embed(
                    title=f"Username changed to `{name}`",
                    color=self.bot.config.embed_color
                )
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Failed to update username",
                    description=str(e),
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @app_commands.command(name="setstatus", description="Set bot custom status")
    @app_commands.describe(status="Custom status text")
    @app_commands.check(is_admin)
    async def setstatus(self, interaction: discord.Interaction, status: str):
        activity = discord.CustomActivity(name=status)
        await self.bot.change_presence(activity=activity)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Custom status updated",
                description=f"`{status}`",
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="mediarestrict", description="Restrict user from sending media")
    @app_commands.describe(
        user="User to restrict",
        duration="Duration (optional, e.g. 1h, 1d)"
    )
    @app_commands.check(is_admin)
    async def mediarestrict(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        duration: str = None
    ):
        no_media_role = discord.utils.get(interaction.guild.roles, name="no-media")
        
        if not no_media_role:
            no_media_role = await interaction.guild.create_role(
                name="no-media",
                color=discord.Color.red(),
                reason="Created for media restriction system"
            )
            
            for channel in interaction.guild.text_channels:
                try:
                    await channel.set_permissions(
                        no_media_role,
                        attach_files=False,
                        embed_links=False
                    )
                except:
                    continue
        
        await user.add_roles(no_media_role)
        
        time_msg = ""
        if duration:
            from utils.helpers import parse_duration
            delta = parse_duration(duration)
            if delta:
                time_msg = f" for {duration}"
                
                async def remove_later():
                    import asyncio
                    await asyncio.sleep(delta.total_seconds())
                    try:
                        await user.remove_roles(no_media_role)
                    except:
                        pass
                
                self.bot.loop.create_task(remove_later())
        
        embed = discord.Embed(
            title="Media Restrictions Applied",
            description=f"{user.mention} can no longer send media{time_msg}",
            color=self.bot.config.embed_color
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="mediaunrestrict", description="Remove media restrictions from user")
    @app_commands.describe(user="User to unrestrict")
    @app_commands.check(is_admin)
    async def mediaunrestrict(self, interaction: discord.Interaction, user: discord.Member):
        no_media_role = discord.utils.get(interaction.guild.roles, name="no-media")
        
        if not no_media_role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="No 'no-media' role exists in this server",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        if no_media_role not in user.roles:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description=f"{user.mention} doesn't have media restrictions",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        await user.remove_roles(no_media_role)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Media Restrictions Removed",
                description=f"{user.mention} can now send media again",
                color=self.bot.config.embed_color
            )
        )

async def setup(bot):
    await bot.add_cog(Admin(bot))
