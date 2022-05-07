import requests
import time
import config
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed

# Use OpenSea API to retrieve events from startTime to endTime (in Unix epoch) for a single Contract Address
def getEvents(startTime, endTime, contractAddress, eventType):
    print(startTime)
    url = f'https://api.opensea.io/api/v1/events?only_opensea=true&asset_contract_address={contractAddress}&event_type={eventType}&occurred_after={startTime}&occurred_before={endTime}'

    if config.api_key != "":
        headers = {
            "Accept": "application/json",
            "X-API-KEY": config.api_key
        }
    else:
        headers = {
            "Accept": "application/json"
        }

    return requests.request("GET", url, headers=headers)


# Convert OpenSea price to ETH in String format, i.e. 3.2 Ξ
def convertPriceToETH(price):
    return f'{float(float(price)/1000000000000000000.0):g} Ξ'

# Parse OpenSea Event for name of the asset
# See: https://docs.opensea.io/reference/asset-object
def getTitleFromEvent(event):
    return event.get("asset").get("name")

# Parse OpenSea Event to create a discord Embed
# See: https://discordpy.readthedocs.io/en/stable/api.html#embed
def convertEventToEmbed(event, eventType):
    if (eventType == 'successful'):
        embedTitle = f'Dapper Dino {getTitleFromEvent(event)} was purchased!'
    elif (eventType == 'created'):
        embedTitle = f'{getTitleFromEvent(event)} was listed!'
    embed = DiscordEmbed(title=embedTitle, url=event.get("asset").get("permalink"))
    embed.set_image(url=event.get("asset").get("image_original_url"))

    if (eventType == 'successful'):
        embed.add_embed_field(name="Sale Price", value=convertPriceToETH(event.get("total_price")), inline=False)
    elif (eventType == 'created'):
        embed.add_embed_field(name="List Price", value=convertPriceToETH(event.get("ending_price")), inline=False)

    return embed
        

def run_bot_sync(eventType):
    # Timer & Client set up
    end_time = time.time()
    start_time = end_time - int(config.update_interval)*60
    webhook = DiscordWebhook(url=config.webhook_url.get(eventType))
    
    for collection in config.collection_addresses:
        #Get Listings
        print(f'Getting {eventType} events for {collection}')
        currentEvents = getEvents(start_time, end_time, collection, eventType)
        if (currentEvents.status_code != 200):
            print("Error with OpenSea request.")
            print(currentEvents.status_code)
            print(currentEvents.reason)
            return
        currentEvents = currentEvents.json()

        #Send via Webhook        
        for event in currentEvents['asset_events']:
            print(f'Found {eventType} event for {getTitleFromEvent(event)}')
            embed = convertEventToEmbed(event, eventType)
            webhook.add_embed(embed)
            webhook.execute()
            webhook.embeds = [] # Prevents duplication
            time.sleep(1)