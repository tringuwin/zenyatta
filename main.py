import bot
import constants
import stripe

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


if __name__ == '__main__':

    client = MongoClient(constants.MONGO_URI, server_api=ServerApi('1'))
    db = None
    try:
        print('trying ping command')
        client.admin.command('ping')
        print('Pinged deployment!')
        db = client['spicyragu']
        
    except Exception as e:
        print(e)

    # In-memory store for tracking purchases (use DB for production)
    user_sessions = {}

    bot.run_discord_bot(db, user_sessions)