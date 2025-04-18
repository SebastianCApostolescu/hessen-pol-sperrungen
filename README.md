# Hessen Traffic Information

This project provides tools to monitor road closures in Hessen, Germany, using the official Hessen Police API.

## Features

1. Command-line tool to check current road closures
2. Discord bot that sends alerts for new road closures

## Requirements

- Python 3.6 or higher
- Required packages are listed in `requirements.txt`

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Command-line Tool

To check current road closures:
```bash
python traffic_info.py
```

### Discord Bot

1. First, you need to create a Discord bot:
   - Go to https://discord.com/developers/applications
   - Click "New Application"
   - Go to the "Bot" section and create a bot
   - Copy the bot token

2. Configure the bot:
   - Open `traffic_bot.py`
   - Replace `YOUR_DISCORD_TOKEN_HERE` with your bot token
   - Replace `CHANNEL_ID` with the ID of the channel where you want to receive alerts
     (To get the channel ID, enable Developer Mode in Discord settings, then right-click the channel and click "Copy ID")

3. Run the bot:
```bash
python traffic_bot.py
```

The bot will:
- Check for new road closures every 5 minutes
- Send alerts to the specified channel when new closures are detected
- Use a cache file to track known closures
- Format messages with embeds for better readability

## Data Source

The data is fetched from the official Hessen Police API:
https://webapi.polizei.hessen.de/api/traffic/ 