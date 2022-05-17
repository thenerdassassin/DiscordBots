import os

# For post-only bots that post to a single channel, a webhook can be a simpler method
# Different Webhook URLs for different channels for OS Sales and Listings. From env variables.
webhook_url = {
    "successful":os.getenv("DISCORD_WEBHOOKURL_SALES"),
    "created": os.getenv("DISCORD_WEBHOOKURL_LISTINGS")
}

# Bot description shown in the help menu
description = ""

# ID of the guild
# To find this, go to your discord settings > advanced > enable developer mode
# Then, right click the guild picture on the left sidebar and click copy ID
guild_id = 0

# Time (in minutes) between checking for new sales
# All sales are always sent, no matter how often we check
update_interval = 5

# OpenSea API key. Get yours here https://docs.opensea.io/reference/request-an-api-key

api_key = os.getenv("OPENSEA_API_KEY")

# Channel to send listings messages in
# To find this, go to your discord settings > advanced > enable developer mode
# Then, right click the channel name on the left sidebar and click copy ID
channel_id = 0

# Contract Address
# To find this, go to the OpenSea page for the collection and click on the Etherscan button.
# Then, next to the Contract Address, click copy.
collection_addresses =["0x2D0Ee46b804f415Be4dC8aa1040834F5125EBD2E", "0xE11AfbB703dC6c8c717ccEBA526d9568015e43D9"]
