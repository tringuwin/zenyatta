
import bot
from mongo import init_mongo_db

if __name__ == '__main__':
    
    db = init_mongo_db()
    bot.run_discord_bot(db)