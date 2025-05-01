import discord
from discord.ext import tasks
import asyncio
import json
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
from traffic_info import fetch_traffic_info, format_date, get_time_value

# Load environment variables
load_dotenv()

# Store the last known state of closures
CACHE_FILE = 'closure_cache.json'
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID', 0))

def truncate_text(text, max_length=1024):
    """Truncate text to specified length, adding ellipsis if truncated"""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text

class TrafficBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.known_closures = self.load_cache()

    async def setup_hook(self):
        # Start the background task
        self.check_traffic_updates.start()

    def load_cache(self):
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
        return {}

    def save_cache(self):
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.known_closures, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def get_closure_key(self, item):
        """Create a unique key for a closure based on its properties"""
        location = item.get('location', {}).get('description', '')
        desc = item.get('description', [{}])[0].get('value', '')
        return f"{location}:{desc}"

    @tasks.loop(minutes=5)  # Check every 5 minutes
    async def check_traffic_updates(self):
        try:
            data = fetch_traffic_info()
            if not data or 'data' not in data:
                return

            current_closures = {}
            new_closures = []
            removed_closures = []

            # Process current closures
            for item in data['data']:
                descriptions = item.get('description', [])
                if not descriptions:
                    continue

                desc = descriptions[0].get('value', '')
                
                # Check specifically for road closures
                if any(keyword in desc.lower() for keyword in ['gesperrt', 'sperrung']):
                    closure_key = self.get_closure_key(item)
                    current_closures[closure_key] = item

                    # Check if this is a new closure
                    if closure_key not in self.known_closures:
                        new_closures.append(item)

            # Check for removed closures
            for closure_key in self.known_closures:
                if closure_key not in current_closures:
                    removed_closures.append(self.known_closures[closure_key])

            # Send alerts for new closures
            if new_closures and self.is_ready():
                channel = self.get_channel(CHANNEL_ID)
                if channel:
                    for item in new_closures:
                        location = item.get('location', {}).get('description', 'Location not specified')
                        desc = item.get('description', [{}])[0].get('value', 'No description available')
                        duration = item.get('duration', {})
                        start_time = get_time_value(duration, 'startTime')
                        end_time = get_time_value(duration, 'endTime')

                        # Ensure no empty values and truncate if needed
                        if not location.strip():
                            location = 'Location not specified'
                        if not desc.strip():
                            desc = 'No description available'
                        if not start_time:
                            start_time = 'Not specified'
                        if not end_time:
                            end_time = 'Not specified'

                        # Truncate long descriptions
                        desc = truncate_text(desc)
                        location = truncate_text(location)

                        embed = discord.Embed(
                            title="🚨 New Road Closure Alert",
                            color=discord.Color.red(),
                            timestamp=datetime.now(pytz.timezone('Europe/Berlin'))
                        )
                        embed.add_field(name="Location", value=location, inline=False)
                        embed.add_field(name="Description", value=desc, inline=False)
                        embed.add_field(name="Start", value=format_date(start_time), inline=True)
                        embed.add_field(name="End", value=format_date(end_time), inline=True)

                        await channel.send(embed=embed)

            # Send alerts for removed closures
            if removed_closures and self.is_ready():
                channel = self.get_channel(CHANNEL_ID)
                if channel:
                    for item in removed_closures:
                        location = item.get('location', {}).get('description', 'Location not specified')
                        desc = item.get('description', [{}])[0].get('value', 'No description available')

                        # Ensure no empty values and truncate if needed
                        if not location.strip():
                            location = 'Location not specified'
                        if not desc.strip():
                            desc = 'No description available'

                        # Truncate long descriptions
                        desc = truncate_text(desc)
                        location = truncate_text(location)

                        embed = discord.Embed(
                            title="✅ Road Closure Removed",
                            color=discord.Color.green(),
                            timestamp=datetime.now(pytz.timezone('Europe/Berlin'))
                        )
                        embed.add_field(name="Location", value=location, inline=False)
                        embed.add_field(name="Description", value=desc, inline=False)

                        await channel.send(embed=embed)

            # Update known closures
            self.known_closures = current_closures
            self.save_cache()

        except Exception as e:
            print(f"Error checking traffic updates: {e}")

    @check_traffic_updates.before_loop
    async def before_check_traffic_updates(self):
        await self.wait_until_ready()

    async def on_ready(self):
        print(f'Bot is ready! Logged in as {self.user}')
        print(f'Monitoring traffic updates for channel ID: {CHANNEL_ID}')

def main():
    # Create bot instance
    client = TrafficBot()
    
    # Run the bot
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main() 