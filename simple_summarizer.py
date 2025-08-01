#!/usr/bin/env python3
"""
Simple Discord Summarizer - Just run this script!
"""

import discord
import asyncio
import openai
import os
from datetime import datetime, timedelta, timezone

# Get tokens from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

# Channels to summarize (just the names, no # needed)
CHANNELS = ['general', 'dank-memes', 'autism', 'stocks-and-finance']

# Channel to post the summary to (just the name, no # needed)
SUMMARY_CHANNEL = 'general'



async def collect_messages(client):
    """Collect messages from target channels in the last 24 hours"""
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    print(f"📅 Looking for messages since: {yesterday.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    all_messages = []
    
    for guild in client.guilds:
        print(f"🏠 Checking server: {guild.name}")
        for channel in guild.text_channels:
            if channel.name in CHANNELS:
                print(f"📖 Reading #{channel.name}...")
                try:
                    message_count = 0
                    async for message in channel.history(after=yesterday, limit=None):
                        if not message.author.bot:  # Skip bot messages
                            all_messages.append(f"{message.author.display_name}: {message.content}")
                            message_count += 1
                    print(f"   Found {message_count} messages")
                except Exception as e:
                    print(f"   ❌ Error reading #{channel.name}: {e}")
            else:
                print(f"   Skipping #{channel.name} (not in target channels)")
    
    print(f"📊 Total messages collected: {len(all_messages)}")
    return all_messages


def generate_ai_summary(messages):
    """Generate AI summary from collected messages"""
    if not messages:
        return "No messages found in the last 24 hours. The server was surprisingly quiet!"
    
    print(f"💬 Found {len(messages)} messages. Getting AI summary...")
    
    # Create prompt
    messages_text = "\n".join(messages[-200:])  # Last 200 messages to avoid token limits
    
    prompt = f"""You're summarizing Discord messages from some truly special individuals. 
Here are the messages:

{messages_text}

Format your response exactly like this:

## Summary
• [First key topic/event that happened]
• [Second key topic/event that happened]
• [Third key topic/event that happened]
• [Continue with other notable topics/events]

## Commentary
[Write exactly one paragraph of witty, sassy commentary about the conversations. Be entertaining with humor and light sarcasm, calling out funny moments and patterns, but keep it to just one paragraph.]"""
    
    # Get AI summary
    try:
        openai_client = openai.OpenAI(api_key=OPENAI_KEY)
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a witty Discord message summarizer with sass."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.8
        )
        
        summary = response.choices[0].message.content
        print("✅ AI summary generated!")
        return summary
        
    except Exception as e:
        print(f"❌ Error getting AI summary: {e}")
        return f"Error generating summary: {e}"


def save_summary_to_file(summary):
    """Save the summary to a text file"""
    filename = f"summary_{datetime.now().strftime('%Y-%m-%d')}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Discord Summary - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("="*50 + "\n\n")
        f.write(summary)
    
    print(f"📄 Summary saved to {filename}")
    print("\n" + "="*50)
    print(summary)
    print("="*50)
    
    return filename


async def post_summary_to_discord(client, summary):
    """Post the summary to the configured Discord channel"""
    print(f"📤 Looking for #{SUMMARY_CHANNEL} to post summary...")
    
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == SUMMARY_CHANNEL:
                print(f"📤 Posting summary to #{channel.name} in {guild.name}...")
                
                try:
                    # Format the message with proper Discord markdown
                    message = f"🤖 **Daily Discord Summary - {datetime.now().strftime('%Y-%m-%d')}**\n\n{summary}"
                    
                    # Discord has a 2000 character limit, so we might need to split long messages
                    if len(message) <= 2000:
                        await channel.send(message)
                        print("✅ Summary posted successfully!")
                    else:
                        # Split into multiple messages if too long
                        print("⚠️ Summary is long, splitting into multiple messages...")
                        
                        # Send header first
                        header = f"🤖 **Daily Discord Summary - {datetime.now().strftime('%Y-%m-%d')}**"
                        await channel.send(header)
                        
                        # Split the summary content
                        summary_parts = []
                        current_part = ""
                        
                        for line in summary.split('\n'):
                            if len(current_part + line + '\n') <= 1900:  # Leave some buffer
                                current_part += line + '\n'
                            else:
                                if current_part:
                                    summary_parts.append(current_part.strip())
                                current_part = line + '\n'
                        
                        if current_part:
                            summary_parts.append(current_part.strip())
                        
                        # Send each part
                        for i, part in enumerate(summary_parts):
                            await channel.send(part)
                            print(f"✅ Posted part {i+1}/{len(summary_parts)}")
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Failed to post to #{channel.name}: {e}")
                    return False
    
    print(f"❌ Could not find channel #{SUMMARY_CHANNEL} in any server")
    return False


async def run_bot():
    """Run the bot and collect data"""
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print("✅ Connected to Discord!")
        print(f"🤖 Bot is logged in as: {client.user} (ID: {client.user.id})")
        
        print(f"🌐 Connected to {len(client.guilds)} servers:")
        if len(client.guilds) == 0:
            print("   ❌ BOT IS NOT IN ANY SERVERS!")
            print("   You need to invite the bot to your Discord server first.")
            print("   Use this URL (replace YOUR_CLIENT_ID):")
            print("   https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=67584&scope=bot")
            await client.close()
            return
            
        for guild in client.guilds:
            print(f"   - {guild.name}")
        
        try:
            # Collect messages from target channels
            messages = await collect_messages(client)
            
            # Generate AI summary
            summary = generate_ai_summary(messages)
            
            # Save summary to file
            save_summary_to_file(summary)
            
            # Post summary to Discord
            await post_summary_to_discord(client, summary)
            
        except Exception as e:
            print(f"❌ Error during processing: {e}")
        
        finally:
            await client.close()
    
    print("🤖 Starting Discord Summarizer...")
    print("🔐 Connecting to Discord...")
    
    try:
        await client.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")

def main():
    """Main function - run the bot"""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_BOT_TOKEN environment variable not set!")
        print("Run: export DISCORD_BOT_TOKEN='your_bot_token'")
        exit(1)
    
    if not OPENAI_KEY:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Run: export OPENAI_API_KEY='your_openai_key'")
        exit(1)
    
    main()