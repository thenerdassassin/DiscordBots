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


# Convert OpenSea price to ETH in String format, i.e. Ξ3.2 
def convertPriceToETH(price):
    return f'Ξ{float(float(price)/1000000000000000000.0):g}'

# Parse OpenSea Event for name of the asset
# See: https://docs.opensea.io/reference/asset-object
def getTitleFromEvent(event):
    return event.get("asset").get("name")

def getUsernameFromEvent(event, userKey):
    username = event.get(userKey).get("user").get("username")
    userProfileLink = f'https://opensea.io/{event.get(userKey).get("address")}'
    if (username):
        return f'[{username}]({userProfileLink})'
    

    return f'[Unnamed]({userProfileLink})'

# Parse OpenSea Event for the link to the asset
# See: https://docs.opensea.io/reference/asset-object
def getLinkToOpenSea(event):
    return event.get("asset").get("permalink")

# Parse OpenSea Event to create an Embed with title, description,
# and url. See: https://discordpy.readthedocs.io/en/stable/api.html#embed
def createEmbed(event, eventType):
    if (eventType == 'successful'):
        return DiscordEmbed(
            title=f'{getTitleFromEvent(event)} was purchased!', 
            description=f'Amount {convertPriceToETH(event.get("total_price"))}',
            url=getLinkToOpenSea(event)
        )
    elif (eventType == 'created'):
        return DiscordEmbed(
            title=f'{getTitleFromEvent(event)} was listed!', 
            description=f'Amount {convertPriceToETH(event.get("starting_price"))}',
            url=getLinkToOpenSea(event)
        )

# Parse OpenSea Event to create a discord Embed
# See: https://discordpy.readthedocs.io/en/stable/api.html#embed
def convertEventToEmbed(event, eventType):
    embed = createEmbed(event, eventType)
    embed.set_image(url=event.get("asset").get("image_original_url"))

    if (eventType == 'successful'):
        embed.add_embed_field(name='Buyer', value=f'{getUsernameFromEvent(event, "winner_account")}', inline=True)

    embed.add_embed_field(name='Seller', value=f'{getUsernameFromEvent(event, "seller")}', inline=True)
    embed.add_embed_field(name='Link', value=f'[OpenSea]({getLinkToOpenSea(event)})', inline=True)

    return embed
        

def run_bot_sync(eventType):
    # Timer & Client set up
    end_time = time.time()
    start_time = end_time - int(config.update_interval)*60
    webhook = DiscordWebhook(url=config.webhook_url.get(eventType))
    
    for collection in config.collection_addresses:
        # Get Listings
        print(f'Getting {eventType} events for {collection}')
        currentEvents = getEvents(start_time, end_time, collection, eventType)
        if (currentEvents.status_code != 200):
            print("Error with OpenSea request.")
            print(currentEvents.status_code)
            print(currentEvents.reason)
            return
        currentEvents = currentEvents.json()

        # Send via Webhook        
        for event in currentEvents['asset_events']:
            # Skipping Bundles
            if (not event.get("asset")):
                continue
            print(f'Found {eventType} event for {getTitleFromEvent(event)}')
            embed = convertEventToEmbed(event, eventType)
            webhook.add_embed(embed)
            webhook.execute()
            webhook.embeds = [] # Prevents duplication
            time.sleep(1)