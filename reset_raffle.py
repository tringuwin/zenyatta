async def reset_raffle_handler(db, message):
        db_constants = db['constants']
        db_constants.update_one({"name": 'raffle_total'}, {"$set": {"value": 0}})

        users = db['users']
        all_users = users.find()

        for user in all_users:
            if 'tickets' in user:
                users.update_one({"discord_id": user['discord_id']}, {"$set": {"tickets": 0}})

        await message.channel.send('Raffle reset')