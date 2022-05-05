import datetime
import logging
import eventbot

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # Get Listings
    eventbot.run_bot_sync('created')
    # Get Sales
    eventbot.run_bot_sync('successful')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
