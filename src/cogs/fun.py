import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import random
import re
from datetime import timedelta
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fork_sessions = {}
        self.fork_cooldowns = {}
        self.last_quotes = []
    
    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        """Flip a coin - heads or tails"""
        result = random.choice(["Heads", "Tails"])
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🪙 Coin Flip",
                description=f"The coin lands on **{result}**!",
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
    @app_commands.describe(question="Your question for the 8-ball")
    async def eightball(self, interaction: discord.Interaction, question: str):
        answers = [
            "Mop says yes.",
            "No, the dirt remains.",
            "Ask again after sweeping.",
            "The suds are unclear.",
            "Certainly. The floor agrees.",
            "Doubtful. Try vacuuming your logic.",
            "Yes, but don't slip.",
            "Signs point to mildew.",
            "It's spotless truth.",
            "Grime says no.",
            "Bucket whispers yes.",
            "Trash says absolutely not.",
            "Wipe your doubts away – yes.",
            "Nope. Even the mop is shaking its head.",
            "Floor squeaked a yes.",
            "Dust settles on maybe.",
            "Broom hesitates. Try again.",
            "Yes. Janitor's intuition.",
            "No. That idea belongs in the bin.",
            "Possibly. Even the tiles are unsure.",
            "The janitor shrugs – uncertain.",
            "Outlook clean.",
            "Murky like a dirty mop bucket.",
            "The vacuum sucks the answer away.",
            "Sure. But keep it tidy."
        ]
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Magic Mop 8-Ball",
                description=random.choice(answers),
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="urban", description="Look up a word on Urban Dictionary")
    @app_commands.describe(word="Word to look up")
    async def urban(self, interaction: discord.Interaction, word: str):
        """Get Urban Dictionary definition"""
        await interaction.response.defer()
        
        url = f"https://api.urbandictionary.com/v0/define?term={word}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await interaction.followup.send(
                        embed=discord.Embed(
                            title="Error",
                            description="Couldn't reach Urban Dictionary",
                            color=discord.Color.red()
                        )
                    )
                
                data = await resp.json()
                if not data['list']:
                    return await interaction.followup.send(
                        embed=discord.Embed(
                            title="No Definition Found",
                            description=f"No urban definition found for **{word}**",
                            color=self.bot.config.embed_color
                        )
                    )
                
                definition = data['list'][0]['definition'].replace('[', '').replace(']', '')
                example = data['list'][0]['example'].replace('[', '').replace(']', '')
                
                embed = discord.Embed(
                    title=f"Urban Dictionary: {word}",
                    description=definition[:1024],
                    color=self.bot.config.embed_color
                )
                
                if example:
                    embed.add_field(name="Example", value=example[:1024], inline=False)
                
                await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="define", description="Get dictionary definition")
    @app_commands.describe(word="Word to define")
    async def define(self, interaction: discord.Interaction, word: str):
        await interaction.response.defer()
        
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await interaction.followup.send(
                        embed=discord.Embed(
                            title="No Definition Found",
                            description=f"No dictionary definition found for **{word}**",
                            color=self.bot.config.embed_color
                        )
                    )
                
                data = await resp.json()
                entry = data[0]
                word = entry['word']
                meanings = entry['meanings']
                
                embed = discord.Embed(
                    title=f"Dictionary: {word}",
                    color=self.bot.config.embed_color
                )
                
                for meaning in meanings[:3]:
                    part_of_speech = meaning['partOfSpeech']
                    definitions = meaning['definitions']
                    
                    value = ""
                    for i, definition in enumerate(definitions[:3]):
                        value += f"{i+1}. {definition['definition']}\n"
                        if 'example' in definition:
                            value += f"   *\"{definition['example']}\"*\n"
                    
                    embed.add_field(
                        name=part_of_speech.capitalize(),
                        value=value or "No definition available",
                        inline=False
                    )
                
                if 'phonetic' in entry:
                    embed.set_footer(text=f"Pronunciation: {entry['phonetic']}")
                
                await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="quote", description="Get a random quote from a user")
    @app_commands.describe(user="User to quote (leave empty for yourself)")
    async def quote(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        
        await interaction.response.defer()
        
        url_pattern = re.compile(r'https?://\S+')
        messages = []
        scanned = 0
        
        for channel in interaction.guild.text_channels:
            perms = channel.permissions_for(interaction.guild.me)
            user_perms = channel.permissions_for(target)
            
            if not (perms.read_messages and perms.read_message_history):
                continue
            if not (user_perms.read_messages and user_perms.read_message_history):
                continue
            
            try:
                async for msg in channel.history(limit=200, oldest_first=True):
                    if msg.author.id != target.id:
                        continue
                    
                    if (len(msg.content) >= self.bot.config.quote_min_length and
                        not msg.attachments and
                        not msg.embeds and
                        not url_pattern.search(msg.content)):
                        
                        content = msg.content.strip()
                        if content not in messages:
                            messages.append(content)
                            scanned += 1
                            
                            if scanned >= self.bot.config.quote_scan_limit:
                                break
                
                if scanned >= self.bot.config.quote_scan_limit:
                    break
                    
            except (discord.Forbidden, discord.HTTPException):
                continue
        
        available_quotes = [m for m in messages if m not in self.last_quotes]
        
        if not available_quotes:
            return await interaction.followup.send(
                embed=discord.Embed(
                    title="No Quote Found",
                    description=f"No suitable unique message found from **{target.display_name}**",
                    color=self.bot.config.embed_color
                )
            )
        
        quote_text = random.choice(available_quotes)
        self.last_quotes.append(quote_text)

        if len(self.last_quotes) > 4:
            self.last_quotes.pop(0)

        embed = discord.Embed(
            title="Quote",
            description=f'"{quote_text}"\n— {target.display_name}',
            color=self.bot.config.embed_color
        )

        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="broomfight", description="Challenge someone to a broom fight")
    @app_commands.describe(user="User to challenge")
    async def broomfight(self, interaction: discord.Interaction, user: discord.Member):
        """Challenge another user to a broom fight"""
        if user.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You can't fight yourself. Even the mop knows that.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        winner = random.choice([interaction.user, user])
        loser = user if winner == interaction.user else interaction.user
        
        desc = (
            f"{interaction.user.mention} challenges {user.mention} to a broom duel!\n\n"
            f"💥 After intense sweeping and dodging...\n"
            f"🏆 **{winner.display_name}** emerges victorious!\n"
            f"😵 {loser.display_name} drops their mop."
        )
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🧹 Broom Fight!",
                description=desc,
                color=self.bot.config.embed_color
            )
        )
    
    @app_commands.command(name="fork", description="Challenge someone to a fork duel")
    @app_commands.describe(target="User to challenge (leave empty to check cooldown)")
    async def fork(self, interaction: discord.Interaction, target: discord.Member = None):
        now = discord.utils.utcnow()

        if target is None:
            last_used = self.fork_cooldowns.get(interaction.user.id)
            cooldown_delta = timedelta(minutes=self.bot.config.fork_cooldown_minutes)
            
            if last_used:
                remaining = (last_used + cooldown_delta) - now
                if remaining.total_seconds() > 0:
                    timestamp = f"<t:{int((now + remaining).timestamp())}:R>"
                    return await interaction.response.send_message(
                        embed=discord.Embed(
                            title="Fork Cooldown",
                            description=f"You can fork again {timestamp}",
                            color=self.bot.config.embed_color
                        ),
                        ephemeral=True
                    )
                else:
                    return await interaction.response.send_message(
                        embed=discord.Embed(
                            title="Fork Cooldown",
                            description="You can fork again now!",
                            color=self.bot.config.embed_color
                        ),
                        ephemeral=True
                    )
            else:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Fork Cooldown",
                        description="You haven't used the fork command recently. No cooldown active.",
                        color=self.bot.config.embed_color
                    ),
                    ephemeral=True
                )
        if target.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid Target",
                    description="You can't fork yourself!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        if target.bot:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid Target",
                    description="You can't fork a bot!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        last_used = self.fork_cooldowns.get(interaction.user.id)
        cooldown_delta = timedelta(minutes=self.bot.config.fork_cooldown_minutes)
        
        if last_used and now - last_used < cooldown_delta:
            remaining = (last_used + cooldown_delta) - now
            timestamp = f"<t:{int((now + remaining).timestamp())}:R>"
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Fork Cooldown",
                    description=f"You will be able to fork someone {timestamp}",
                    color=self.bot.config.embed_color
                ),
                ephemeral=True
            )
        
        if interaction.user.id in self.fork_sessions:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Fork Duel Active",
                    description="You're already in a fork duel!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        number = random.randint(1, 100)
        self.fork_sessions[interaction.user.id] = (target, number)
        self.fork_cooldowns[interaction.user.id] = now
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Fork Duel Initiated",
                description=(
                    f"{interaction.user.mention}, guess the secret number between **1 and 100**.\n"
                    f"If you're within **±9**, {target.mention} gets forked (5 min timeout).\n"
                    f"If not, **you** get forked (1m 25s timeout).\n\n"
                    f"**You have 60 seconds to respond!**"
                ),
                color=self.bot.config.embed_color
            )
        )
        
        await asyncio.sleep(60)
        if interaction.user.id in self.fork_sessions:
            self.fork_sessions.pop(interaction.user.id)
            until = discord.utils.utcnow() + timedelta(seconds=85)
            
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Fork Duel Timed Out",
                    description=(
                        f"{interaction.user.mention} failed to guess in time.\n"
                        f"They receive a 1 minute 25 second timeout."
                    ),
                    color=discord.Color.orange()
                )
            )
            
            try:
                await interaction.user.timeout(until, reason="Failed to respond to fork duel")
            except:
                pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author.id not in self.fork_sessions:
            return
        
        try:
            guess = int(message.content.strip())
            if not (1 <= guess <= 100):
                return
        except ValueError:
            return
        
        target, number = self.fork_sessions.pop(message.author.id)
        delta = abs(guess - number)
        
        if delta <= 9:
            until = discord.utils.utcnow() + timedelta(minutes=5)
            await message.channel.send(
                embed=discord.Embed(
                    title="🎯 Bullseye!",
                    description=(
                        f"{message.author.mention} guessed **{guess}** (target was {number}) – "
                        f"{target.mention} is forked for 5 minutes."
                    ),
                    color=discord.Color.red()
                )
            )
            try:
                await target.timeout(until, reason="Forked by duel")
            except:
                pass
        else:
            until = discord.utils.utcnow() + timedelta(seconds=85)
            await message.channel.send(
                embed=discord.Embed(
                    title="💥 Backfired!",
                    description=(
                        f"{message.author.mention} guessed **{guess}** (target was {number}) – "
                        f"they forked themselves. 1 minute 25 second timeout."
                    ),
                    color=discord.Color.orange()
                )
            )
            try:
                await message.author.timeout(until, reason="Forked themselves")
            except:
                pass

async def setup(bot):
    await bot.add_cog(Fun(bot))
