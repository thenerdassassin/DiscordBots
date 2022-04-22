import requests
import time
import config
from discord_webhook import DiscordWebhook, DiscordEmbed

#import discord
#from discord.ext import tasks, commands

# Use OpenSea API to retrieve events from startTime to endTime (in Unix epoch) for a single Contract Address
def getEvents(startTime, endTime, contractAddress):
    url = f'https://api.opensea.io/api/v1/events?only_opensea=true&asset_contract_address={contractAddress}&event_type=created&occurred_after={startTime}&occurred_before={endTime}'

    if config.api_key != "":
        headers = {
            "Accept": "application/json",
            "X-API-KEY": config.api_key
        }
    else:
        headers = {
            "Accept": "application/json"
        }

    return requests.request("GET", url, headers=headers).json()

# Convert OpenSea price to ETH in String format, i.e. 3.2 Ξ
def convertPriceToETH(price):
    return f'{float(float(price)/1000000000000000000.0):g} Ξ'

# Parse OpenSea Event for name of the asset
# See: https://docs.opensea.io/reference/asset-object
def getTitleFromEvent(event):
    return event.get("asset").get("name")

# Parse OpenSea Event to create a discord Embed
# See: https://discordpy.readthedocs.io/en/stable/api.html#embed
def convertEventToEmbed(event):
    embedTitle = f'{getTitleFromEvent(event)} was listed!'
    embed = DiscordEmbed(title=embedTitle, url=event.get("asset").get("permalink"))
    embed.set_image(url=event.get("asset").get("image_original_url"))
    embed.add_embed_field(name="List Price", value=convertPriceToETH(event.get("ending_price")), inline=False)
    return embed

### Commenting but keeping async code
# # Retrieve OpenSea events and send Discord embed to channel
# async def sendLatestEvents(channel, contractAddress, startTime, endTime):
#     currentEvents = getEvents(startTime, endTime, contractAddress)
#     for event in currentEvents['asset_events']:
#         print(f'Found listing for {getTitleFromEvent(event)}')
#         time.sleep(2)
#         embed = convertEventToEmbed(event)
#         await channel.send(embed=embed)


# async def get_and_send_messages():
#     current_time = time.time()
#     start_time = current_time - int(config.update_interval)*60
#     channel = client.get_channel(int(config.channel_id))
#     for collection in config.collection_addresses:
#         print(f'Getting Listings for {collection}')
#         await sendLatestEvents(channel, collection, start_time, current_time)
#     start_time = current_time

# client = commands.Bot(command_prefix=config.prefix, description=config.description)
        

def run_bot_sync():
    # Timer & Client set up
    end_time = time.time()
    start_time = end_time - int(config.update_interval)*60
    webhook = DiscordWebhook(url=config.webhook_url)
    
    for collection in config.collection_addresses:
        #Get Listings
        print(f'Getting Listings for {collection}')
        currentEvents = getEvents(start_time, end_time, collection)

        #Deduplicate, take most recent
        nfts_to_report = []
        unique_names = list(set([ x['asset']['name'] for x in currentEvents['asset_events']]))
        for n in unique_names:
            nfts_to_report.append([x for x in currentEvents['asset_events'] if x['asset']['name'] == n][-1])
        

        #Send via Webhook        
        for event in nfts_to_report:
            print(f'Found listing for {getTitleFromEvent(event)}')
            embed = convertEventToEmbed(event)
            webhook.add_embed(embed)
            resp = webhook.execute()
            time.sleep(1)
