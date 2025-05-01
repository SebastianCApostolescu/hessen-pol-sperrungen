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

# Server Setup Instructions

## Option 1: Using System Python (Simpler)

1. Install dependencies globally:
```bash
sudo apt update
sudo apt install python3 python3-pip
sudo pip3 install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Discord token and channel ID
```

3. Make the management script executable:
```bash
chmod +x manage_bot.sh
```

4. Set up systemd service:
```bash
# Edit traffic-bot.service with your username and correct paths
sudo cp traffic-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable traffic-bot
sudo systemctl start traffic-bot
```

## Option 2: Using Virtual Environment (More Isolated)

1. Install Python and create virtual environment:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Discord token and channel ID
```

3. Make the management script executable:
```bash
chmod +x manage_bot.sh
```

4. Set up systemd service:
```bash
# Edit traffic-bot.service with your username and correct paths
# Make sure to update the paths to point to your virtual environment
sudo cp traffic-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable traffic-bot
sudo systemctl start traffic-bot
```

## Management Commands

Using the management script:
```bash
./manage_bot.sh start    # Start the bot
./manage_bot.sh stop     # Stop the bot
./manage_bot.sh restart  # Restart the bot
./manage_bot.sh status   # Check bot status
```

Using systemd:
```bash
sudo systemctl start traffic-bot
sudo systemctl stop traffic-bot
sudo systemctl restart traffic-bot
sudo systemctl status traffic-bot
```

## Logs

View systemd logs:
```bash
sudo journalctl -u traffic-bot -f
```

## Notes

- Option 1 (System Python) is simpler but installs packages globally
- Option 2 (Virtual Environment) provides better isolation but requires more setup
- Choose Option 1 if this is your only Python application
- Choose Option 2 if you have multiple Python applications with different dependencies 