import time
from helpers import can_be_int, get_constant_value
from user import user_exists


async def make_all_cards_from_data(db, message, client):

    card_admin_data = get_constant_value(db, 'card_admin_data')

    for team_name in card_admin_data['teams_in_data']:

        team_data = card_admin_data['teams_in_data'][team_name]
        for player_data in team_data:

            user_id = player_data['player_id']
            
            display_cards = db['display_cards']
            num_displays = display_cards.count_documents({})
            new_id = num_displays + 1

            new_obj = {
                'player_id': user_id,
                'normal_img': player_data['normal_img'],
                'special_img': player_data['special_img'],
                'card_id': new_id
            }

            #display_cards.insert_one(new_obj)
            print(new_obj)

            await message.channel.send('New card added with ID of **'+str(new_id)+'**')

            time.sleep(1)

    await message.channel.send('all them cards done boss')


