import random
import time
import discord
from bracket import gen_tourney, notify_next_users, send_next_info, wipe_tourney, won_match
from mongo import add_fun_fact, approve_user, create_event, create_or_update_battle_tag, deny_user, event_status, find_user_with_battle_tag, generate_bracket, get_all_events, get_event_by_id, give_daily_gift, output_passes, output_tokens, switch_matches, try_join_event
from rewards import give_passes_command, give_tokens, give_tokens_command, sell_pass_for_tokens
from user import user_exists


async def dm_user_register_info(author, message):

    await message.channel.send(author.mention+' Hi! Thanks for registering. Please use the !battle command in this channel to input your Battle Tag. (Hint: you can find and copy your Battle Tag in the Battle Net app.) **Command example: !battle SpicyRagu#1708**')
    try:
        await author.send(author.mention+' Hi! Thanks for registering. Please use the !battle command in this channel to input your Battle Tag. (Hint: you can find and copy your Battle Tag in the Battle Net app.) **Command example: !battle SpicyRagu#1708**')
    except:
        print('could not dm user')

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
                
                await message.channel.send("Please wait while I check the database...")
                lower_tag = battle_tag.lower()

                if find_user_with_battle_tag(db, lower_tag):
                    await message.channel.send("That Battle Tag has already been connected with a discord account. (Maybe you've already linked it?)")
                else:
                    create_or_update_battle_tag(db, battle_tag, lower_tag, message.author.id)
                    await message.channel.send("Success! Your Battle Tag has been linked to the SpicyRagu server! (Please note: if you change your Battle Tag please use the !battle command again to update it!)")
                    await message.channel.send("Now that your account is linked would you like to sign up for an event? Just say **!events** to see events with openings!")
            else:
                await message.channel.send("The Battle Tag you provided seems to be missing the # and numbers at the end. Please include that too.")

    else:
        await message.channel.send('This command was not formatted correctly. Please type !battle and then add your Battle Tag.')


async def add_event(db, message): 

    word_list = message.content.split('|')

    if len(word_list) != 4:
        await message.channel.send('Incorrect command format.')
    else:
        if get_event_by_id(db, word_list[1]):
            await message.channel.send('An event with this id already exists.')
        else:
            create_event(db, word_list[1], word_list[2], word_list[3])
            await message.channel.send('Event created successfully.')


async def delete_event(db, message, event_id):

    events = db['events']

    filter_query = {"event_id": event_id}

    result = events.delete_one(filter_query)

    if result.deleted_count == 1:
        await message.channel.send('Event with id '+event_id+' has been deleted')
    else:
        await message.channel.send('Event with id does not exist.')



def run_discord_bot(mongo_client, db):
    TOKEN = 'MTEzMDIyNTQzNjAwNjMwNTk0Ng.GNqc6p.qR6t7fym71pGd3CLl9QKwQ8usCFoXhhG8W7PDE'
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    MY_ID = 1112204092723441724
    GUILD_ID = 1130553449491210442
    MEMBER_ROLE_ID = 1131309952200347741

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))

    @client.event
    async def on_member_join(member):
        print("New user joined")
        guild = client.get_guild(GUILD_ID)
        role = guild.get_role(MEMBER_ROLE_ID)

        if role is not None:
            await member.add_roles(role)
            print("Gave role to new user")


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return


        user_message = str(message.content)
        is_command = len(user_message) > 0 and (user_message[0] == '!')
        if not is_command:
            return
        
        username = str(message.author)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')
        lower_message = user_message.lower()

        is_admin = (message.author.id == MY_ID)

        valid_channel = is_admin or isinstance(message.channel, discord.DMChannel) or message.channel.id == 1130553489106411591

        if not valid_channel:
            
            await message.delete()
            warning = await message.channel.send(message.author.mention+" Please only use commands in #bot-commands or in a Direct Message with me.")

            time.sleep(10)
            await warning.delete()
            return
        
        if lower_message == '!help':

            help_embed = discord.Embed(title='List of commands:')
            help_embed.add_field(name='!register', value='Show instructions to register', inline=False)
            help_embed.add_field(name='!battle BattleTagHere#1234', value='Register your battle tag with the SpicyRagu server', inline=False)
            help_embed.add_field(name='!events', value='Show a list of current server events', inline=False)
            help_embed.add_field(name='!join [event id]', value='Join an upcoming event', inline=False)
            help_embed.add_field(name='!status [event id]', value='See the status of an event join request', inline=False)
            help_embed.add_field(name='!suggestevent [idea here]', value='Suggest an idea for a future event', inline=False)
            help_embed.add_field(name='!tokens', value='See your current number of tokens', inline=False)
            help_embed.add_field(name='!passes', value='See your current passes', inline=False)
            help_embed.add_field(name='!sellpass', value='Sell 1 Priority Pass for 10 tokens', inline=False)
            help_embed.add_field(name='!dailygift', value='Earn a daily gift once per day', inline=False)
            help_embed.add_field(name='!funfact [fun fact here]', value='Add a fun fact about yourself that might be mentioned during livestreamed events', inline=False)
            help_embed.add_field(name='!hello', value='Say hi to the Zenyatta bot', inline=False)

            await message.channel.send(embed=help_embed)

        elif lower_message == '!register':
            await dm_user_register_info(message.author, message)

        elif lower_message.startswith('!battle '):
            
            await register_battle_user(message, message.content, db)

        elif lower_message == "!events":


            event_list = get_all_events(db)
            found = False
            none_string = "It looks like there's no events right now... Check back soon!"

            final_string = ""

            for event in event_list:

                if 'test' in event['event_id']:
                    continue

                found = True
                event_full = False
                if (event['max_players'] == event['spots_filled']):
                    join_string = "FULL"
                    event_full = True
                else:
                    join_string = "**"+str(event['max_players']-event['spots_filled'])+" Spots Remaining**"

                final_string = final_string+"**["+event['event_id']+"]** "+event['event_name']+" : "+ str(event['max_players']) +" Total Players : "+join_string

                if not event_full:
                    final_string += " : To join event enter the command **!join "+event['event_id']+"**\n"
                else:
                    final_string += "\n"

            if found:
                await message.channel.send(final_string)
            else:
                await message.channel.send(none_string)

        elif lower_message.startswith("!join "):

            word_list = message.content.split()
            if len(word_list) == 2:
                await try_join_event(db, message, word_list[1], client)
            else:
                message.channel.send("Command was not in the correct format. Please enter '!join' followed by the id of the event you want to join.")

        elif lower_message.startswith("!status "):

            word_list = message.content.split()
            if len(word_list) == 2:
                await event_status(db, message, word_list[1])
            else:
                await message.channel.send("Command was not in the correct format. Please enter '!status' followed by the ID of the event.")

        elif lower_message.startswith("!suggestevent "):
            event_idea = message.content[len("!suggestevent "):].strip()

            event_channel = client.get_channel(1133850857037901956)

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

        elif lower_message == "!sellpass":

            await sell_pass_for_tokens(db, message)

        elif lower_message == '!dailygift':

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



        # ADMIN COMMANDS

        elif lower_message.startswith("!addevent") and is_admin:
            
            # !addevent|[event id]|[event name]|[max participants]
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


        elif lower_message.startswith("!test") and is_admin:

            sent_message = await message.channel.send("This is a test message")
            await sent_message.add_reaction("✅")

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

            guild = client.get_guild(GUILD_ID)
            tourney_role = guild.get_role(1131326944311525577)
            event_channel = client.get_channel(1131365793855176854)

            await send_next_info(db, message, guild, event_channel)

            await event_channel.send('**TOURNAMENT HAS STARTED** '+tourney_role.mention)
            await notify_next_users(db, guild, message, event_channel)

        elif lower_message == '!pausetourney' and is_admin:

            guild = client.get_guild(GUILD_ID)
            tourney_role = guild.get_role(1131326944311525577)
            event_channel = client.get_channel(1131365793855176854)

            await event_channel.send('**TOURNAMENT HAS PASUED** '+tourney_role.mention)

        elif lower_message.startswith('!win ') and is_admin:
            
            event_channel = client.get_channel(1131365793855176854)

            # !gentourney [winner 1 or 2]
            word_list = message.content.split()
            if len(word_list) == 2:
                guild = client.get_guild(GUILD_ID)
                await won_match(int(word_list[1]), message, db, guild, event_channel)
            else:
                await message.channel.send("Invalid number of arguments.")

        elif lower_message.startswith('!giverewards') and is_admin:
            
            reward_per_round = [10, 10, 100, 200, 500, 0, 0]

            bracket = db['brackets'].find_one({'event_id': '1'})

            final_dict = {}

            round_index = 0
            for round in bracket['bracket']:
                for match in round:
                    
                    for player in match:
                        if not (player['is_bye'] or player['is_tbd']):
                            final_dict[str(player['user'])] = round_index

                round_index += 1

            for player_id_string, highest_round in final_dict.items():

                user = db['users'].find_one({'discord_id': int(player_id_string)})
                if user:

                    reward = reward_per_round[highest_round]
                    await give_tokens(db, user, reward)

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


        elif lower_message == '!listids' and is_admin:

            for member in client.get_all_members():

                print(member.display_name+" : "+str(member.id) + " : "+member.name+' : '+member.discriminator)

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
                            await message.channel.send('User ID: '+str(member.id)+"\nBattle Tag: "+user['battle_tag'])

                        break

            else:
                await message.channel.send("Invalid number of arguments.")

        else:
            await message.channel.send('Invalid command. Please see **!help** for a list of commands.')

    client.run(TOKEN)