from dotenv import load_dotenv
import os

import bot
import constants

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


if __name__ == '__main__':

    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = None

    try:
        print('trying ping command')
        client.admin.command('ping')
        print('Pinged deployment!')
        db = client['spicyragu']
        
    except Exception as e:
        print(e)

    bot.run_discord_bot(db)