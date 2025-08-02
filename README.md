# Discord Idiots Summarizer 🤖

Simple Discord bot that creates sassy AI summaries of your server's daily chaos and posts them back to Discord.

## Setup

1. **Create conda environment:**
   ```bash
   conda create -n discord_idiots python=3.11
   conda activate discord_idiots
   pip install -r requirements.txt
   ```

2. **Set up Discord Bot:**
   - Go to Discord Developer Portal
   - Create application/bot
   - Navigate to Bot tab
   - Enable "Message Content Intent" (under Privileged Gateway Intents)
   - Copy bot token (click "Reset Token" under Token header)
   - Navigate to OAuth2 tab
   - Select these scopes: bot, applications.commands
   - Select these bot permissions: View Channels, Send Messages, Read Message History
   - Copy the Generated URL towards bottom of page
   - Paste that into web broswer and invite bot to desired server

3. **Get OpenAI API key** from platform.openai.com

4. **Edit the script:**
   ```bash
   nano simple_summarizer.py
   ```
   Put your tokens at the top:
   ```python
   DISCORD_TOKEN = "your_bot_token_here"
   OPENAI_KEY = "your_openai_key_here"
   ```

## Usage

```bash
conda activate discord_idiots
python simple_summarizer.py
```

The bot will:
- Read last 24 hours from #general, #dank-memes, #autism, #stocks-and-finance
- Generate a sassy AI summary
- Post it back to Discord in #general

That's it! 🎪