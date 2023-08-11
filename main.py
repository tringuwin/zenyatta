import bot

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://loganstanford53:cMczqREMdzhQR9T6@cluster0.o9naf24.mongodb.net/?retryWrites=true&w=majority"




async def main():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = None
    try:
        print('trying ping command')
        client.admin.command('ping')
        print('Pinged deployment!')
        db = client['spicyragu']

        # users = db['users']
        # users.delete_many({})
        # events = db['events']
        # events.delete_many({})

        
    except Exception as e:
        print(e)

    print(db)
    await bot.run_discord_bot(client, db)

if __name__ == '__main__':

    main()