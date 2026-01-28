# 🧹 Janitor Bot v2.0

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

*A modern, feature-rich Discord bot with slash commands, modular architecture, and fun interactive games.*

[Features](#-features) • [Installation](#-installation) • [Commands](#-command-reference) • [Configuration](#%EF%B8%8F-configuration) • [Development](#-development)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#%EF%B8%8F-configuration)
- [Command Reference](#-command-reference)
  - [Info Commands](#info-commands)
  - [Fun Commands](#fun-commands)
  - [Game Commands](#game-commands)
  - [Moderation Commands](#moderation-commands-admin-only)
  - [Admin Commands](#admin-commands-admin-only)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Development Guide](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎮 Interactive Games
- **Russian Roulette Duel** - Challenge users with interactive buttons and stat tracking
- **Fork Duel** - Number guessing game with timeout penalties
- **Broom Fight** - Random outcome duels

### 🎉 Fun & Utility
- **Smart Quote System** - Fetches random quotes from users with anti-repeat logic
- **Dictionary & Urban Dictionary** - Word definitions at your fingertips
- **Magic 8-Ball** - Janitor-themed fortune telling
- **Birthday Tracking** - Automatic role assignment for birthdays

### 🛡️ Moderation Tools
- **Advanced Purge** - Bulk message deletion with logging
- **Timeout Management** - Flexible duration-based timeouts
- **Media Restrictions** - Temporary media send permissions
- **Channel Controls** - Lock, unlock, and slowmode management

### 🔧 Admin Features
- **Bot Customization** - Change avatar, banner, username, and status
- **Role Management** - Clone and delete roles
- **Message Sending** - Send messages as the bot
- **Logging System** - Comprehensive moderation logs

### 💻 Technical Features
- **Slash Commands** - Modern Discord UI with autocomplete
- **Modular Architecture** - Clean cog system for easy maintenance
- **SQLite Database** - Persistent data storage
- **JSON Configuration** - Easy-to-edit settings
- **Comprehensive Logging** - File and console logging
- **Error Handling** - Graceful error management throughout

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/janitor-bot.git
cd janitor-bot

# Install dependencies
pip install -r requirements.txt

# Configure the bot
# Edit config.json with your tokens

# Run the bot
python main.py
```

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Discord Bot Token** - [Discord Developer Portal](https://discord.com/developers/applications)
- **Genius API Token** (optional) - [Genius API](https://genius.com/api-clients) - Only needed for lyrics command

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/janitor-bot.git
   cd janitor-bot
   ```

2. **Create Project Structure**
   ```
   janitor-bot/
   ├── main.py
   ├── config.json
   ├── requirements.txt
   ├── utils/
   │   ├── __init__.py
   │   ├── config.py
   │   ├── database.py
   │   ├── helpers.py
   │   └── logger.py
   ├── cogs/
   │   ├── __init__.py
   │   ├── admin.py
   │   ├── moderation.py
   │   ├── fun.py
   │   ├── games.py
   │   └── info.py
   ├── data/         (auto-created)
   └── logs/         (auto-created)
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Bot**
   
   Edit `config.json`:
   ```json
   {
     "token": "YOUR_BOT_TOKEN_HERE",
     "genius_token": "YOUR_GENIUS_API_TOKEN"
   }
   ```

5. **Create `__init__.py` files**
   
   Create empty `__init__.py` files in `utils/` and `cogs/` directories:
   ```bash
   touch utils/__init__.py cogs/__init__.py
   ```

6. **Run the Bot**
   ```bash
   python main.py
   ```

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Copy the bot token and add it to `config.json`
6. Go to OAuth2 → URL Generator
7. Select scopes: `bot` and `applications.commands`
8. Select bot permissions (Administrator recommended for full functionality)
9. Use the generated URL to invite the bot to your server

---

## ⚙️ Configuration

### config.json Structure

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "genius_token": "YOUR_GENIUS_API_TOKEN",
  
  "bot_info": {
    "developer": "Your Name",
    "host_provider": "Hosting Service",
    "version": "2.0",
    "description": "Bot Description"
  },
  
  "colors": {
    "primary": "a84141"  // Hex color without #
  },
  
  "roles": {
    "birthday_role_id": 1214960856085962762  // Role to assign on birthdays
  },
  
  "cooldowns": {
    "duel_seconds": 30,           // Russian Roulette cooldown
    "fork_minutes": 10,           // Fork duel cooldown
    "fork_timeout_minutes": 5     // Fork timeout duration
  },
  
  "limits": {
    "purge_max": 350,             // Max messages to purge
    "quote_scan_limit": 2000,     // Max messages to scan for quotes
    "quote_min_length": 20,       // Min quote length
    "quote_history_size": 4       // Recent quotes to avoid repeating
  },
  
  "database": {
    "path": "data/bot.db"         // SQLite database location
  },
  
  "logging": {
    "log_channel_id": null        // Set via /setlog command
  }
}
```

### Environment Variables (Alternative)

You can also use environment variables for sensitive data:

```python
# In main.py, modify Config class to check environment variables
import os

token = os.getenv('DISCORD_TOKEN') or self.data.get('token', '')
```

---

## 📚 Command Reference

All commands use Discord's slash command system. Type `/` in Discord to see available commands.

### Info Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/help` | Show bot information and features | None | `/help` |
| `/commands` | List all commands by category | `category` (optional) | `/commands fun` |
| `/whois` | Detailed user information with badges | `user` (optional) | `/whois @User` or `/whois 123456789` |
| `/ping` | Check bot latency | None | `/ping` |
| `/uptime` | Show how long bot has been running | None | `/uptime` |
| `/duelstats` | View Russian Roulette statistics | `user` (optional) | `/duelstats @User` |
| `/birthdays` | Show upcoming birthdays | `channel` (admin only) | `/birthdays` or `/birthdays #general` |

#### `/whois` Features
- Works for **users outside the server** (use their ID)
- Shows **all Discord badges**:
  - HypeSquad houses (Bravery, Brilliance, Balance)
  - Bug Hunter (Level 1 & 2)
  - Early Supporter
  - Active Developer
  - Verified Bot Developer
  - Discord Staff/Partner
- Displays **banner image** if user has one
- Shows **server-specific info** (roles, nickname, join date) if in server
- Links to **avatar** and **server avatar**
- Shows **timeout status** if applicable

#### `/birthdays` Features
- **Regular Users**: Shows 3 closest birthdays in current channel
- **Admins**: Can specify channel to send birthday list
- Automatically **assigns birthday role** to today's celebrants
- Parses roles formatted as "15th January", "3rd March", etc.

---

### Fun Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/quote` | Random quote from a user's messages | `user` (optional) | `/quote @User` |
| `/coinflip` | Flip a coin | None | `/coinflip` |
| `/8ball` | Ask the magic janitor 8-ball | `question` | `/8ball Will it rain?` |
| `/urban` | Urban Dictionary definition | `word` | `/urban yeet` |
| `/define` | Dictionary definition | `word` | `/define serendipity` |
| `/broomfight` | Challenge to a broom fight | `user` | `/broomfight @User` |
| `/fork` | Fork duel number guessing game | `target` (optional) | `/fork @User` |

#### `/quote` System
- Scans up to 2000 messages across all readable channels
- Filters out:
  - Messages with attachments
  - Messages with embeds
  - Messages with URLs
  - Messages shorter than 20 characters
- Avoids repeating last 4 quotes
- Respects channel permissions (won't quote from channels user can't see)

#### `/fork` Duel Rules
- Guess a number between 1-100
- **Win** (within ±9): Target gets 5-minute timeout
- **Lose**: You get 1 minute 25 second timeout
- **No answer**: 1 minute 25 second timeout
- 10-minute cooldown between uses
- 60 seconds to respond

---

### Game Commands

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/rrd` | Russian Roulette duel | `target` | `/rrd @User` |
| `/rrdleaderboard` | View duel leaderboard | None | `/rrdleaderboard` |

#### `/rrd` Russian Roulette Duel

**How It Works:**
1. Challenge a user with `/rrd @User`
2. Target gets **30 seconds** to accept or decline (via buttons)
3. Target is **pinged** in the challenge message
4. 6-chamber revolver with 1 bullet
5. Players take turns pulling the trigger
6. **Loser** gets 60-second timeout
7. **Stats** are tracked in database

**Features:**
- ✅ Interactive button-based UI
- ✅ 30-second cooldown per user
- ✅ Win/loss statistics tracked
- ✅ Leaderboard by win ratio
- ✅ Automatic timeout on expiry
- ✅ Buttons disabled after response

**Statistics Tracked:**
- Total wins
- Total losses
- Win ratio percentage
- Last duel timestamp

---

### Moderation Commands (Admin Only)

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/ban` | Ban a user | `user`, `duration` (optional), `reason` (optional), `delete_days` (0 or 7) | `/ban @User 7d Spamming` |
| `/timeout` | Timeout a user | `user`, `duration` (default: 1h), `reason` (optional) | `/timeout @User 30min Spam` |
| `/removetimeout` | Remove timeout | `user` | `/removetimeout @User` |
| `/lock` | Lock a channel | `channel` (optional) | `/lock #general` |
| `/unlock` | Unlock a channel | `channel` (optional) | `/unlock #general` |
| `/slowmode` | Set channel slowmode | `seconds`, `channel` (optional) | `/slowmode 10 #chat` |
| `/purge` | Bulk delete messages | `amount`, `user` (optional) | `/purge 50` or `/purge 20 @User` |
| `/mediarestrict` | Restrict user from media | `user`, `duration` (optional) | `/mediarestrict @User 1h` |
| `/mediaunrestrict` | Remove media restrictions | `user` | `/mediaunrestrict @User` |

#### Duration Formats
All commands support flexible duration formats:
- `30min` - 30 minutes
- `2h` - 2 hours
- `1d` - 1 day
- `1w` - 1 week
- `1m` - 1 month
- `1y` - 1 year

#### `/purge` Features
- Delete up to **350 messages** at once
- Filter by **specific user**
- Automatic **logging** to configured log channel
- Creates **text file** with deleted message content
- Includes timestamps and authors

#### `/mediarestrict` System
- Creates/uses "no-media" role
- Automatically configures permissions across all channels
- Optional **temporary restriction** with duration
- Prevents:
  - File attachments
  - Embed links

---

### Admin Commands (Admin Only)

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/setlog` | Set logging channel | `channel` | `/setlog #mod-log` |
| `/clearlog` | Clear log channel config | None | `/clearlog` |
| `/clonerole` | Clone a role | `role`, `new_name` | `/clonerole @Moderator Mod-Backup` |
| `/removerole` | Delete a role | `role` | `/removerole @OldRole` |
| `/speech` | Send message as bot | `channel`, `content` | `/speech #general Hello world!` |
| `/setpic` | Update bot avatar | `image` (attachment) | `/setpic` (attach image) |
| `/setbanner` | Update bot banner | `image` (attachment) | `/setbanner` (attach image) |
| `/setusername` | Change bot username | `name` | `/setusername JanitorBot` |
| `/setstatus` | Set custom status | `status` | `/setstatus Cleaning servers` |

#### `/clonerole` Features
- Copies **all permissions**
- Preserves **color**
- Maintains **hoist** and **mentionable** settings
- Places new role at **same position** as original

#### Logging System
- Set channel with `/setlog #channel`
- Logs all purge operations
- Includes:
  - Moderator who performed action
  - Timestamp
  - Channel affected
  - Message count
  - Full message content (as text file)

---

## 📁 Project Structure

```
janitor-bot/
│
├── main.py                      # Bot entry point and main bot class
│   ├── JanitorBot class         # Main bot with config and database
│   ├── setup_hook()             # Loads cogs and syncs commands
│   └── on_ready()               # Startup logging
│
├── config.json                  # Configuration file (JSON)
│   ├── tokens                   # Bot and API tokens
│   ├── bot_info                 # Bot metadata
│   ├── colors                   # Embed colors
│   ├── roles                    # Special role IDs
│   ├── cooldowns                # Command cooldowns
│   ├── limits                   # Various limits
│   └── logging                  # Log channel config
│
├── requirements.txt             # Python dependencies
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   ├── config.py               # Configuration manager
│   │   ├── Config class        # Loads and manages config.json
│   │   ├── Properties          # Easy access to config values
│   │   └── save()              # Save config changes
│   │
│   ├── database.py             # Database manager
│   │   ├── Database class      # SQLite connection manager
│   │   ├── init_tables()       # Create database tables
│   │   ├── get_duel_stats()    # Fetch duel statistics
│   │   ├── update_duel_stats() # Update win/loss records
│   │   └── get_duel_leaderboard() # Fetch top players
│   │
│   ├── helpers.py              # Helper functions
│   │   ├── get_user()          # Flexible user lookup
│   │   ├── parse_duration()    # Parse time strings
│   │   ├── format_duration()   # Format seconds to readable
│   │   └── is_admin()          # Admin permission check
│   │
│   └── logger.py               # Logging configuration
│       └── setup_logger()      # Configure file and console logging
│
├── cogs/                        # Command modules (cogs)
│   ├── __init__.py
│   │
│   ├── info.py                 # Information commands
│   │   ├── /help               # Bot information
│   │   ├── /commands           # Command list
│   │   ├── /whois              # User information (enhanced)
│   │   ├── /uptime             # Bot uptime
│   │   ├── /ping               # Latency check
│   │   └── /birthdays          # Birthday tracking
│   │
│   ├── fun.py                  # Fun & interactive commands
│   │   ├── /coinflip           # Coin flip
│   │   ├── /8ball              # Magic 8-ball
│   │   ├── /urban              # Urban Dictionary
│   │   ├── /define             # Dictionary definition
│   │   ├── /quote              # Random user quote
│   │   ├── /broomfight         # Broom duel
│   │   ├── /fork               # Fork duel game
│   │   └── on_message()        # Fork guess handler
│   │
│   ├── games.py                # Game commands
│   │   ├── /rrd                # Russian Roulette Duel
│   │   ├── /duelstats          # View duel statistics
│   │   ├── /rrdleaderboard     # Duel leaderboard
│   │   └── DuelView class      # Interactive button UI
│   │
│   ├── moderation.py           # Moderation commands
│   │   ├── /ban                # Ban users
│   │   ├── /timeout            # Timeout users
│   │   ├── /removetimeout      # Remove timeout
│   │   ├── /lock               # Lock channels
│   │   ├── /unlock             # Unlock channels
│   │   ├── /slowmode           # Set slowmode
│   │   └── /purge              # Bulk delete messages
│   │
│   └── admin.py                # Admin commands
│       ├── /setlog             # Configure logging
│       ├── /clearlog           # Clear log config
│       ├── /clonerole          # Clone roles
│       ├── /removerole         # Delete roles
│       ├── /speech             # Send messages as bot
│       ├── /setpic             # Update avatar
│       ├── /setbanner          # Update banner
│       ├── /setusername        # Change username
│       ├── /setstatus          # Set status
│       ├── /mediarestrict      # Restrict media
│       └── /mediaunrestrict    # Remove restrictions
│
├── data/                        # Data directory (auto-created)
│   └── bot.db                  # SQLite database
│
└── logs/                        # Logs directory (auto-created)
    └── bot.log                 # Application log file
```

### File Descriptions

#### Core Files

- **main.py** - Bot entry point, handles startup and cog loading
- **config.json** - All bot configuration in JSON format
- **requirements.txt** - Python package dependencies

#### Utils Module

- **config.py** - Centralized configuration management with property accessors
- **database.py** - SQLite database interface for persistent data
- **helpers.py** - Reusable utility functions (user lookup, time parsing, etc.)
- **logger.py** - Logging configuration for debugging and monitoring

#### Cogs (Command Modules)

- **info.py** - User information and bot statistics
- **fun.py** - Entertainment commands and interactive features
- **games.py** - Competitive games with stat tracking
- **moderation.py** - Server moderation tools
- **admin.py** - Bot administration and configuration

---

## 🗄️ Database Schema

### Tables

#### `duel_stats`
Stores Russian Roulette duel statistics per user.

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | INTEGER (PK) | Discord user ID |
| `wins` | INTEGER | Number of duel wins |
| `losses` | INTEGER | Number of duel losses |
| `last_duel` | INTEGER | Unix timestamp of last duel |

**Indexes:**
- Primary key on `user_id`

**Queries:**
```sql
-- Get user stats
SELECT wins, losses, last_duel FROM duel_stats WHERE user_id = ?

-- Update win
UPDATE duel_stats SET wins = wins + 1, last_duel = ? WHERE user_id = ?

-- Leaderboard
SELECT user_id, wins, losses 
FROM duel_stats 
WHERE wins + losses > 0 
ORDER BY CAST(wins AS FLOAT) / NULLIF(wins + losses, 0) DESC 
LIMIT 5
```

### Database Location

Default: `data/bot.db` (configurable in `config.json`)

### Backup Recommendations

```bash
# Manual backup
cp data/bot.db data/bot.db.backup

# Scheduled backup (Linux/Mac)
# Add to crontab: 0 0 * * * cp /path/to/data/bot.db /path/to/backups/bot.db.$(date +\%Y\%m\%d)
```

---

## 🛠️ Development

### Adding New Commands

1. **Choose the appropriate cog** (`info.py`, `fun.py`, `games.py`, `moderation.py`, or `admin.py`)

2. **Add the command:**
   ```python
   @app_commands.command(name="mycommand", description="What this command does")
   @app_commands.describe(param1="Description of param1")
   async def mycommand(self, interaction: discord.Interaction, param1: str):
       """Command implementation"""
       await interaction.response.send_message(
           embed=discord.Embed(
               title="My Command",
               description=f"You said: {param1}",
               color=self.bot.config.embed_color
           )
       )
   ```

3. **Restart the bot** - Commands sync automatically on startup

### Creating New Cogs

1. **Create file in `cogs/` directory:**
   ```python
   # cogs/mycog.py
   import discord
   from discord import app_commands
   from discord.ext import commands

   class MyCog(commands.Cog):
       def __init__(self, bot):
           self.bot = bot
       
       @app_commands.command(name="test")
       async def test(self, interaction: discord.Interaction):
           await interaction.response.send_message("Test!")

   async def setup(bot):
       await bot.add_cog(MyCog(bot))
   ```

2. **Add to `main.py` cog list:**
   ```python
   cog_folders = ['cogs.admin', 'cogs.moderation', 'cogs.fun', 'cogs.info', 'cogs.games', 'cogs.mycog']
   ```

3. **Restart the bot**

### Adding Database Tables

1. **Update `utils/database.py`:**
   ```python
   def _init_tables(self):
       """Initialize all database tables"""
       conn = self._get_connection()
       cursor = conn.cursor()
       
       # Your new table
       cursor.execute('''
           CREATE TABLE IF NOT EXISTS my_table (
               id INTEGER PRIMARY KEY,
               data TEXT
           )
       ''')
       
       conn.commit()
       conn.close()
   ```

2. **Add methods to interact with table:**
   ```python
   def get_my_data(self, id: int):
       conn = self._get_connection()
       cursor = conn.cursor()
       cursor.execute("SELECT data FROM my_table WHERE id=?", (id,))
       result = cursor.fetchone()
       conn.close()
       return result[0] if result else None
   ```

### Adding Config Options

1. **Update `config.json`:**
   ```json
   {
     "my_feature": {
       "enabled": true,
       "timeout": 60
     }
   }
   ```

2. **Add property to `utils/config.py`:**
   ```python
   @property
   def my_feature_enabled(self) -> bool:
       return self.data.get('my_feature', {}).get('enabled', False)
   ```

3. **Use in commands:**
   ```python
   if self.bot.config.my_feature_enabled:
       # Feature logic
   ```

### Testing

```bash
# Run bot in test mode
python main.py

# Check logs
tail -f logs/bot.log

# Test specific command
# Use /commandname in Discord
```

### Debugging

Enable debug logging:

```python
# In utils/logger.py
logger.setLevel(logging.DEBUG)  # Change from INFO to DEBUG
```

Check logs at `logs/bot.log` for detailed information.

---

## 🐛 Troubleshooting

### Common Issues

#### Bot Won't Start

**Problem:** Bot crashes immediately or won't connect

**Solutions:**
- ✅ Check `config.json` has valid bot token
- ✅ Verify all dependencies installed: `pip install -r requirements.txt`
- ✅ Check Python version: `python --version` (needs 3.8+)
- ✅ Look at `logs/bot.log` for error messages
- ✅ Ensure `__init__.py` exists in `utils/` and `cogs/`

#### Commands Not Appearing

**Problem:** Slash commands don't show in Discord

**Solutions:**
- ✅ Verify bot has `applications.commands` scope
- ✅ Wait 5-10 minutes for Discord to sync
- ✅ Restart bot to force re-sync
- ✅ Check bot has proper permissions in server
- ✅ Try kicking and re-inviting bot with correct URL

#### Permission Errors

**Problem:** "Missing Permissions" or "Forbidden" errors

**Solutions:**
- ✅ Ensure bot role is **above** roles it needs to modify
- ✅ Grant bot **Administrator** permission (recommended)
- ✅ Check specific permissions needed:
  - Ban Members (for `/ban`)
  - Moderate Members (for `/timeout`)
  - Manage Channels (for `/lock`, `/unlock`)
  - Manage Messages (for `/purge`)
  - Manage Roles (for `/mediarestrict`, role commands)

#### Database Errors

**Problem:** Database locked or corrupted

**Solutions:**
- ✅ Stop bot completely before accessing database
- ✅ Check file permissions on `data/bot.db`
- ✅ Restore from backup if corrupted
- ✅ Delete `data/bot.db` to reset (loses all data!)

#### Fork/Duel Not Responding

**Problem:** Game commands not accepting input

**Solutions:**
- ✅ Check bot has `Read Message History` permission
- ✅ Ensure `on_message` event is registered
- ✅ Verify Message Content Intent is enabled in Discord Developer Portal
- ✅ Check `logs/bot.log` for errors

#### Birthday Role Not Working

**Problem:** Birthday role not assigned

**Solutions:**
- ✅ Check `birthday_role_id` in `config.json` is correct
- ✅ Ensure bot role is **above** birthday role
- ✅ Verify role names match format: "15th January", "3rd March", etc.
- ✅ Bot needs `Manage Roles` permission

### Getting Help

1. **Check logs:** `logs/bot.log` has detailed error messages
2. **Enable debug mode:** See [Debugging](#debugging) section
3. **Search issues:** Check GitHub issues for similar problems
4. **Create issue:** Include:
   - Error message from logs
   - Steps to reproduce
   - Python version
   - discord.py version

---

## 🎯 Best Practices

### Security

- ❌ **Never commit** `config.json` with real tokens to Git
- ✅ Add to `.gitignore`:
  ```
  config.json
  data/
  logs/
  __pycache__/
  *.pyc
  ```
- ✅ Use environment variables for production
- ✅ Regularly rotate bot token if leaked
- ✅ Limit bot permissions to only what's needed

### Performance

- ✅ Use `defer()` for commands that take time
- ✅ Limit database queries in loops
- ✅ Cache frequently accessed data
- ✅ Use pagination for large result sets

### Code Quality

- ✅ Follow PEP 8 style guidelines
- ✅ Add docstrings to all functions
- ✅ Use type hints for parameters
- ✅ Handle errors gracefully with try/except
- ✅ Log important events and errors

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Test thoroughly
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Contribution Guidelines

- ✅ Test all changes before submitting
- ✅ Update documentation for new features
- ✅ Follow existing code structure
- ✅ One feature per pull request
- ✅ Describe changes clearly in PR

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 GXTHICKITTY

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
