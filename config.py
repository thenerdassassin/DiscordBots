import os

# Create a bot application and get its token at the Discord Developer Portal.
# Follow this guide if you need help: https://www.writebots.com/discord-bot-token/
# Make sure to enable both privileged intents on the bot tab.
# This is also how you will invite the bot to your server.

token = os.getenv("DISCORD_BOT_TOKEN")

# For post-only bots that post to a single channel, a webhook can be a simpler method
webhook_url = os.getenv("WEBHOOK_URL")

# Command prefix
prefix = ""

# Bot description shown in the help menu
description = ""

# ID of the guild
# To find this, go to your discord settings > advanced > enable developer mode
# Then, right click the guild picture on the left sidebar and click copy ID
guild_id = 896049791656689664

# Time (in minutes) between checking for new sales
# All sales are always sent, no matter how often we check
update_interval = 60

# OpenSea API key. Get yours here https://docs.opensea.io/reference/request-an-api-key

api_key = os.getenv("OPENSEA_API_KEY")

# Channel to send listings messages in
# To find this, go to your discord settings > advanced > enable developer mode
# Then, right click the channel name on the left sidebar and click copy ID
channel_id = 966539982892310538

# Contract Address
# To find this, go to the OpenSea page for the collection and click on the Etherscan button.
# Then, next to the Contract Address, click copy.
collection_addresses =["0x2D0Ee46b804f415Be4dC8aa1040834F5125EBD2E", "0xE11AfbB703dC6c8c717ccEBA526d9568015e43D9"]