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
   - Enable "Message Content Intent" 
   - Copy bot token

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