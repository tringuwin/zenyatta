import time
import discord
from mongo import approve_user, create_event, create_or_update_battle_tag, deny_user, event_status, find_user_with_battle_tag, generate_bracket, get_all_events, get_event_by_id, output_tokens, try_join_event


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
                    await message.channel.send("Success! Your Battle Tag has been linked to Ragu Bot! (Please note: if you change your Battle Tag please use the !battle command again to update it!)")
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
        

        if lower_message == '!register':
            await dm_user_register_info(message.author, message)

        elif lower_message.startswith('!battle '):
            
            await register_battle_user(message, message.content, db)
            # if is_dm_channel(message.channel):
            #     await register_battle_user(message, message.content, db)
            # else:
            #     await message.channel.send('For your privacy, please only use the !battle command in a DM with me.')
            #     await message.delete()

        elif lower_message == "!events":

            event_list = get_all_events(db)
            found = False
            none_string = "It looks like there's no events right now... Check back soon!"

            final_string = ""

            for event in event_list:
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

        elif lower_message.startswith("!status"):

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

        elif lower_message.startswith("!bracket ") and is_admin:

            # !bracket [event id]
            word_list = message.content.split()
            if len(word_list) == 2:
                await generate_bracket(db, message, word_list[1])
            else:
                await message.channel.send("Invalid number of arguments.")


        elif lower_message.startswith("!test") and is_admin:

            sent_message = await message.channel.send("This is a test message")
            await sent_message.add_reaction("✅")



            
           

    client.run(TOKEN)