import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="rrd", description="Challenge someone to Russian Roulette")
    @app_commands.describe(target="User to challenge")
    async def russian_roulette_duel(self, interaction: discord.Interaction, target: discord.Member):
        if target == interaction.user:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You can't duel yourself!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        if target.bot:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You can't duel a bot!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        author_stats = self.bot.db.get_duel_stats(interaction.user.id)
        last_duel = author_stats['last_duel']
        current_time = datetime.now().timestamp()
        
        if last_duel and (current_time - last_duel) < self.bot.config.duel_cooldown:
            cooldown_end = datetime.fromtimestamp(last_duel + self.bot.config.duel_cooldown)
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Cooldown Active",
                    description=f"You can duel again <t:{int(cooldown_end.timestamp())}:R>",
                    color=discord.Color.orange()
                ),
                ephemeral=True
            )
        
        target_stats = self.bot.db.get_duel_stats(target.id)
        embed = discord.Embed(
            title="🔫 Duel Challenge",
            description=(
                f"{interaction.user.mention} has challenged {target.mention} to Russian Roulette!\n\n"
                "The loser gets a 60 second timeout.\n"
                f"{target.mention}, click ✅ to accept or ❌ to decline."
            ),
            color=self.bot.config.embed_color
        )
        
        embed.add_field(
            name=f"{interaction.user.display_name}'s Stats",
            value=f"🏆 Wins: {author_stats['wins']}\n☠️ Losses: {author_stats['losses']}",
            inline=True
        )
        embed.add_field(
            name=f"{target.display_name}'s Stats",
            value=f"🏆 Wins: {target_stats['wins']}\n☠️ Losses: {target_stats['losses']}",
            inline=True
        )
        
        view = DuelView(interaction.user, target, self.bot)
        
        message = await interaction.response.send_message(
            content=f"{target.mention}",
            embed=embed,
            view=view
        )
        view.message = await interaction.original_response()

    @app_commands.command(name="duelstats", description="View duel statistics")
    @app_commands.describe(user="User to check stats for (leave empty for yourself)")
    async def duel_stats(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        stats = self.bot.db.get_duel_stats(target.id)
        
        embed = discord.Embed(
            title=f"🏆 Duel Statistics: {target.display_name}",
            color=self.bot.config.embed_color
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        
        total = stats['wins'] + stats['losses']
        
        embed.add_field(
            name="🔫 Duels Fought",
            value=f"Total: {total}",
            inline=False
        )
        embed.add_field(
            name="🏆 Victories",
            value=f"{stats['wins']} wins",
            inline=True
        )
        embed.add_field(
            name="☠️ Defeats",
            value=f"{stats['losses']} losses",
            inline=True
        )
        
        if total > 0:
            win_rate = (stats['wins'] / total) * 100
            embed.add_field(
                name="📊 Win Rate",
                value=f"{win_rate:.1f}%",
                inline=False
            )
        
        if stats['last_duel'] > 0:
            embed.set_footer(text=f"Last duel: <t:{stats['last_duel']}:R>")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="rrdleaderboard", description="View duel leaderboard")
    async def rrd_leaderboard(self, interaction: discord.Interaction):
        top_players = self.bot.db.get_duel_leaderboard(5)
        
        embed = discord.Embed(
            title=":crossed_swords: Russian Roulette Duel Leaderboard",
            description="Top 5 players by win ratio",
            color=self.bot.config.embed_color
        )
        
        if not top_players:
            embed.description = "No duel data available yet."
        else:
            leaderboard = []
            for i, (user_id, wins, losses) in enumerate(top_players):
                try:
                    user = await self.bot.fetch_user(user_id)
                    username = user.display_name
                except:
                    username = f"Unknown User ({user_id})"
                
                total = wins + losses
                win_ratio = (wins / total) * 100 if total > 0 else 0
                crown = ":crown:" if i == 0 else ""
                
                leaderboard.append(
                    f"{i+1}. {username} {crown} - **{wins}W** / **{losses}L** ({win_ratio:.1f}%)"
                )
            
            embed.add_field(
                name="Top Duelists",
                value="\n".join(leaderboard),
                inline=False
            )
        
        embed.set_footer(
            text=f"Requested by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        
        await interaction.response.send_message(embed=embed)


class DuelView(discord.ui.View):
    def __init__(self, challenger, target, bot):
        super().__init__(timeout=30.0)
        self.challenger = challenger
        self.target = target
        self.bot = bot
        self.message = None
        self.responded = False
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.target:
            await interaction.response.send_message(
                "This challenge is not for you!",
                ephemeral=True
            )
            return False
        return True
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, emoji="✅")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.responded = True
        await interaction.response.defer()
        
        for item in self.children:
            item.disabled = True
        
        await interaction.message.edit(view=self)
        
        embed = discord.Embed(
            title="🔫 Russian Roulette Duel",
            description=(
                f"{self.challenger.mention} vs {self.target.mention}\n\n"
                "The revolver has 6 chambers with 1 bullet.\n"
                "Players will take turns pulling the trigger...\n\n"
                "**First shot:** Loading chamber..."
            ),
            color=self.bot.config.embed_color
        )
        embed.set_footer(text="The loser gets a 60 second timeout!")
        
        await interaction.followup.send(embed=embed)
        
        chambers = [False] * 6
        bullet_pos = random.randint(0, 5)
        chambers[bullet_pos] = True
        current_turn = 0
        turn_names = [self.challenger, self.target]
        
        for turn in range(6):
            await asyncio.sleep(2)
            
            if chambers[turn]:
                loser = turn_names[current_turn]
                winner = turn_names[1 - current_turn]
                
                self.bot.db.update_duel_stats(winner.id, won=True)
                self.bot.db.update_duel_stats(loser.id, won=False)
                
                winner_stats = self.bot.db.get_duel_stats(winner.id)
                loser_stats = self.bot.db.get_duel_stats(loser.id)
                
                embed = discord.Embed(
                    title="🔫 Russian Roulette Duel",
                    description=(
                        f"💥 **BANG!** {loser.mention} didn't survive the duel!\n\n"
                        f"🏆 **Winner:** {winner.mention} (now has {winner_stats['wins']} wins)\n"
                        f"☠️ **Loser:** {loser.mention} (now has {loser_stats['losses']} losses)"
                    ),
                    color=discord.Color.red()
                )
                embed.set_footer(text="Timeout applied for 60 seconds!")
                
                await interaction.channel.send(embed=embed)
                
                try:
                    await loser.timeout(timedelta(seconds=60), reason="Lost Russian Roulette duel")
                except:
                    pass
                
                break
            else:
                embed = discord.Embed(
                    title="🔫 Russian Roulette Duel",
                    description=(
                        f"**Turn {turn + 1}:** {turn_names[current_turn].mention} pulls the trigger...\n"
                        f"*click!* The chamber was empty.\n\n"
                        f"Next turn: {turn_names[1 - current_turn].mention}"
                    ),
                    color=self.bot.config.embed_color
                )
                
                await interaction.channel.send(embed=embed)
                current_turn = 1 - current_turn
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, emoji="❌")
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.responded = True
        for item in self.children:
            item.disabled = True
        
        embed = discord.Embed(
            title="Duel Declined",
            description=f"{self.target.mention} chickened out!",
            color=discord.Color.red()
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        if self.responded:
            return
            
        for item in self.children:
            item.disabled = True
        
        if self.message:
            try:
                embed = discord.Embed(
                    title="Duel Expired",
                    description=f"{self.target.mention} didn't respond in time!",
                    color=discord.Color.orange()
                )
                await self.message.edit(embed=embed, view=self)
            except:
                pass


async def setup(bot):
    await bot.add_cog(Games(bot))
