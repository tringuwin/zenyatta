import time
import discord
import asyncio
from admin_handlers.gen_bracket import gen_bracket_handler
from command_handlers.donate import donate_handler
from command_handlers.donate_pass import donate_pass_handler
from command_handlers.fun_fact import fun_fact_handler
from command_handlers.gift import gift_handler
from command_handlers.hello import hello_handler
from command_handlers.suggest_event import suggest_event_handler
from command_handlers.teams.del_team_from_event import del_team_from_event_handler
from command_handlers.teams.get_teams import get_teams_handler
import constants
import traceback
from admin_handlers.add_event import add_event_handler
from admin_handlers.close_event import close_event_handler
from admin_handlers.delete_event import delete_event_handler
from admin_handlers.delete_item import delete_item_handler
from admin_handlers.edit_item_name import edit_item_name_handler
from admin_handlers.make_public import make_public_handler
from admin_handlers.make_shop import make_shop_handler
from admin_handlers.prune_team_event import prune_team_event_handler
from admin_handlers.set_stock import set_stock_handler
from admin_handlers.total_tokens import total_tokens_handler
from admin_handlers.update_shop import update_shop_handler
from admin_handlers.wipe_teams import wipe_teams_handler
from admin_handlers.add_item import add_item_handler
from command_handlers.battle import battle_handler
from command_handlers.buy import buy_handler
from command_handlers.events import events_handler
from command_handlers.join import join_handler
from command_handlers.teams.accept_invite import accept_invite_handler
from command_handlers.teams.delete_team import delete_team_handler
from command_handlers.teams.deny_invite import deny_invite_handler
from command_handlers.teams.help_teams import help_teams_handler
from command_handlers.teams.invite import invite_handler
from command_handlers.teams.kick_player import kick_player_handler
from command_handlers.teams.leave_team import leave_team_handler
from command_handlers.teams.my_invites import my_invites_handler
from command_handlers.teams.make_team import make_team_handler
from command_handlers.hatch import hatch_handler
from command_handlers.help import help_hanlder
from command_handlers.teams.team_details import team_details_hanlder
from command_handlers.teams.team_join import team_join_handler
from command_handlers.teams.teams import teams_handler
from command_handlers.wager import twager_handler, wager_handler
from bracket import both_no_show, gen_tourney, no_show, notify_next_users, send_next_info, wipe_tourney, won_match
from discord_actions import get_guild, get_member_by_username, is_dm_channel
from mongo import output_eggs, output_passes, output_tokens, switch_matches
from notifs import handle_notifs
from rewards import give_eggs_command, give_passes_command, change_tokens, give_tokens_command, sell_pass_for_tokens
from user import get_user_passes, get_user_tokens, user_exists



async def handle_message(message, db, client):

    user_message = str(message.content)
    is_command = len(user_message) > 0 and (user_message[0] == '!')
    if not is_command:
        return
    
    channel = str(message.channel)
    lower_message = user_message.lower()

    is_admin = (message.author.id == constants.SPICY_RAGU_ID)

    valid_channel = is_admin or is_dm_channel(message.channel) or message.channel.id == constants.BOT_CHANNEL or (message.channel.id == constants.CASINO_CHANNEL and (lower_message.startswith('!wager') or lower_message.startswith('!twager')))
    if (not valid_channel) and (message.channel.id == constants.CASINO_CHANNEL and lower_message == '!tokens'):
        valid_channel = True

    if not valid_channel:
        
        await message.delete()
        warning = await message.channel.send(message.author.mention+" Please only use commands in #bot-commands or in a Direct Message with me.")

        time.sleep(10)
        await warning.delete()
        return
    

    if lower_message == '!help':
        await help_hanlder(message)
    
    elif lower_message.startswith('!battle '):
        await battle_handler(db, message, client)

    elif lower_message == "!events":
        await events_handler(db, message)

    elif lower_message.startswith("!join "):
        await join_handler(db, message, client)
    
    elif lower_message.startswith("!suggestevent "):
        await suggest_event_handler(message, client)

    elif lower_message == "!tokens":
        await output_tokens(db, message)

    elif lower_message == "!passes":
        await output_passes(db, message)

    elif lower_message == "!eggs":
        await output_eggs(db, message)

    elif lower_message == "!sellpass":
        await sell_pass_for_tokens(db, message)

    elif lower_message == '!dailygift' or lower_message == '!gift':
        await gift_handler(db, message)

    elif lower_message.startswith('!funfact '):
        await fun_fact_handler(db, message)

    elif lower_message == "!hello":
        await hello_handler(message)

    elif lower_message == '!hatch':
        await hatch_handler(db, message)

    elif lower_message.startswith('!wager'):
        await wager_handler(db, message)

    elif lower_message.startswith('!twager'):
        await twager_handler(db, message)

    elif lower_message.startswith('!buy'):
        await buy_handler(db, message)

    elif lower_message.startswith('!donate '):
        await donate_handler(db, message)

    elif lower_message.startswith('!donatepass'):
        await donate_pass_handler(db, message)

    # TEAM COMMANDS

    elif lower_message == '!teams':
        await teams_handler(db, message)

    elif lower_message.startswith('!getteams ') and is_admin:
        await get_teams_handler(db, message)

    elif lower_message.startswith('!teamdetails'):
        await team_details_hanlder(db, message)

    elif lower_message.startswith('!maketeam'):
        await make_team_handler(db, message)

    elif lower_message.startswith('!invite'):
        await invite_handler(db, message)

    elif lower_message == '!myinvites':
        await my_invites_handler(db, message)

    elif lower_message.startswith('!acceptinvite '):
        await accept_invite_handler(db, message)

    elif lower_message.startswith('!denyinvite'):
        await deny_invite_handler(db, message)

    elif lower_message.startswith('!leaveteam'):
        await leave_team_handler(db, message)

    elif lower_message.startswith('!deleteteam'):
        await delete_team_handler(db, message)

    elif lower_message.startswith('!teamjoin'):
        await team_join_handler(client, db, message)

    elif lower_message.startswith('!kickplayer'):
        await kick_player_handler(db, message)

    elif lower_message.startswith('!helpteams'):
        await help_teams_handler(message)

    elif lower_message.startswith('!delteamfromevent') and is_admin:
        await del_team_from_event_handler(db, message)

    # ADMIN COMMANDS

    elif lower_message.startswith("!addevent") and is_admin:
        # !addevent|[event id]|[event name]|[max participants]|[0 for no pass, 1 for pass]|[team size]|[event role id]
        await add_event_handler(db, message)

    elif lower_message.startswith("!delevent") and is_admin:
        # !delevent [event id]
        await delete_event_handler(db, message)

    elif lower_message.startswith('!pruneteamevent') and is_admin:
        await prune_team_event_handler(db, message, client)
        

    elif lower_message.startswith("!genbracket ") and is_admin:
        # !genbracket [event id]
        await gen_bracket_handler(db, message)

    elif lower_message.startswith("!wipebrackets") and is_admin:
            
        brackets = db['brackets']
        brackets.delete_many({})
        await message.channel.send('Brackets have been wiped')

    elif lower_message.startswith("!switchmatches ") and is_admin:

        # !switchmatches [event id] [switch match id 1] [switch match id 2]
        word_list = message.content.split()
        if len(word_list) == 4:
            await switch_matches(db, message, word_list[1], word_list[2], word_list[3])
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message.startswith("!gentourney ") and is_admin:

        # !gentourney [event id]
        word_list = message.content.split()
        if len(word_list) == 2:
            await gen_tourney(db, word_list[1], message)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message == '!wipetourney' and is_admin:

        await wipe_tourney(db, message)

    elif lower_message == '!starttourney' and is_admin:

        guild = client.get_guild(constants.GUILD_ID)
        tourney_role = guild.get_role(constants.EVENT_ROLE)
        event_channel = client.get_channel(constants.EVENT_CHANNEL_ID)

        await send_next_info(db, message, guild, event_channel)

        await event_channel.send('**TOURNAMENT HAS STARTED** '+tourney_role.mention)
        await notify_next_users(db, guild, message, event_channel)

    elif lower_message == '!pausetourney' and is_admin:

        guild = client.get_guild(constants.GUILD_ID)
        tourney_role = guild.get_role(constants.EVENT_ROLE)
        event_channel = client.get_channel(constants.EVENT_CHANNEL_ID)

        await event_channel.send('**TOURNAMENT HAS PASUED** '+tourney_role.mention)

    elif lower_message.startswith('!win ') and is_admin:
        
        event_channel = client.get_channel(constants.EVENT_CHANNEL_ID)

        # !win [winner 1 or 2]
        word_list = message.content.split()
        if len(word_list) == 2:
            guild = client.get_guild(constants.GUILD_ID)
            await won_match(int(word_list[1]), message, db, guild, event_channel)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message.startswith('!noshow ') and is_admin:

        event_channel = client.get_channel(constants.EVENT_CHANNEL_ID)

        # !noshow [loser 1 or 2]
        word_list = message.content.split()
        if len(word_list) == 2:
            guild = client.get_guild(constants.GUILD_ID)
            await no_show(int(word_list[1]), message, db, guild, event_channel)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message == '!bothnoshow' and is_admin:

        event_channel = client.get_channel(constants.EVENT_CHANNEL_ID)
        guild = client.get_guild(constants.GUILD_ID)

        await both_no_show(message, db, guild, event_channel)

    elif lower_message.startswith('!giverewards') and is_admin:
        
        reward_per_round = [10, 10, 100, 200, 500, 0, 0]

        bracket = db['brackets'].find_one({'event_id': '2'})

        final_dict = {}

        round_index = 0
        for round in bracket['bracket']:
            for match in round:
                
                for player in match:
                    if 'no_show' in player:
                        final_dict[str(player['user'])] = -1
                    elif not (player['is_bye']) or (player['is_tbd']):
                        final_dict[str(player['user'])] = round_index

            round_index += 1

        for player_id_string, highest_round in final_dict.items():

            if highest_round > -1:
                user = db['users'].find_one({'discord_id': int(player_id_string)})
                if user:

                    reward = reward_per_round[highest_round]
                    await change_tokens(db, user, reward)

        await message.channel.send('Rewards given')

        
    elif lower_message.startswith('!givetokens ') and is_admin:

        # !givetokens [winner id] [tokens]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_tokens_command(client, db, word_list[1], int(word_list[2]), message)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message.startswith('!givepasses ') and is_admin:

        # !givepasses [winner id] [passes]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_passes_command(client, db, word_list[1], int(word_list[2]), message)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message.startswith('!giveeggs ') and is_admin:

        # !giveeggs [winner id] [eggs]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_eggs_command(db, int(word_list[1]), int(word_list[2]), message)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message == '!listids' and is_admin:

        for member in client.get_all_members():

            user = user_exists(db, member.id)
            if user:

                print(member.display_name+" : "+str(member.id) + " : "+user['battle_tag'])

    elif lower_message.startswith('!getdetails ') and is_admin:

        # !getdetails [username]
        word_list = message.content.split()
        if len(word_list) == 2:
            
            member = await get_member_by_username(client, word_list[1])
            user = user_exists(db, member.id)
            if user:
                final_string = 'User ID: '+str(member.id)+"\nBattle Tag: "+user['battle_tag']
                final_string += '\nTokens: '+str(get_user_tokens(user))+'\n'+'Passes: '+str(get_user_passes(user))
                await message.channel.send(final_string)

            
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message == '!wipeteams' and is_admin:
        await wipe_teams_handler(db, message)
    elif lower_message == '!totaltokens' and is_admin:
        await total_tokens_handler(db, message)
    elif lower_message == '!makeshop' and is_admin:
        await make_shop_handler(db, message)
    elif lower_message.startswith('!additem') and is_admin:
        await add_item_handler(db, message)
    elif lower_message.startswith('!delitem') and is_admin:
        await delete_item_handler(db, message)
    elif lower_message == '!updateshop' and is_admin:
        await update_shop_handler(db, message)
    elif lower_message.startswith('!edititemname') and is_admin:
        await edit_item_name_handler(db, message)
    elif lower_message.startswith('!makepublic') and is_admin:
        await make_public_handler(db, message)
    elif lower_message.startswith('!closeevent') and is_admin:
        await close_event_handler(db, message)
    elif lower_message.startswith('!setstock') and is_admin:
        await set_stock_handler(db, message)
    elif lower_message.startswith('!say') and is_admin:
        
        rest = message.content[len("!say "):].strip()
        guild = await get_guild(client)
        chat_channel = guild.get_channel(constants.CHAT_CHANNEL)
        await chat_channel.send(rest)

    elif lower_message == '!testerror' and is_admin:

        test = {
            'test': 1
        }
        test2 = test['test2']

    elif lower_message == '!makereactionroles' and is_admin:

        reaction_roles = [
            
            {
                'title': 'Gift Notifications',
                'id': constants.GIFT_ROLE_ID,
                'extra': 'If you have this role you will be messaged by the bot when your daily gift is ready. This will not work if you are not registered.'
            }
        ]
            
        guild = await get_guild(client)
        channel = guild.get_channel(1143592783999926404)
        for role in reaction_roles:
            discord_role = guild.get_role(role['id'])
            
            message = await channel.send('Add an emoji reaction to get the '+discord_role.mention+ ' role. Remove the reaction to remove it. Default is **OFF**.\n*'+role['extra']+'*')
            await message.add_reaction("✅")

    else:
        await message.channel.send('Invalid command. Please see **!help** for a list of commands.')


async def check_database_and_send_messages(db, client):
    while True:
        
        await handle_notifs(db, client)
        await asyncio.sleep(60)

def run_discord_bot(db):
    intents = discord.Intents.all()
    intents.message_content = True
    intents.reactions = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))

        client.loop.create_task(check_database_and_send_messages(db, client))

    @client.event
    async def on_raw_reaction_add(payload):

        message_id = payload.message_id
        member = payload.member
        if message_id == constants.SERVER_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.SERVER_NOTIFS_ROLE)
            await member.remove_roles(role)
        elif message_id ==  constants.TOURNEY_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
            await member.remove_roles(role)
        elif message_id ==  constants.TWITCH_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.TWITCH_NOTIFS_ROLE)
            await member.remove_roles(role)
        elif message_id ==  constants.GIFT_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.GIFT_ROLE_ID)
            await member.add_roles(role)

    @client.event
    async def on_raw_reaction_remove(payload):
        guild = await get_guild(client)
        message_id = payload.message_id
        user_id = payload.user_id
        member = guild.get_member(user_id)
        if message_id == constants.SERVER_NOTIF_MSG:
            role = guild.get_role(constants.SERVER_NOTIFS_ROLE)
            await member.add_roles(role)
        elif message_id ==  constants.TOURNEY_NOTIF_MSG:
            role = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
            await member.add_roles(role)
        elif message_id ==  constants.TWITCH_NOTIF_MSG:
            role = guild.get_role(constants.TWITCH_NOTIFS_ROLE)
            await member.add_roles(role)
        elif message_id ==  constants.GIFT_NOTIF_MSG:
            role = guild.get_role(constants.GIFT_ROLE_ID)
            await member.remove_roles(role)

    @client.event
    async def on_member_join(member):
        guild = client.get_guild(constants.GUILD_ID)
        role = guild.get_role(constants.MEMBER_ROLE_ID)
        server_notifs = guild.get_role(constants.SERVER_NOTIFS_ROLE)
        tourney_notifs = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
        twitch_notifs = guild.get_role(constants.TWITCH_NOTIFS_ROLE)

        if role is not None:
            await member.add_roles(role, server_notifs, tourney_notifs, twitch_notifs)


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        try:
            await handle_message(message, db, client)
        except Exception as e:
            print(e)
            traceback.print_exc()
            guild = client.get_guild(constants.GUILD_ID)
            spicy_member = guild.get_member(constants.SPICY_RAGU_ID)
            await message.channel.send('Whoops... An error occured. Let me notify staff. '+spicy_member.mention)
            err_channel = guild.get_channel(constants.ERROR_LOGS_CHANNEL)
            print(e)
            await err_channel.send(e)
            traceback_str = traceback.format_exc()
            await err_channel.send(traceback_str)



    client.run(constants.DISCORD_TOKEN)