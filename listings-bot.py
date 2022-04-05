import requests
import time
import config
import discord
from discord.ext import tasks, commands

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
    embed = discord.Embed(title=embedTitle, url=event.get("asset").get("permalink"))
    embed.set_image(url=event.get("asset").get("image_original_url"))
    embed.add_field(name="List Price", value=convertPriceToETH(event.get("ending_price")), inline=False)
    return embed

# Retrieve OpenSea events and send Discord embed to channel
async def sendLatestEvents(channel, contractAddress, startTime, endTime):
    currentEvents = getEvents(startTime, endTime, contractAddress)
    for event in currentEvents['asset_events']:
        print(f'Found listing for {getTitleFromEvent(event)}')
        time.sleep(2)
        embed = convertEventToEmbed(event)
        await channel.send(embed=embed)

client = commands.Bot(command_prefix=config.prefix, description=config.description)

# Initialize the tasks loop when ready.
@client.event
async def on_ready():
    print('Bot is Ready!')
    send_messages.start()

# On loop timer, send listings to Discord
@tasks.loop(minutes=config.update_interval)
async def send_messages():
    global last_run
    global current_time
    current_time = time.time()
    channel = client.get_channel(config.channel_id)
    for collection in config.collection_addresses:
        print(f'Getting Listings for {collection}')
        await sendLatestEvents(channel, collection, last_run, current_time)
    last_run = current_time

# Client and timer set up
last_run = time.time()
current_time = time.time()
client.run(config.token)