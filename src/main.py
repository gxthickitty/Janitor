import asyncio
import discord
from discord.ext import commands
from pathlib import Path
import json
import time

from utils.config import Config
from utils.database import Database
from utils.logger import setup_logger

logger = setup_logger()

class JanitorBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        intents.message_content = True
        
        super().__init__(
            command_prefix=commands.when_mentioned_or('v', 'V'),
            intents=intents,
            help_command=None
        )
        
        self.config = Config()
        self.db = Database()
        self.start_time = time.time()
        
    async def setup_hook(self):
        logger.info("Loading cogs...")
        
        cog_folders = ['cogs.admin', 'cogs.moderation', 'cogs.fun', 'cogs.info', 'cogs.games', 'cogs.customize']
        
        for folder in cog_folders:
            try:
                await self.load_extension(folder)
                logger.info(f"Loaded {folder}")
            except Exception as e:
                logger.error(f"Failed to load {folder}: {e}")
        
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        logger.info(f'Logged in as {self.user.name} ({self.user.id})')
        logger.info(f'Connected to {len(self.guilds)} guilds')
        logger.info('Bot is ready!')

async def main():
    bot = JanitorBot()
    
    try:
        await bot.start(bot.config.token)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
