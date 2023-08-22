import random
import time
import discord
from admin_handlers.close_event import close_event_handler
from admin_handlers.delete_item import delete_item_handler
from admin_handlers.edit_item_name import edit_item_name_handler
from admin_handlers.make_public import make_public_handler
from admin_handlers.make_shop import make_shop_handler
from admin_handlers.set_stock import set_stock_handler
from admin_handlers.total_tokens import total_tokens_handler
from admin_handlers.update_shop import update_shop_handler
from admin_handlers.wipe_teams import wipe_teams_handler
from admin_handlers.add_item import add_item_handler
from command_handlers.buy import buy_handler
from command_handlers.join import join_handler
from command_handlers.teams.accept_invite import accept_invite_handler
from command_handlers.teams.delete_team import delete_team_handler
from command_handlers.teams.deny_invite import deny_invite_handler
from command_handlers.teams.help_teams import help_teams_hanlder
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
from command_handlers.wager import wager_handler
import constants
import traceback
from bracket import both_no_show, gen_tourney, no_show, notify_next_users, send_next_info, wipe_tourney, won_match
from events import event_is_open, get_event_team_size
from mongo import add_fun_fact, approve_user, create_event, create_or_update_battle_tag, deny_user, find_user_with_battle_tag, generate_bracket, get_all_events, get_event_by_id, give_daily_gift, output_eggs, output_passes, output_tokens, switch_matches
from rewards import give_eggs_command, give_passes_command, change_tokens, give_tokens_command, sell_pass_for_tokens
from user import get_user_passes, get_user_tokens, user_exists


async def dm_user_register_info(author, message):

    await message.channel.send(author.mention+' Hi! Thanks for registering. Please use the !battle command in this channel to input your Battle Tag. (Hint: you can find and copy your Battle Tag in the Battle Net app.) **Command example: !battle SpicyRagu#1708**')

def is_dm_channel(channel):

    if isinstance(channel, discord.DMChannel):
        return True
    else:
        return False
    
async def register_battle_user(message, message_content, db):

    word_list = message_content.split()

    if len(word_list) == 2:
        
        battle_tag = word_list[1]
        print(battle_tag)
        
        if len(battle_tag) > 100:
            await message.channel.send('The battle tag you provided is not valid.')
        else:

            if '#' in battle_tag:
                
                lower_tag = battle_tag.lower()

                if find_user_with_battle_tag(db, lower_tag):
                    await message.channel.send("That Battle Tag has already been connected with a discord account. (Maybe you've already linked it?)")
                else:
                    create_or_update_battle_tag(db, battle_tag, lower_tag, message.author.id)
                    await message.channel.send("Success! Your Battle Tag has been linked to the SpicyRagu server! (Please note: if you change your Battle Tag please use the !battle command again to update it!)")
                    return True
            else:
                await message.channel.send("The Battle Tag you provided seems to be missing the # and numbers at the end. Please include that too.")

    else:
        await message.channel.send('This command was not formatted correctly. Please type !battle and then add your Battle Tag.')

    return False


async def add_event(db, message): 

    word_list = message.content.split('|')

    if len(word_list) != 6:
        await message.channel.send('Incorrect command format.')
    else:
        if get_event_by_id(db, word_list[1]):
            await message.channel.send('An event with this id already exists.')
        else:
            create_event(db, word_list[1], word_list[2], word_list[3], word_list[4], word_list[5])
            await message.channel.send('Event created successfully.')


async def delete_event(db, message, event_id):

    events = db['events']

    filter_query = {"event_id": event_id}

    result = events.delete_one(filter_query)

    if result.deleted_count == 1:
        await message.channel.send('Event with id '+event_id+' has been deleted')
    else:
        await message.channel.send('Event with id does not exist.')



def run_discord_bot(db):
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))

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

            user_message = str(message.content)
            is_command = len(user_message) > 0 and (user_message[0] == '!')
            if not is_command:
                return
            
            username = str(message.author)
            channel = str(message.channel)

            print(f'{username} said: "{user_message}" ({channel})')
            lower_message = user_message.lower()

            is_admin = (message.author.id == constants.SPICY_RAGU_ID)

            valid_channel = is_admin or isinstance(message.channel, discord.DMChannel) or message.channel.id == constants.BOT_CHANNEL or (message.channel.id == constants.CASINO_CHANNEL and lower_message.startswith('!wager'))
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
            elif lower_message == '!register':
                await dm_user_register_info(message.author, message)

            elif lower_message.startswith('!battle '):
                
                success = await register_battle_user(message, message.content, db)
                if success:
                    guild = client.get_guild(constants.GUILD_ID)
                    reg_role = guild.get_role(constants.REGISTERED_ROLE)
                    member = guild.get_member(message.author.id)
                    if member and reg_role:
                        await member.add_roles(reg_role)

            elif lower_message == "!events":


                event_list = get_all_events(db)
                found = False
                none_string = "It looks like there's no events right now... Check back soon!"
                # await message.channel.send(none_string)
                # return

                final_string = ""

                for event in event_list:


                    if not event_is_open(event):
                        continue

                    found = True
                    event_full = False
                    if (event['max_players'] == event['spots_filled']):
                        join_string = "FULL"
                        event_full = True
                    else:
                        join_string = "**"+str(event['max_players']-event['spots_filled'])+" Spots Remaining**"

                    num_players = get_event_team_size(event)
                    add_part = 'Players'
                    if num_players > 1:
                        add_part = 'Teams'

                    final_string = final_string+"**["+event['event_id']+"]** "+event['event_name']+" : "+ str(event['max_players']) +" Total "+add_part+" : "+join_string+' : '
                    
                    if num_players == 1:
                        final_string += '1 player per team'
                    else:
                        final_string += str(num_players)+' players per team'

                    if ('needs_pass' in event) and (event['needs_pass']):
                        final_string += ' : ***🎟️ PRIORITY PASS REQUIRED 🎟️***'

                    if not event_full:
                        if num_players == 1:
                            final_string += "\n*To join this event enter the command* **!join "+event['event_id']+"**\n\n"
                        else:
                            final_string += "\n*To join this event enter the command* **!teamjoin "+event['event_id']+" [team name here]**\n\n"
                    else:
                        final_string += "\n\n"

                if found:
                    await message.channel.send(final_string)
                else:
                    await message.channel.send(none_string)

            elif lower_message.startswith("!join "):

                await join_handler(db, message, client)

            elif lower_message.startswith("!suggestevent "):
                event_idea = message.content[len("!suggestevent "):].strip()

                event_channel = client.get_channel(constants.SUGGEST_CHANNEL)

                embed_msg = discord.Embed(
                    title = "Event Idea From "+message.author.name,
                    description=event_idea
                )
                embed_msg.set_footer(text="Suggest your own idea using the command !suggestevent [event idea here]", icon_url=message.author.display_avatar)

                event_idea_msg = await event_channel.send(embed=embed_msg)
                await event_idea_msg.add_reaction("👍")

                await message.delete()

            elif lower_message == "!tokens":

                await output_tokens(db, message)

            elif lower_message == "!passes":

                await output_passes(db, message)

            elif lower_message == "!eggs":

                await output_eggs(db, message)

            elif lower_message == "!sellpass":

                await sell_pass_for_tokens(db, message)

            elif lower_message == '!dailygift' or lower_message == '!gift':

                await give_daily_gift(db, message)

            elif lower_message.startswith('!funfact '):

                fun_fact = message.content[len("!funfact "):].strip()
                await add_fun_fact(message, fun_fact, db)

            elif lower_message == "!hello":

                answers = [
                    'Greetings.',
                    'Hello.',
                    'I greet you.',
                    'Peace be upon you.'
                ]

                random_response = random.choice(answers)
                await message.channel.send(random_response)

            elif lower_message == '!hatch':
                await hatch_handler(db, message)

            elif lower_message.startswith('!wager'):
                await wager_handler(db, message)

            elif lower_message == '!teams':
                await teams_handler(db, message)

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
                await help_teams_hanlder(message)


            elif lower_message.startswith('!buy'):
                await buy_handler(db, message)

            # ADMIN COMMANDS

            elif lower_message.startswith("!addevent") and is_admin:
                
                # !addevent|[event id]|[event name]|[max participants]|[0 for no pass, 1 for pass]|[team size]
                await add_event(db, message)

            elif lower_message.startswith("!delevent") and is_admin:

                # !delevent [event id]
                word_list = message.content.split()
                if len(word_list) == 2:
                    await delete_event(db, message, word_list[1])
                else:
                    await message.channel.send('Invalid use of command')

            elif lower_message.startswith("!approve ") and is_admin:

                # !approve [user_id] [event id]
                word_list = message.content.split()
                if len(word_list) == 3:
                    await approve_user(db, int(word_list[1]), word_list[2], client, message)
                else:
                    await message.channel.send("Invalid number of arguments.")


            elif lower_message.startswith("!deny") and is_admin:

                # !deny|[user id]|[event id]|[reason]
                word_list = message.content.split('|')
                if len(word_list) == 4:
                    await deny_user(db, int(word_list[1]), word_list[2], word_list[3], client, message)
                else:
                    await message.channel.send("Invalid number of arguments.")

            elif lower_message.startswith("!genbracket ") and is_admin:

                # !bracket [event id]
                word_list = message.content.split()
                if len(word_list) == 2:
                    await generate_bracket(db, message, word_list[1])
                else:
                    await message.channel.send("Invalid number of arguments.")

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
                    await give_tokens_command(db, int(word_list[1]), int(word_list[2]), message)
                else:
                    await message.channel.send("Invalid number of arguments.")

            elif lower_message.startswith('!givepasses ') and is_admin:

                # !givepasses [winner id] [passes]
                word_list = message.content.split()
                if len(word_list) == 3:
                    await give_passes_command(db, int(word_list[1]), int(word_list[2]), message)
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
                    
                    for member in client.get_all_members():

                        disc = member.discriminator
                        final_name = member.name
                        if disc != '0':
                            final_name = final_name+"#"+disc

                        if word_list[1] == final_name:
                            
                            user = user_exists(db, member.id)
                            if user:
                                final_string = 'User ID: '+str(member.id)+"\nBattle Tag: "+user['battle_tag']
                                final_string += '\nTokens: '+str(get_user_tokens(user))+'\n'+'Passes: '+str(get_user_passes(user))
                                await message.channel.send(final_string)

                            break
                else:
                    await message.channel.send("Invalid number of arguments.")

            elif lower_message == '!givereg' and is_admin:

                guild = client.get_guild(constants.GUILD_ID)
                reg_role = guild.get_role(constants.REGISTERED_ROLE)

                if reg_role:
                    for member in client.get_all_members():
                        member_id = member.id
                        existing_user = user_exists(db, member_id)
                        if existing_user:
                            await member.add_roles(reg_role)

                    await message.channel.send('Reg roles given')

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
            elif lower_message == '!testerror' and is_admin:

                guild = client.get_guild(constants.GUILD_ID)
                server_notifs = guild.get_role(constants.SERVER_NOTIFS_ROLE)
                tourney_notifs = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
                twitch_notifs = guild.get_role(constants.TWITCH_NOTIFS_ROLE)

                all_members = await guild.fetch_members()
                for member in all_members:
                    await member.add_roles(server_notifs, tourney_notifs, twitch_notifs)

                await message.channel.send('Done giving roles')
            else:
                await message.channel.send('Invalid command. Please see **!help** for a list of commands.')
        except Exception as e:
            guild = client.get_guild(constants.GUILD_ID)
            spicy_member = guild.get_member(constants.SPICY_RAGU_ID)
            await message.channel.send('Whoops... An error occured. Let me notify staff. '+spicy_member.mention)
            print(e)
            traceback.print_exc()


    client.run(constants.DISCORD_TOKEN)