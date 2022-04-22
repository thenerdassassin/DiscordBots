import datetime
import logging
import listingsbot

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    listingsbot.run_bot_sync()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
