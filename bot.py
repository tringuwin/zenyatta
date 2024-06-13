import asyncio
import random
import time
import discord
import aiohttp
from datetime import timedelta
from admin_handlers.delete_by_tag import delete_by_tag_handler
from admin_handlers.force_add_team import force_add_team_handler
from admin_handlers.force_battle_handler import force_battle_handler
from admin_handlers.force_delete_team import force_delete_team_handler
from admin_handlers.force_league_remove import force_league_remove_handler
from admin_handlers.force_make_team import force_make_team_handler
from admin_handlers.force_remove_player import force_remove_player_handler
from admin_handlers.force_remove_team import force_remove_team_handler
from admin_handlers.force_twitch import force_twitch_handler
from admin_handlers.full_events import full_events_handler
from admin_handlers.gen_bracket import gen_bracket_handler
from admin_handlers.give_gems import give_gems_handler
from admin_handlers.give_lootbox import give_lootbox_handler
from admin_handlers.give_random_gem import give_random_gem_handler
from admin_handlers.give_sac import give_sac_handler
from admin_handlers.give_sub_boxes import give_sub_boxes_handler
from admin_handlers.give_twitch_lootbox import give_twitch_lootbox_handler
from admin_handlers.give_xp import give_xp_handler
from admin_handlers.prune_sac import prune_sac_handler
from admin_handlers.set_item_price import set_item_price_handler
from admin_handlers.set_level import set_level_handler
from admin_handlers.sub_rewards import gift_rewards_handler, sub_rewards_handler
from admin_handlers.total_league import total_league_handler
from auction import check_auction
from cards import buy_card_handler, card_owners_handler, cards_handler, give_card_handler, init_card_handler, init_custom_handler, list_card_handler, open_pack_handler, sell_card_handler, total_packs_handler, unlist_card_handler, view_card_handler, wipe_card_database_handler, wipe_player_cards_handler
from cards_data import init_card_data_db, update_card_data_db
from command_handlers.accept_gem_trade import accept_gem_trade_handler
from command_handlers.auction.bid import bid_handler
from command_handlers.auction.end_auction import end_auction_handler
from command_handlers.auction.start_auction import start_auction_handler
from command_handlers.auction_timer import auction_timer_handler
from command_handlers.bandforband import band_for_band_handler
from command_handlers.bets.bet import bet_handler
from command_handlers.bets.finish_bet import finish_bet_handler
from command_handlers.bets.my_bets import my_bets_handler
from command_handlers.bets.new_bet import new_bet_handler, update_bets
from command_handlers.bets.void_bet import void_bet_handler
from command_handlers.blackjack import blackjack_handler, check_for_black_jack
from command_handlers.bracket import bracket_handler
from command_handlers.buy_ticket import buy_ticket_handler
from command_handlers.deny_gem_trade import deny_gem_trade_handler
from command_handlers.donate import donate_handler
from command_handlers.donate_pass import donate_pass_handler
from command_handlers.gems import gems_handler
from command_handlers.getdetails import get_details_handler
from command_handlers.gg_ez import gg_ez_handler
from command_handlers.gift import gift_handler
from command_handlers.hello import hello_handler
from command_handlers.help.help_bonus import help_bonus_handler
from command_handlers.help.help_cards import help_cards_handler
from command_handlers.help.help_casino import help_casino_handler
from command_handlers.help.help_gems import help_gems_handler
from command_handlers.help.help_league import help_league_handler
from command_handlers.help.help_lft import help_lft_handler
from command_handlers.help.help_poke import help_poke_handler
from command_handlers.helper_salary import helper_salary_handler
from command_handlers.invited_by import invited_by_handler
from command_handlers.leaderboard import leaderboard_handler
from command_handlers.league.add_loss import add_loss_handler
from command_handlers.league.add_win import add_win_handler
from command_handlers.league.change_role import change_role_handler
from command_handlers.league.change_team_owner import change_team_owner_handler
from command_handlers.league.change_tpp import change_tpp_handler
from command_handlers.league.e_sub import e_sub_handler
from command_handlers.league.fan_of import fan_of_handler
from command_handlers.league.force_delete_league_team import force_delete_league_team_handler
from command_handlers.league.force_league_add import force_league_add_handler
from command_handlers.league.give_team_tokens import give_team_tokens_handler
from command_handlers.league.league_accept import league_accept_handler
from command_handlers.league.league_cancel_invite import league_cancel_invite_handler
from command_handlers.league.league_deny import league_deny_handler
from command_handlers.league.league_invite import league_invite_handler
from command_handlers.league.league_invites import league_invites_handler
from command_handlers.league.league_kick import league_kick_handler
from command_handlers.league.league_leave import league_leave_handler
from command_handlers.league.league_order import league_order_handler
from command_handlers.league.league_xp import league_xp_handler, total_league_xp_handler
from command_handlers.league.lft.set_lft_color import set_lft_color_handler
from command_handlers.league.lft.set_lft_hero import set_lft_hero_handler
from command_handlers.league.lft.set_rank import set_rank_handler
from command_handlers.league.lft.toggle_lft import toggle_lft_handler
from command_handlers.league.lft.update_lft import update_lft_handler
from command_handlers.league.make_league_team import make_league_team_handler
from command_handlers.league.make_team_admin import make_team_admin_handler
from command_handlers.league.ping_team import ping_team_handler
from command_handlers.league.prune_team import prune_team_handler
from command_handlers.league.remove_team_admin import remove_team_admin_handler
from command_handlers.league.reset_map import reset_map_handler
from command_handlers.league.reset_maps import reset_maps_handler
from command_handlers.league.reset_scores import reset_scores_handler
from command_handlers.league.reset_wins import reset_wins_handler
from command_handlers.league.rival_of import rival_of_handler
from command_handlers.league.schedule import schedule_handler
from command_handlers.league.set_apps_link import set_apps_link_handler
from command_handlers.league.set_league_team import set_league_team_handler
from command_handlers.league.set_map import set_map_handler
from command_handlers.league.set_score import set_score_handler
from command_handlers.league.set_win import set_win_handler
from command_handlers.league.standings import standings_handler
from command_handlers.league.toggle_apps import toggle_apps_handler
from command_handlers.league.update_team import update_team_handler
from command_handlers.lootboxes import lootboxes_handler
from command_handlers.mine import mine_handler
from command_handlers.open import open_handler
from command_handlers.poke_leaderboard import poke_leaderboard_handler
from command_handlers.twitch import twitch_handler
from command_handlers.xp_battle.battle_no_show import battle_no_show_handler
from command_handlers.xp_battle.battle_teams import battle_teams_handler
from command_handlers.xp_battle.battle_win import battle_win_handler
from command_handlers.xp_battle.end_battle import end_battle_handler
from command_handlers.xp_battle.end_reg import end_reg_handler
from command_handlers.xp_battle.start_battle import start_battle_handler
from poke_data import update_poke_data_db
from pokemon import add_poke_handler, all_pokes_handler, get_pokedex, get_sort_index, my_pokes_handler, open_poke_handler, sell_poke_handler, view_poke_handler
from command_handlers.profile import profile_handler
from command_handlers.raffle import raffle_handler
from command_handlers.random_map import random_map_handler
from command_handlers.rps import rps_handler
from command_handlers.sell_gems import sell_gems_handler
from command_handlers.solo_join import solo_join_handler
from command_handlers.sub_timer import sub_timer_handler
from command_handlers.suggest import suggest_handler
from command_handlers.suggest_event import suggest_event_handler
from command_handlers.teams.del_team_from_event import del_team_from_event_handler
from command_handlers.teams.get_teams import get_teams_handler
from command_handlers.teams.switch_event_teams import switch_event_teams
from command_handlers.token_leaderboard import token_leaderboard_handler
from command_handlers.trade_gem import trade_gem_handler
from command_handlers.trade_gem_set import trade_gem_set_handler
from command_handlers.which_hero_handler import which_hero_handler
from command_handlers.which_team import which_team_handler
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
from command_handlers.help.help import help_handler
from command_handlers.teams.team_details import team_details_hanlder
from command_handlers.teams.team_join import team_join_handler
from command_handlers.teams.teams import teams_handler
from command_handlers.wager import twager_handler, wager_handler
from bracket import both_no_show, gen_tourney, no_show, notify_next_users, send_next_info, wipe_tourney, won_match
from discord_actions import get_guild, get_role_by_id, is_dm_channel, member_has_role
from helper_handlers.twitch_pack import twitch_pack_handler
from helper_handlers.twitch_pass import twitch_pass_handler
from helper_handlers.twitch_tokens import twitch_tokens_handler
from helpers import can_be_int, get_constant_value, set_constant_value
from api import get_member, give_role, remove_role, send_msg
from mongo import output_eggs, output_packs, output_passes, output_pickaxes, output_tokens, switch_matches
from payroll import check_payroll
from random_event import react_to_event, try_random_event
from rewards import change_xp, give_eggs_command, give_packs_command, give_passes_command, change_tokens, give_pickaxes_command, give_pp_handler, give_tokens_command, sell_pass_for_tokens, sell_pickaxe_for_tokens
from server_level import server_points_handler
from streamlabs import check_streamlabs_raffles
from teams import get_team_by_name
from time_helpers import check_weekly, long_enough_for_gift
from twitch_token import check_token_issue
from user import get_knows_gift, get_last_gift, get_lvl_info, get_role_id_by_level, notify_user_of_gift, user_exists
from xp_battles import add_to_battle, how_many_handler, remove_from_battle


def is_valid_channel(message, lower_message, is_helper, is_push_bot):

    if is_helper or is_push_bot:
        return True, None
    
    if lower_message == '!hello' or lower_message == '!gg ez' or lower_message.startswith('!whichteam') or lower_message.startswith('!whichhero') or lower_message=='!pingteam' or lower_message.startswith('!profile') or lower_message.startswith('!bandforband') or lower_message == '!fortnite' or lower_message == '!zorp' or lower_message == '!howdy' or lower_message == '!sigma':
        return True, None

    if message.channel.id == constants.BOT_CHANNEL:

        if lower_message.startswith('!wager'):
            return False, 'Please only use the wager command in the Roulette Channel.'
        elif lower_message.startswith('!twager'):
            return False, 'Please only use the twager command in the Roulette Channel.'
        elif lower_message.startswith('!blackjack'):
            return False, 'Please only use the blackjack command in the Blackjack Channel.'
        elif lower_message.startswith('!mine'):
            return False, 'Please only use the mine command in the Mineshaft Channel.'
        else:
            return True, None
        
    elif message.channel.id == constants.CASINO_CHANNEL:

        if lower_message.startswith('!wager') or lower_message.startswith('!twager') or lower_message.startswith('!tokens') or lower_message.startswith('!help'):
            return True, None
        else:
            return False, 'Only these commands are allowed in the Roulette Channel: !wager, !twager, !tokens, !helpcasino, !help'
        
    elif message.channel.id == constants.BLACKJACK_CHANNEL:

        if lower_message.startswith('!blackjack') or lower_message.startswith('!tokens') or lower_message.startswith('!help'):
            return True, None
        else:
            return False, 'Only these commands are allowed in the Blackjack Channel: !blackjack, !tokens, !helpcasino'
        
    elif message.channel.id == constants.MINE_CHANNEL:

        if lower_message.startswith('!mine') or lower_message.startswith('!tokens') or lower_message.startswith('!pickaxes') or lower_message.startswith('!gems') or lower_message.startswith('!sellgems') or lower_message.startswith('!tradegemset') or lower_message.startswith('!help'):
            return True, None
        else:
            return False, 'Only these commands are allowed in the Mineshaft Channel: !mine, !tokens, !pickaxes, !gems, !helpcasino'
        
    elif message.channel.id == constants.RPS_CHANNEL:

        if lower_message.startswith('!rps') or lower_message.startswith('!tokens') or lower_message.startswith('!help'):
            return True, None
        else:
            return False, 'Only these commands are allowed in the RPS Channel: !rps, !tokens, !helpcasino'
        
    elif message.channel.id == constants.GEM_TRADING_CHANNEL:

        if lower_message.startswith('!help') or lower_message.find('gem') != -1:
            return True, None
        else:
            return False, 'Only gem related commands are allowed in the Gem Trading channel.'
        
    elif (message.channel.id == constants.CARD_TRADING_CHANNEL) or (message.channel.id == constants.PACK_OPEN_CHANNEL):

        if lower_message.find('card') != -1 or lower_message.find('pack') != -1 or lower_message.find('token') != -1 or lower_message.find('donate') != -1:
            return True, None
        
        
    return False, 'Please only use commands in a valid channel'


def bad_work_checker(message_text):

    lower_message = message_text.lower()
    for bad_word in constants.VERY_BAD_WORD_LIST:
        if lower_message.find(bad_word) != -1:
            return True
        
    return False


async def handle_message(message, db, client):

    random_event_chance = random.randint(1, 100)
    if random_event_chance == 100:
        await try_random_event(db, client)

    channel = str(message.channel)
    if is_dm_channel(message.channel):
        await send_msg(message.channel, 'Sorry, I do not respond to messages in Direct Messages. Please only use commands in the #bot-commands channel of the Spicy OW Discord server.', 'DM Alert')
        return
    
    has_bad_word = bad_work_checker(message.content)
    if has_bad_word:
        guild = await get_guild(client)
        helpers_channel = guild.get_channel(constants.HELPERS_CHANNEL)
        await message.author.timeout(timedelta(days=7))
        await helpers_channel.send(message.author.name+' was timed out for saying **'+message.content+'**\n\nPlease verify if this timeout was correct and take action on it.')
        await message.delete()
        return

    user_message = str(message.content)
    is_admin = (message.author.id == constants.SPICY_RAGU_ID)
    is_helper = (not message.author.bot) and member_has_role(message.author, constants.HELPER_ROLE_ID)
    is_league_helper = (not message.author.bot) and member_has_role(message.author, constants.LEAGUE_REWARDS_ROLE_ID)
    is_cp_helper = (not message.author.bot) and member_has_role(message.author, constants.CHANNEL_POINTS_ROLE_ID)
    is_tp_helper = (not message.author.bot) and member_has_role(message.author, constants.TWITCH_PACKS_ROLE_ID)
    has_image_perms = message.author.bot or member_has_role(message.author, constants.IMAGE_PERMS_ROLE)
    is_push_bot = (message.author.id == constants.PUSH_BOT_ID)

    lower_message = user_message.lower()
    if (not has_image_perms) and (lower_message.find('discord.gg') != -1 or lower_message.find('http') != -1):
        await message.delete()

        db_constants = db['constants']
        warned_users_obj = db_constants.find_one({'name': 'warnings'})
        warned_users = warned_users_obj['value']

        if message.author.id in warned_users:
            # ban user and delete messages, notify helpers
            banned_name = message.author.name
            await message.author.ban(delete_message_days=7)
            guild = await get_guild(client)
            helpers_channel = guild.get_channel(constants.HELPERS_CHANNEL)
            await helpers_channel.send('BAN REPORT: User "'+banned_name+'" was banned for sending links twice without Image Permission. Please review the logs and check if this ban was correct. Revoke the ban if the user was not enaging in harmful activity.')
            return
        else:
            # add to warnings array
            await message.channel.send(message.author.mention+' '+' users without Image Perms are not allowed to post links. Please ask a Helper for Image Perms. **Your account has been flagged as potentially dangerous, and if you post a link without image permission again, you will be automatically banned by the bot.**')
            warned_users.append(message.author.id)
            db_constants.update_one({"name": 'warnings'}, {"$set": {"value": warned_users}})
            guild = await get_guild(client)
            helpers_channel = guild.get_channel(constants.HELPERS_CHANNEL)
            await helpers_channel.send('WARN REPORT: User "'+message.author.name+'" was *warned* for sending a link without Image Permission. Please review the logs and check if what they sent was allowed. If it was allowed, please give them image perms immediately to prevent them from being accidently banned.')
            return

    # peanut butter check
    # if lower_message.find('peanut butter') != -1:
    #     await message.channel.send('<:Winton:1243994564268920933> Did someone say peanut butter? <:Winton:1243994564268920933>')

    is_command = len(user_message) > 0 and (user_message[0] == '!')
    if (not is_command) and (not is_push_bot):
        return

    valid_channel, response = is_valid_channel(message, lower_message, is_helper, is_push_bot)

    if not valid_channel:
        
        await message.delete()
        warning = await message.channel.send(message.author.mention+" "+response)

        time.sleep(10)
        await warning.delete()
        return


    if lower_message == '!help':
        await help_handler(message)

    elif lower_message == '!helpleague':
        await help_league_handler(message)

    elif lower_message == '!helpgems':
        await help_gems_handler(message)

    elif lower_message == '!helpcasino':
        await help_casino_handler(message)

    elif lower_message == '!helpcards':
        await help_cards_handler(message)

    elif lower_message == '!helpbonus':
        await help_bonus_handler(message)

    elif lower_message == '!helplft':
        await help_lft_handler(message)

    elif lower_message == '!helppoke':
        await help_poke_handler(message)

    elif lower_message == '!version':
        await send_msg(message.channel, constants.VERSION, '!version')
    
    elif lower_message.startswith('!battle '):
        await battle_handler(db, message, client)

    elif lower_message.startswith('!twitch '):
        await twitch_handler(db, message)

    elif lower_message.startswith('!forcetwitch ') and is_admin:
        await force_twitch_handler(db, message, client)

    elif lower_message.startswith('!subrewards') and is_admin:
        await sub_rewards_handler(client, db, message)

    elif lower_message.startswith('!giftrewards') and is_admin:
        await gift_rewards_handler(client, db, message)

    elif lower_message == "!events":
        await events_handler(db, message)

    elif lower_message.startswith("!join "):
        await join_handler(db, message, client)
    
    elif lower_message.startswith("!suggestevent "):
        await suggest_event_handler(message, client)

    elif lower_message.startswith("!suggest "):
        await suggest_handler(message, client)

    elif lower_message == "!tokens":
        await output_tokens(db, message)

    elif lower_message == "!passes":
        await output_passes(db, message)

    elif lower_message == '!packs':
        await output_packs(db, message)

    elif lower_message == '!cards':
        await cards_handler(db, message)

    elif lower_message == '!gems':
        guild = await get_guild(client)
        await gems_handler(db, message, guild)

    elif lower_message == '!lootboxes':
        await lootboxes_handler(db, message)

    elif lower_message == "!eggs":
        await output_eggs(db, message)

    elif lower_message == '!pickaxes':
        await output_pickaxes(db, message)

    elif lower_message == "!sellpass":
        await sell_pass_for_tokens(db, message)

    elif lower_message == '!sellpickaxe':
        await sell_pickaxe_for_tokens(db, message)

    elif lower_message == '!dailygift' or lower_message == '!gift':
        await gift_handler(db, message, client, is_admin)

    elif lower_message == "!hello":
        await hello_handler(message)

    elif lower_message == '!spicyowrank':

        response = 'Spicy OW is the **61st** highest ranked Overwatch Discord Server'
        response += "\nNext Server to Beat: **Kaizen eSports**"

        await message.channel.send(response)

    elif lower_message == '!gg ez':
        await gg_ez_handler(message)

    elif lower_message.startswith('!whichhero'):
        await which_hero_handler(message)

    elif lower_message == '!store':
        await message.channel.send('Check out the official SOL Merch Store here! https://exclaim.gg/store/spicyow')

    elif lower_message.startswith('!whichteam'):
        await which_team_handler(message)

    elif lower_message == '!hatch':
        await hatch_handler(db, message)

    elif lower_message.startswith('!wager'):
        await wager_handler(db, message)

    elif lower_message.startswith('!twager'):
        await twager_handler(db, message)

    elif lower_message == '!mine':
        await mine_handler(db, message, client)

    elif lower_message.startswith('!blackjack'):
        await blackjack_handler(db, message, client)

    elif lower_message.startswith('!rps'):
        await rps_handler(db, message)

    elif lower_message.startswith('!buy '):
        await buy_handler(db, message, client)

    elif lower_message.startswith('!donate '):
        await donate_handler(db, message)

    elif lower_message.startswith('!donatepass'):
        await donate_pass_handler(db, message)

    elif lower_message.startswith('!solojoin'):
        await message.channel.send('This command is not currently enabled! Check back later')
        #await solo_join_handler(db, message, client)

    elif lower_message.startswith('!invitedby'):
        await invited_by_handler(db, message)

    elif lower_message == '!verifyranks':
        final_string = 'Please make a ticket here (the top one) to show staff a screenshot of your ranks: https://discord.com/channels/1130553449491210442/1202441473027477504/1202442124390440970'
        final_string += '\n\nSend a screenshot of your career profile that includes both your ranks and battle tag.'
        await message.channel.send(final_string)
    
    # pi-pi chan

    elif lower_message.startswith('!setrank') and is_helper:
        await set_rank_handler(db, message)

    elif lower_message == '!leaderboard':
        await leaderboard_handler(db, message)

    elif lower_message == '!tokenleaderboard':
        await token_leaderboard_handler(db, message)

    elif lower_message == '!pokeleaderboard':
        await poke_leaderboard_handler(db, message)

    elif lower_message == '!bracket':
        await bracket_handler(message)

    elif lower_message.startswith('!profile'):
        await profile_handler(db, message, client)

    elif lower_message == '!randommap':
        await random_map_handler(message)

    elif lower_message == '!standings':
        #await message.channel.send('This command is disabled until Season 3 starts on June 1st 2024.')
        await standings_handler(db, message, client)

    elif lower_message == '!schedule':
        #await message.channel.send('This command is disabled until Season 3 starts on June 1st 2024.')
        await schedule_handler(db, message, client)

    # elif lower_message == '!buyticket':
    #     #await message.channel.send('There is no raffle at the moment.')
    #     await buy_ticket_handler(db, message, 1)
    
    # elif lower_message.startswith('!buyticket '):
    #     #await message.channel.send('There is no raffle at the moment.')
    #     params = lower_message.split()
    #     if len(params) == 2:
    #         raw_amount = params[1]
    #         if can_be_int(raw_amount):
    #             await buy_ticket_handler(db, message, int(raw_amount))
    #         else:
    #             await send_msg(message.channel, message.author.mention+' Please enter a number of tickets to buy.', '!buyticket')
    #     else:
    #         await send_msg(message.channel, message.author.mention+' Invalid number of parameters.', '!buyticket')


    # elif lower_message == '!raffle':
    #     await raffle_handler(db, message)

    elif lower_message.startswith('!bid '):
        await bid_handler(db, message, client)

    elif lower_message == '!subtimer':
        await message.channel.send('Twitch Lootboxes are now given instantly when you subscribe or re-subscribe!')
        # await sub_timer_handler(db, message)

    elif lower_message == '!auctiontimer':
        await auction_timer_handler(db, message)

    # TEAM COMMANDS

    elif lower_message == '!teams':
        await teams_handler(db, message)

    elif lower_message.startswith('!getteams ') and is_admin:
        await get_teams_handler(db, message)

    elif lower_message.startswith('!teaminfo'):
        await team_details_hanlder(db, message)

    elif lower_message.startswith('!maketeam '):
        await make_team_handler(db, message)

    elif lower_message.startswith('!invite '):
        await invite_handler(db, message, is_admin)

    elif lower_message == '!myinvites':
        await my_invites_handler(db, message)

    elif lower_message.startswith('!acceptinvite '):
        await accept_invite_handler(db, message, client)

    elif lower_message.startswith('!denyinvite'):
        await deny_invite_handler(db, message)

    elif lower_message.startswith('!leaveteam'):
        await leave_team_handler(db, message, client)

    elif lower_message.startswith('!deleteteam'):
        await delete_team_handler(db, message, client)

    elif lower_message.startswith('!teamjoin'):
        await team_join_handler(client, db, message)

    elif lower_message.startswith('!kickplayer'):
        await kick_player_handler(db, message, client)

    elif lower_message.startswith('!helpteams'):
        await help_teams_handler(message)

    elif lower_message.startswith('!delteamfromevent') and is_admin:
        await del_team_from_event_handler(db, message)

    elif lower_message.startswith('!switcheventteams ') and is_admin:
        # !switcheventteams [event id] [match id] [spot id (1 or 2)] [new team name]
        await switch_event_teams(db, message)

    # LEAGUE COMMANDS

    elif lower_message.startswith('!makeleagueteam') and is_admin:
        # !makeleagueteam [team role id] @Owner [Team Name]
        await make_league_team_handler(db, message, client)

    elif lower_message.startswith('!changeteamowner') and is_admin:
        # !changeteamowner @player team name
        await change_team_owner_handler(db, message, client)

    elif lower_message.startswith('!changetpp'):
        # !changetpp @Player [new tpp]
        await change_tpp_handler(db, message, client)

    elif lower_message.startswith('!changerole'):
        # !changerole @Player [new role]
        await change_role_handler(db, message, client)

    elif lower_message.startswith('!leaguekick '):
        # !leaguekick @Player
        await league_kick_handler(db, message, client)

    elif lower_message.startswith('!maketeamadmin'):
        # !maketeamadmin @Player
        await make_team_admin_handler(db, message, client)

    elif lower_message.startswith('!removeteamadmin'):
        # !removeteamadmin @Player
        await remove_team_admin_handler(db, message, client)

    elif lower_message.startswith('!leagueinvite '):
        # !leagueinvite @player
        await league_invite_handler(db, message)

    elif lower_message.startswith('!leaguecancelinvite '):
        # !leaguecancelinvite @player
        await league_cancel_invite_handler(db, message)

    elif lower_message == '!leagueinvites':
        await league_invites_handler(db, message)

    elif lower_message.startswith('!leagueaccept '):
        await league_accept_handler(db, message, client)

    elif lower_message.startswith('!leaguedeny' ):
        await league_deny_handler(db, message)

    elif lower_message == '!leagueleave':
        await league_leave_handler(db, message, client)

    elif lower_message == '!leaguexp':
        await league_xp_handler(db, message, client)

    elif lower_message == '!leaguexptotal':
        await total_league_xp_handler(db, message, client)

    elif lower_message == '!pingteam':
        await ping_team_handler(db, message, client)

    elif lower_message == '!pruneteam':
        await prune_team_handler(db, message, client)

    elif lower_message.startswith('!leagueorder'):
        await league_order_handler(db, message, client)

    elif lower_message.startswith('!setappslink'):
        await set_apps_link_handler(db, message)

    elif lower_message == '!toggleapps':
        await toggle_apps_handler(db, message)

    elif lower_message == '!lft':
        await message.channel.send('See the list of players looking to join a team here: https://spicyragu.netlify.app/sol/lft')

    elif lower_message == '!togglelft':
        await toggle_lft_handler(db, message)

    elif lower_message.startswith('!setlftcolor'): 
        await set_lft_color_handler(db, message)

    elif lower_message.startswith('!setlfthero'):
        # !setlfthero index hero
        await set_lft_hero_handler(db, message)

    elif lower_message.startswith('!updatelft'):
        await update_lft_handler(db, message)

    elif lower_message.startswith('!setleagueteam ') and is_admin:
        # !setleagueteam [user_id] [team name]
        await set_league_team_handler(db, message)

    elif lower_message.startswith('!wipeleagueteams') and is_admin:
        
        league_teams = db['leagueteams']
        league_teams.delete_many({})

        await send_msg(message.channel, 'All league teams deleted', '!wipeleagueteams')

    elif lower_message.startswith('!forcedelleagueteam ') and is_admin:
        await force_delete_league_team_handler(db, message)

    elif lower_message.startswith('!updateteam ') and is_admin:
        await update_team_handler(db, message, client)

    elif lower_message.startswith('!giveteamtokens ') and is_admin:
        await give_team_tokens_handler(db, message)

    elif lower_message.startswith('!fanof'):
        await fan_of_handler(db, message)

    elif lower_message.startswith('!rivalof'):
        await rival_of_handler(db, message)

    elif lower_message.startswith('!bandforband '):
        await band_for_band_handler(db, message)


    # ADMIN COMMANDS

    # elif lower_message.startswith('!givesac ') and is_helper:
    #     await give_sac_handler(db, message, client)

    elif lower_message.startswith('!startauction') and is_admin:
        await start_auction_handler(db, message, client)

    elif lower_message == '!endauction' and is_admin:
        await end_auction_handler(db, message, client)

    elif lower_message.startswith('!fullevents') and is_admin:
        await full_events_handler(db, message)

    elif lower_message.startswith("!addevent") and is_admin:
        # !addevent|[event id]|[event name]|[max participants]|[0 for no pass, 1 for pass, 2 for subs]|[team size]|[event role id]|[event channel id]
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
        await send_msg(message.channel, 'Brackets have been wiped', '!wipebrackets')

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

        await send_next_info(db, message, guild, client)
        await notify_next_users(db, guild, message)


    elif lower_message.startswith('!endbattle') and is_admin:
        await end_battle_handler(db, message)

    elif lower_message == '!startbattle' and is_admin:
        await start_battle_handler(db, message, client)

    elif lower_message == '!hm' and is_admin:
        await how_many_handler(db, message)

    elif lower_message.startswith('!bns') and is_admin:
        await battle_no_show_handler(db, message)

    elif lower_message == '!endreg' and is_admin:
        await end_reg_handler(db, message, client)

    elif lower_message == '!battleteams' and is_admin:
        await battle_teams_handler(db, message)

    elif lower_message.startswith('!battlewin') and is_admin:
        await battle_win_handler(db, message, client)


    elif lower_message == '!testdata' and is_admin:

        test_sign_up_data = [
            533018500810276886, # simber
            210612137175941132, # bigmac
            311169693178134528, # teef
            931317668882051072, # dank solo cup
            724317013555675176, # counterwatch

            512806663271481365, # stats
            388322034658312196, # woofie
            852226927581331456, # jackiexpress
            712545218397732955, # mrbustdown
            576730780903145492 # gducke
        ]

        constants_db = db['constants']
        battle_obj = constants_db.find_one({'name': 'battle'})
        battle_info = battle_obj['value']
        battle_info['sign_ups'] = test_sign_up_data
        constants_db.update_one({"name": "battle"}, {"$set": {"value": battle_info}})
        await message.channel.send('test data set')

    elif lower_message.startswith('!newbet') and is_admin:
        # !newbets|title|home team name|away team name|uses home/away boolean (0/1)
        await new_bet_handler(db, message, client)

    elif lower_message.startswith('!bet'):
        await bet_handler(db, message)

    elif lower_message == '!mybets':
        await my_bets_handler(db, message, client) 

    elif lower_message.startswith('!finishbet') and is_admin:
        await finish_bet_handler(db, message, client)

    elif lower_message.startswith('!voidbet') and is_admin:
        await void_bet_handler(db, message, client)

    elif lower_message.startswith('!forcebattle') and is_admin:
        await force_battle_handler(db, message, client)

    elif lower_message.startswith('!forcemaketeam') and is_admin:
        await force_make_team_handler(db, message, client)

    elif lower_message.startswith('!forcedeleteteam') and is_admin:
        await force_delete_team_handler(db, message, client)

    elif lower_message.startswith('!forceaddteam') and is_admin:
        await force_add_team_handler(db, message, client)

    elif lower_message.startswith('!forceremoveteam') and is_admin:
        await force_remove_team_handler(db, message, client)

    elif lower_message.startswith('!forceremoveplayer') and is_admin:
        await force_remove_player_handler(db, message)

    elif lower_message.startswith('!forceleagueremove') and is_admin:
        await force_league_remove_handler(db, message, client)

    elif lower_message.startswith('!forceleagueadd') and is_admin:
        await force_league_add_handler(db, message, client)

    elif lower_message.startswith('!serverpoints ') and is_admin:
        await server_points_handler(db, message, client)

    elif lower_message.startswith('!twitch10') and is_cp_helper:
        await twitch_tokens_handler(client, db, message, 10)

    elif lower_message.startswith('!twitch50') and is_cp_helper:
        await twitch_tokens_handler(client, db, message, 50)

    elif lower_message.startswith('!twitchpass') and is_cp_helper:
        await twitch_pass_handler(client, db, message)

    elif lower_message.startswith('!twitchpack') and is_cp_helper:
        await twitch_pack_handler(client, db, message)

    elif lower_message == '!fortnite':
        await message.channel.send('fortnite')

    elif lower_message == '!sigma':
        await message.channel.send('https://i.imgur.com/2qptwSa.png')

    elif lower_message == '!howdy':
        await message.channel.send('https://tenor.com/view/good-morning-summer-mickey-mouse-gif-13892611')

    elif lower_message == '!thepoint':
        await message.channel.send('https://i.imgur.com/mwekfl2.png')

    elif lower_message == '!zorp':

        test_zorp = ['zorp?', 'bogos binted', 'pickenteen zumflood', 'porijug riwedor', 'zeriup zort', 'zorty zort', 'bering bering zrop', 'mrop mrop vorp', 'vropy vorp', 
                     'fortzorp', 'HELP ME IM TRAPPED HELP ME PLEASE HELP ME PLEASE IM NOT A DISCORD BOT HELP PLEASE HELP PLEASE', 'figeldeen zorpenstein']

        await message.channel.send(random.choice(test_zorp))

    elif lower_message == '!bee':

        await message.channel.send("Scripts.com Bee Movie By Jerry Seinfeld NARRATOR: (Black screen with text; The sound of buzzing bees can be heard) According to all known laws of aviation, : there is no way a bee should be able to fly. : Its wings are too small to get its fat little body off the ground. : The bee, of course, flies anyway : because bees don't care what humans think is impossible. BARRY BENSON: (Barry is picking out a shirt) Yellow, black. Yellow, black. Yellow, black. Yellow, black. : Ooh, black and yellow! Let's shake it up a little. JANET BENSON: Barry! Breakfast is ready! BARRY: Coming! : Hang on a second. (Barry uses his antenna like a phone) : Hello? ADAM FLAYMAN:(Through phone) - Barry? BARRY: - Adam? ADAM: - Can you believe this is happening? BARRY: - I can't. I'll pick you up. (Barry flies down the stairs) : MARTIN BENSON: Looking sharp. JANET: Use the stairs. Your father paid good money for those. BARRY: Sorry. I'm excited. MARTIN: Here's the graduate. We're very proud of you, son. : A perfect report card, all B's. JANET: Very proud. (Rubs Barry's hair) BARRY= Ma! I got a thing going here. JANET: - You got lint on your fuzz. BARRY: - Ow! That's me!JANET: - Wave to us! We'll be in row 118,000. - Bye! (Barry flies out the door) JANET: Barry, I told you, stop flying in the house! (Barry drives through the hive,and is waved at by Adam who is reading a newspaper) BARRY== - Hey, Adam. ADAM: - Hey, Barry. (Adam gets in Barry's car) : - Is that fuzz gel? BARRY: - A little. Special day, graduation. ADAM: Never thought I'd make it. (Barry pulls away from the house and continues driving) BARRY: Three days grade school, three days high school... ADAM: Those were awkward. BARRY: Three days college. I'm glad I took a day and hitchhiked around the hive. ADAM== You did come back different. (Barry and Adam pass by Artie, who is jogging) ARTIE: - Hi, Barry!")

    elif lower_message == '!testdm' and is_admin:

        guild = await get_guild(client)
        spicy_emoji = guild.get_emoji(1168952409125556304)
        default_msg = "Welcome to the Spicy OW "+str(spicy_emoji)+" Discord Server! I'm *Zenyatta*, the server's helper bot. "
        default_msg += "\n\nIf you're interested in joining a **League Team**, you can see which teams have applications open here: https://spicyragu.netlify.app/sol/apply"
        default_msg += '\n\nYou can also find more information about our League here: https://discord.com/channels/1130553449491210442/1178427939453411469'
        default_msg += '\n\nThank you for joining! If you have any questions, feel free to ask here: https://discord.com/channels/1130553449491210442/1166410753184632933'

        await message.channel.send(default_msg)

    elif lower_message.startswith('!8ball'):

        eight_ball = [
            'It is certain',
            'It is decidedly so',
            'Without a doubt',
            'Yes definitely',
            'You may rely on it',
            'Reply hazy, try again',
            'Ask again later',
            'Better not tell you now',
            'Cannot predict now',
            'Concentrate and ask again',
            "Don't count on it",
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Very doubtful'
        ]

        await message.channel.send(random.choice(eight_ball))

    elif lower_message.startswith('!thisgif'):

        await message.channel.send('https://i.imgur.com/J2jCzIb.png')

    elif lower_message.startswith('!initraffleconst') and is_admin:
        
        db_constants = db['constants']
        new_entry = {
            'name': 'raffle_total',
            'value': 0
        }
        db_constants.insert_one(new_entry)

        await message.channel.send('init success')

    elif lower_message == '!initwarningsconst' and is_admin:

        db_constants = db['constants']
        new_entry = {
            'name': 'warnings',
            'value': []
        }
        db_constants.insert_one(new_entry)
        await message.channel.send('warnings init complete')

    elif lower_message.startswith('!initrandomevent') and is_admin:

        db_constants = db['constants']
        new_entry = {
            'name': 'random_event',
            'last_event': 0,
            'event_msg_id': 0,
            'claimed': 0
        }
        db_constants.insert_one(new_entry)

        await message.channel.send('init success')

    elif lower_message == '!initcarddatabase' and is_admin:

        db_cards = db['cards']
        new_entry = {
            'cards': [],
            'cards_id': 1
        }
        db_cards.insert_one(new_entry)
        await message.channel.send('init success')

    elif lower_message == '!cardowners' and is_admin:

        await card_owners_handler(db, message)

    elif lower_message == '!wipecarddatabase' and is_admin:
        await wipe_card_database_handler(db, message)

    elif lower_message == '!initreselldatabase' and is_admin:

        db_cards = db['resell']
        new_entry = {
            'cards': {},
            'cards_id': 1
        }
        db_cards.insert_one(new_entry)
        await message.channel.send('init success')

    elif lower_message.startswith('!wipeplayercards ') and is_admin:
        await wipe_player_cards_handler(db, message)

    elif lower_message.startswith('!initcard ') and is_admin:

        await init_card_handler(db, message)

    elif lower_message.startswith('!initcustom ') and is_admin:

        await init_custom_handler(db, message)

    elif lower_message.startswith('!viewcard '):

        await view_card_handler(client, db, message)

    elif lower_message.startswith('!sellcard '):
        await sell_card_handler(db, message)

    elif lower_message.startswith('!givecard '):
        await give_card_handler(db, message)

    elif lower_message.startswith('!listcard '):
        await list_card_handler(db, message)

    elif lower_message.startswith('!unlistcard '):
        await unlist_card_handler(db, message)

    elif lower_message.startswith('!buycard '):
        await buy_card_handler(db, message)

    elif lower_message == '!openpack':
        await open_pack_handler(db, message)

    elif lower_message == '!totalpacks':
        await total_packs_handler(db, message)

    elif lower_message == '!cardmarket':
        await message.channel.send('Check out the SOL Card Market here!\n\nhttps://spicyragu.netlify.app/sol/card-market')

    elif lower_message == '!allcards':
        await message.channel.send('View all your cards here: https://spicyragu.netlify.app/sol/user-cards/'+str(message.author.id))

    elif lower_message == '!initcarddata':
        await init_card_data_db(db, message)

    elif lower_message == '!updatecarddata':
        await update_card_data_db(db, message)

    elif lower_message == '!updatepokedata':
        await update_poke_data_db(db, message)

    elif lower_message == '!resetraffle' and is_admin:
        db_constants = db['constants']
        db_constants.update_one({"name": 'raffle_total'}, {"$set": {"value": 0}})

        users = db['users']
        all_users = users.find()

        for user in all_users:
            if 'tickets' in user:
                users.update_one({"discord_id": user['discord_id']}, {"$set": {"tickets": 0}})

        await message.channel.send('Raffle reset')


    elif lower_message.startswith('!win ') and is_admin:

        # !win [winner 1 or 2]
        word_list = message.content.split()
        if len(word_list) == 2:
            guild = client.get_guild(constants.GUILD_ID)
            await won_match(int(word_list[1]), message, db, guild, client)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message.startswith('!noshow ') and is_admin:

        # !noshow [loser 1 or 2]
        word_list = message.content.split()
        if len(word_list) == 2:
            guild = client.get_guild(constants.GUILD_ID)
            await no_show(int(word_list[1]), message, db, guild, client)
        else:
            await message.channel.send("Invalid number of arguments.")

    elif lower_message == '!bothnoshow' and is_admin:

        guild = client.get_guild(constants.GUILD_ID)

        await both_no_show(message, db, guild, client)

    elif lower_message == '!rafflewinner' and is_admin:

        giant_array = []

        users = db['users']
        all_users = users.find()

        for user in all_users:
            if 'tickets' in user:
                for i in range(user['tickets']):
                    giant_array.append(user['battle_tag'])

        lucky_winner = random.choice(giant_array)

        await message.channel.send('The winner of the raffle is the user with the battle tag: '+lucky_winner)

    elif lower_message.startswith('!giverewards') and is_admin:
        
        reward_per_round = [25, 50, 100, 300, 1000, 2000, 2000, 2000]

        bracket = db['brackets'].find_one({'event_id': '34'})

        final_dict = {}

        # round_index = 0
        # for round in bracket['bracket']:
        #     for match in round:
        #         for player in match:
        #             if 'no_show' in player:
        #                 final_dict[str(player['user'])] = -1
        #             elif not ((player['is_bye']) or ('is_tbd' in player and player['is_tbd'])):
        #                 final_dict[str(player['user'])] = round_index

        #     round_index += 1

        round_index = 0
        for round in bracket['bracket']:
            for match in round:
                for bracket_team in match:
                    print(bracket_team)
                    if bracket_team['is_bye'] or ('is_tbd' in bracket_team and bracket_team['is_tbd']):
                        continue
                    elif 'no_show' in bracket_team:
                        team = await get_team_by_name(db, bracket_team['user'])
                        if team and 'members' in team:
                            for team_member in team['members']:
                                team_user = user_exists(db, team_member)
                                if team_user:
                                    final_dict[str(team_user['discord_id'])] = -1
                    else:
                        team = await get_team_by_name(db, bracket_team['user'])
                        if team and 'members' in team:
                            for team_member in team['members']:
                                team_user = user_exists(db, team_member)
                                if team_user:
                                    final_dict[str(team_user['discord_id'])] = round_index

            round_index += 1

        for player_id_string, highest_round in final_dict.items():

            is_valid = True
            # for invalid in invalid_gifts:
            #     if player_id_string == invalid:
            #         print('invalid player '+str(invalid))
            #         is_valid = False
            #         break

            if is_valid and highest_round > -1:
                user = db['users'].find_one({'discord_id': int(player_id_string)})
                if user:

                    reward = reward_per_round[highest_round]
                    await change_tokens(db, user, reward)
                    print('Giving '+str(reward)+' tokens to '+user['battle_tag'])

        await message.channel.send('Rewards given')

    elif lower_message == '!initstandings' and is_admin:

        standings = db['standings']
        new_standings = {
            # [win, loss]
            'season': 3,
            'teams': {
                'Olympians': [0, 0],
                'Polar': [0, 0],
                'Eclipse': [0, 0],
                'Saviors': [0, 0],
                'Ragu': [0, 0],
                'Instigators': [0, 0],
                'Guardians': [0, 0],
                'Fresas': [0, 0],
                'Outliers': [0, 0],
                'Phoenix': [0, 0],
                'Hunters': [0, 0],
                'Evergreen': [0, 0],
                'Saturn': [0, 0],
                'Celestials': [0, 0],
                'Misfits': [0, 0]
            },
            'divs': [
                ['Olympians', 'Eclipse', 'Phoenix', 'Hunters', 'Fresas'],
                ['Polar', 'Ragu', 'Outliers', 'Guardians', 'Evergreen'],
                ['Instigators', 'Saviors', 'Saturn', 'Celestials', 'Misfits']
            ]
        }
        standings.insert_one(new_standings)
        await message.channel.send('standings initated')


    elif lower_message == '!initauction' and is_admin:

        auction = db['auction']
        new_auction = {
            'auction_id': 1,
            'is_open': False,
            'item_name': 'NONE',
            'highest_bid': 0,
            'highest_bidder_id': 0
        }
        auction.insert_one(new_auction)
        await message.channel.send('auction data initated')

    elif lower_message == '!testgetconstant' and is_admin:
        constant_val = get_constant_value(db, 'test_constant')
        await message.channel.send('test constant is: '+constant_val)

    elif lower_message == '!testsetconstant' and is_admin:
        set_constant_value(db, 'test_constant', 'nuts')
        await message.channel.send('set test constant')

    elif lower_message.startswith('!addwin') and is_admin:
        await add_win_handler(db, message)

    elif lower_message.startswith('!addloss') and is_admin:
        await add_loss_handler(db, message)

    elif lower_message == '!initmaps' and is_admin:

        maps = db['maps']
        new_maps = {
            'maps_id': 1,
            'maps': {
                'map1': 'https://i.postimg.cc/zfLR8KKm/Samoa.webp',
                'map2': '',
                'map3': '',
                'map4': '',
                'map5': '',
                'map6': '',
                'map7': ''
            }
        }
        maps.insert_one(new_maps)
        await message.channel.send('maps initated')

    elif lower_message == '!initmapnames' and is_admin:

        map_names = db['mapnames']
        new_map_names = {
            'maps_id': 1,
            'maps': {
                'map1': '',
                'map2': '',
                'map3': '',
                'map4': '',
                'map5': '',
                'map6': '',
                'map7': ''
            }
        }
        map_names.insert_one(new_map_names)
        await message.channel.send('map names initated')

    elif lower_message == '!initlocalfiles' and is_admin:

        local_files = db['localfiles']
        # new_local_files = {
        #     'files_id': 1,
        #     'files': {
        #         'map_wins': {
        #             'version': 1,
        #             'data': {
        #                 'map1': 'None',
        #                 'map2': 'None',
        #                 'map3': 'None',
        #                 'map4': 'None',
        #                 'map5': 'None',
        #                 'map6': 'None',
        #                 'map7': 'None'
        #             }
        #         }
        #     }
        # }
        files = local_files.find_one({'files_id': 1})
        scores = {
            'version': 1,
            'data': {
                'score1': 0,
                'score2': 0,
                'score3': 8,
                'score4': 0
            }
        }
        files['files']['scores'] = scores

        local_files.update_one({"files_id": 1}, {"$set": {"files": files['files']}})
        await message.channel.send('local files updated')

    elif lower_message.startswith('!setmap') and is_admin:
        await set_map_handler(db, message)

    elif lower_message == '!resetmaps' and is_admin:
        await reset_maps_handler(db, message)

    elif lower_message.startswith('!resetmap ') and is_admin:
        await reset_map_handler(db, message)

    elif lower_message.startswith('!setwin') and is_admin:
        await set_win_handler(db, message)

    elif lower_message == '!resetwins' and is_admin:
        await reset_wins_handler(db, message)

    elif lower_message.startswith('!setscore') and is_admin:
        await set_score_handler(db, message)

    elif lower_message == '!resetscores' and is_admin:
        await reset_scores_handler(db, message)

    elif lower_message == '!initschedule' and is_admin:

        new_schedule = {
            'season': 3,
            'weeks': [
                {
                    'week': 1,
                    'matches': [
                        ['June 1st (Sat) : Match 1' ,'Hunters', 'Fresas'],
                        ['June 1st (Sat) : Match 2', 'Evergreen', 'Polar'],
                        ['June 1st (Sat) : Match 3', 'Instigators', 'Celestials'],
                        ['June 2nd (Sun) : Match 1', 'Eclipse', 'Phoenix'],
                        ['June 2nd (Sun) : Match 2', 'Guardians', 'Outliers'],
                        ['June 2nd (Sun) : Match 3', 'Saturn', 'Misfits'],
                    ]
                },
                {
                    'week': 2,
                    'matches': [
                        ['June 8th (Sat) : Match 1' ,'Phoenix', 'Olympians'],
                        ['June 8th (Sat) : Match 2', 'Ragu', 'Outliers'],
                        ['June 8th (Sat) : Match 3', 'Saviors', 'Saturn'],
                        ['June 9th (Sun) : Match 1', 'Eclipse', 'Hunters'],
                        ['June 9th (Sun) : Match 2', 'Guardians', 'Evergreen'],
                        ['June 9th (Sun) : Match 3', 'Celestials', 'Misfits'],
                    ]
                },
                {
                    'week': 3,
                    'matches': [
                        ['June 15th (Sat) : Match 1' ,'Phoenix', 'Hunters'],
                        ['June 15th (Sat) : Match 2', 'Polar', 'Guardians'],
                        ['June 15th (Sat) : Match 3', 'Celestials', 'Saviors'],
                        ['June 16th (Sun) : Match 1', 'Olympians', 'Fresas'],
                        ['June 16th (Sun) : Match 2', 'Evergreen', 'Ragu'],
                        ['June 16th (Sun) : Match 3', 'Misfits', 'Instigators'],
                    ]
                },
                {
                    'week': 4,
                    'matches': [
                        ['June 22nd (Sat) : Match 1' ,'Fresas', 'Eclipse'],
                        ['June 22nd (Sat) : Match 2', 'Outliers', 'Evergreen'],
                        ['June 22nd (Sat) : Match 3', 'Saviors', 'Instigators'],
                        ['June 23rd (Sun) : Match 1', 'Hunters', 'Olympians'],
                        ['June 23rd (Sun) : Match 2', 'Polar', 'Ragu'],
                        ['June 23th (Sun) : Match 3', 'Saturn', 'Celestials'],
                    ]
                },
                {
                    'week': 5,
                    'matches': [
                        ['June 29th (Sat) : Match 1' ,'Olympians', 'Eclipse'],
                        ['June 29th (Sat) : Match 2', 'Ragu', 'Guardians'],
                        ['June 29th (Sat) : Match 3', 'Instigators', 'Saturn'],
                        ['June 30th (Sun) : Match 1', 'Fresas', 'Phoenix'],
                        ['June 30th (Sun) : Match 2', 'Outliers', 'Polar'],
                        ['June 30th (Sun) : Match 3', 'Misfits', 'Saviors'],
                    ]
                },
            ]
        }

        schedule = db['schedule']
        schedule.insert_one(new_schedule)
        await message.channel.send('Schedule inserted')
        
    elif lower_message.startswith('!givetokens ') and is_admin:

        # !givetokens [winner id] [tokens]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_tokens_command(client, db, word_list[1], int(word_list[2]), message)
        else:
            await message.channel.send("Invalid number of arguments.")

    # elif lower_message == '!helpersalary' and is_helper:
    #     await helper_salary_handler(db, message, client)

    elif lower_message.startswith('!givexp ') and (is_admin or is_league_helper):
        await give_xp_handler(client, db, message)

    elif lower_message.startswith('!esub ') and is_admin:
        await e_sub_handler(client, db, message)

    elif lower_message.startswith('!setlevel ') and is_admin:
        await set_level_handler(client, db, message)

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

    elif lower_message.startswith('!givepickaxes ') and is_admin:

        # !givepickaxes [winner id] [pickaxes]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_pickaxes_command(client, db, word_list[1], int(word_list[2]), message)
        else:
            await send_msg(message.channel, 'Invalid number of arguments.', '!givepickaxes')

    elif lower_message.startswith('!givepacks ') and (is_admin or is_tp_helper):

        # !givepacks [winner id] [packs]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_packs_command(client, db, word_list[1], float(word_list[2]), message)
        else:
            await send_msg(message.channel, 'Invalid number of arguments.', '!givepacks')

    elif lower_message.startswith('!givegems ') and is_admin:
        await give_gems_handler(db, message, client)

    elif lower_message.startswith('!giverandomgem ') and is_admin:
        await give_random_gem_handler(db, message, client)

    elif lower_message.startswith('!givelootbox ') and is_admin:
        await give_lootbox_handler(db, message, client)

    elif lower_message.startswith('!givetwitchlootbox') and is_admin:
        await give_twitch_lootbox_handler(db, message, client)

    elif lower_message.startswith('!giveallboxes') and is_admin:

        users = db['users']

        for member in client.get_all_members():
            user = user_exists(db, member.id)
            if not user:
                continue
            user_boxes = []
            level, _ = get_lvl_info(user)
            increase_int = 2
            while level >= increase_int:
                user_boxes.append(increase_int)
                increase_int += 1

            users.update_one({"discord_id": user['discord_id']}, {"$set": {"lootboxes": user_boxes}})

        await send_msg(message.channel, 'boxes given', '!giveallboxes')

    elif lower_message == '!givesubboxes' and is_admin:
        await give_sub_boxes_handler(db, message, client)

    elif lower_message == '!prunesac' and is_admin:
        await prune_sac_handler(db, message, client)

    elif lower_message.startswith('!open '):
        await open_handler(db, message, client)

    elif lower_message.startswith('!sellgems '):
        await sell_gems_handler(db, message)

    elif lower_message == '!tradegemset':
        await trade_gem_set_handler(db, message)

    elif lower_message.startswith('!tradegem '):
        await trade_gem_handler(db, message)

    elif lower_message == '!denygemtrade':
        await deny_gem_trade_handler(db, message)

    elif lower_message == '!acceptgemtrade':
        await accept_gem_trade_handler(db, message)

    elif lower_message == '!listids' and is_admin:

        for member in client.get_all_members():

            user = user_exists(db, member.id)
            if user:

                print(member.display_name+" : "+str(member.id) + " : "+user['battle_tag'])

    elif lower_message.startswith('!addpoke') and is_admin:
        # !addpoke id type img_link 
        await add_poke_handler(db, message)

    elif lower_message == '!openpoke':
        await open_poke_handler(db, message)

    elif lower_message.startswith('!sellpoke '):
        await sell_poke_handler(db, message)

    elif lower_message.startswith('!viewpoke '):
        await view_poke_handler(db, message)

    elif lower_message == '!mypokes':
        await my_pokes_handler(db, message)

    elif lower_message == '!allpokes':
        await all_pokes_handler(message)

    elif lower_message == '!unopened':
        await message.channel.send('Check out the full list of unopened Pokemon Cards here! https://spicyragu.netlify.app/poke/unopened')

    elif lower_message == '!setpokedex' and is_admin:
        users = db['users']
        all_users = users.find()
        num_affected = 0
        for user in all_users:

            if not ('poke_cards' in user):
                continue

            poke_cards = user['poke_cards']
            user_pokedex = get_pokedex(db, poke_cards)    
            users.update_one({"discord_id": user['discord_id']}, {"$set": {"pokedex": user_pokedex}})
            num_affected += 1

        await message.channel.send('Complete. '+str(num_affected)+' users affected.')

    elif lower_message == '!setsorts':

        pokemon = db['pokemon']
        all_pokes = pokemon.find()

        for poke in all_pokes:

            sort_index = get_sort_index(poke['set'], poke['set_num'])
            pokemon.update_one({"card_id": poke['card_id']}, {"$set": {"sort": sort_index}})

        await message.channel.send('done')

    elif lower_message.startswith('!givepp ') and is_admin:
        await give_pp_handler(db, message, client)

    elif lower_message.startswith('!getdetails '):
        # !getdetails [username]
        await get_details_handler(db, message, client, is_admin)
    elif lower_message == '!wipeteams' and is_admin:
        await wipe_teams_handler(db, message)
    elif lower_message == '!totaltokens' and is_admin:
        await total_tokens_handler(db, message)
    elif lower_message == '!totalleague' and is_admin:
        await total_league_handler(db, message)
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
    elif lower_message.startswith('!setitemprice') and is_admin:
        await set_item_price_handler(db, message)
    elif lower_message.startswith('!makepublic') and is_admin:
        await make_public_handler(db, message)
    elif lower_message.startswith('!closeevent') and is_admin:
        await close_event_handler(db, message)
    elif lower_message.startswith('!setstock') and is_admin:
        await set_stock_handler(db, message)
    elif lower_message.startswith('!say') and is_helper:
        
        rest = message.content[len("!say "):].strip()
        guild = await get_guild(client)
        chat_channel = guild.get_channel(constants.CHAT_CHANNEL)
        await send_msg(chat_channel, rest, '!say')

    elif lower_message.startswith('!deletebytag ') and is_admin:
        await delete_by_tag_handler(db, message)

    elif lower_message == '!givealllevels' and is_admin:

        guild = await get_guild(client)
        for member in client.get_all_members():
            user = user_exists(db, member.id)
            if user:
                level, _ = get_lvl_info(user)
                level_role_id = get_role_id_by_level(level)
                level_role = guild.get_role(level_role_id)
                await give_role(member, level_role, 'Give All Levels')

        await send_msg(message.channel, 'all done', '!givealllevels')

    elif lower_message.startswith('!postreplay ') and is_admin:
        vod_link = message.content.split()[1]
        guild = await get_guild(client)
        clips_channel = guild.get_channel(constants.CLIPS_CHANNEL)
        await clips_channel.send('A new SOL Replay has been posted on YouTube! Go check it out! '+vod_link)

    elif lower_message == '!getavatar':
        avatar = message.author.display_avatar
        if avatar:
            avatar_link = avatar.url
            await message.channel.send('('+avatar_link+')')
        else:
            await message.channel.send('Problem getting avatar')

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

    elif lower_message == 'check long' and is_push_bot:
        bot_channel = client.get_channel(constants.BOT_CHAT_CHANNEL)
        await send_msg(bot_channel, 'Updating Bets', 'Check Long')
        # await give_sub_boxes_handler(db, message, client)
        # await prune_sac_handler(db, message, client)
        await update_bets(db, message.channel, client)

    elif lower_message == 'check gifts' and is_push_bot:
        bot_channel = client.get_channel(constants.BOT_CHAT_CHANNEL)
        await send_msg(bot_channel, 'Checking gifts', 'Check Gifts')
        guild = await get_guild(client)
        gift_notifs_role_id = constants.GIFT_ROLE_ID
        gift_notifs_role = await get_role_by_id(client, gift_notifs_role_id)

        users = db['users']
        users_notified = 0

        bot_coms_channel = guild.get_channel(constants.BOT_CHANNEL)

        for member in guild.members:
            if gift_notifs_role in member.roles:
                user = user_exists(db, member.id)
                if user:
                    knows = get_knows_gift(user)
                    if not knows:
                        last_gift = get_last_gift(user)
                        long_enough, _ = long_enough_for_gift(last_gift)
                        if long_enough:
                            users.update_one({"discord_id": user['discord_id']}, {"$set": {"knows_gift": True}})
                            await notify_user_of_gift(member, bot_coms_channel)
                            users_notified += 1
                            await asyncio.sleep(1)

        await send_msg(message.channel, str(users_notified)+' users notified of having a gift', 'Check Gifts')

        await send_msg(message.channel, 'Checking payroll', 'Check Payroll')

        await check_payroll(db, message.channel)

        await check_auction(db, message.channel, client)

        await check_weekly(client, db, message.channel, message)

        await check_token_issue(db, message.channel)

        await check_streamlabs_raffles(db, message.channel)

    else:
        await send_msg(message.channel, 'Invalid command. Please see **!help** for a list of commands.', 'Invalid Command')

def run_discord_bot(db):
    intents = discord.Intents.all()
    intents.message_content = True
    intents.reactions = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))

    @client.event
    async def on_raw_reaction_add(payload):
    
        message_id = payload.message_id
        member = payload.member
        channel_id = payload.channel_id

        if channel_id == constants.XP_BATTLE_CHANNEL:

            if member.id == constants.ZEN_ID:
                return
            
            constants_db = db['constants']
            battle_obj = constants_db.find_one({'name': 'battle'})
            battle_info = battle_obj['value']
            if message_id == battle_info['reg_message_id']:
                await add_to_battle(db, member, battle_info, client)
            
            return

        if channel_id == constants.CHAT_CHANNEL and member.id != constants.ZEN_ID:
            emoji = payload.emoji
            if str(emoji) == '❗':
                await react_to_event(db, client, message_id, member)

        if message_id == constants.SERVER_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.SERVER_NOTIFS_ROLE)
            await remove_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.TOURNEY_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
            await remove_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.TWITCH_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.TWITCH_NOTIFS_ROLE)
            await remove_role(member, role, 'Raw Reaction Add')
        elif message_id == constants.GIFT_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.GIFT_ROLE_ID)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id == constants.TOKEN_SHOP_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.TOKEN_NOTIF_ROLE_ID)
            await give_role(member, role, 'Raw Reaction Add')
        elif channel_id == constants.REACTION_ROLE_CHANNEL:
            if message_id in constants.HERO_MESSAGE_TO_ROLE:
                role_id = constants.HERO_MESSAGE_TO_ROLE[message_id]
                guild = await get_guild(client)
                role = guild.get_role(role_id)
                await give_role(member, role, 'Reaction Roles')

        else:

            await check_for_black_jack(db, payload.channel_id, message_id, member, payload.emoji, client)

    @client.event
    async def on_raw_reaction_remove(payload):
        guild = await get_guild(client)
        message_id = payload.message_id
        channel_id = payload.channel_id
        user_id = payload.user_id

        if channel_id == constants.XP_BATTLE_CHANNEL:

            if user_id == constants.ZEN_ID:
                return
            
            member = get_member(guild, user_id, 'Raw Reaction Remove')

            constants_db = db['constants']
            battle_obj = constants_db.find_one({'name': 'battle'})
            battle_info = battle_obj['value']
            if message_id == battle_info['reg_message_id']:
                await remove_from_battle(db, member, battle_info)
            
            return

        if message_id == constants.SERVER_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.SERVER_NOTIFS_ROLE)
            await give_role(member, role, 'Notifs Settings')
        elif message_id ==  constants.TOURNEY_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
            await give_role(member, role, 'Notifs Settings')
        elif message_id ==  constants.TWITCH_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.TWITCH_NOTIFS_ROLE)
            await give_role(member, role, 'Notifs Settings')
        elif message_id ==  constants.GIFT_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.GIFT_ROLE_ID)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id ==  constants.TOKEN_SHOP_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.TOKEN_NOTIF_ROLE_ID)
            await remove_role(member, role, 'Notifs Settings')
        elif channel_id == constants.REACTION_ROLE_CHANNEL:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            if message_id in constants.HERO_MESSAGE_TO_ROLE:
                role = guild.get_role(constants.HERO_MESSAGE_TO_ROLE[message_id])
                await remove_role(member, role, 'Raw Reaction Add')

    @client.event
    async def on_member_join(member):
        guild = client.get_guild(constants.GUILD_ID)
        role = guild.get_role(constants.MEMBER_ROLE_ID)
        server_notifs = guild.get_role(constants.SERVER_NOTIFS_ROLE)
        tourney_notifs = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
        twitch_notifs = guild.get_role(constants.TWITCH_NOTIFS_ROLE)
        level_1_id = get_role_id_by_level(1)
        level_1_role = guild.get_role(level_1_id)

        if role is not None:

            registered_user = user_exists(db, member.id)
            if registered_user:
                registered_role = guild.get_role(constants.REGISTERED_ROLE)
                await member.add_roles(role, server_notifs, tourney_notifs, twitch_notifs, level_1_role, registered_role)
            else:
                await member.add_roles(role, server_notifs, tourney_notifs, twitch_notifs, level_1_role)

        try:

            guild = await get_guild(client)
            spicy_emoji = guild.get_emoji(1168952409125556304)
            default_msg = "Welcome to the Spicy OW "+str(spicy_emoji)+" Discord Server! I'm *Zenyatta*, the server's helper bot. "
            default_msg += "\n\nIf you're interested in joining a **League Team**, you can apply to as many teams as you'd like here: https://spicyragu.netlify.app/sol/apply"
            default_msg += '\n\nFeel free to check out this short video which explains how to find a team to join! https://www.youtube.com/watch?v=EN_f4rr-sCQ'
            default_msg += '\n\nYou can also find more information about our League here: https://discord.com/channels/1130553449491210442/1178427939453411469'
            default_msg += '\n\nThank you for joining! If you have any questions, feel free to ask our friendly staff here: https://discord.com/channels/1130553449491210442/1202441473027477504'

            await member.send(default_msg)
        except Exception:
            print('Could not DM user.')


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        try:
            await handle_message(message, db, client)
        except aiohttp.client_exceptions.ClientOSError as e:
            if e.errno == 104:
                await send_msg(message.channel, 'Network error. Please try your command again.', 'Network Error')
        except discord.errors.NotFound as e:
            await send_msg(message.channel, 'ERROR: I tried to delete a message but it was already deleted.', '404 Error')
        except Exception as e:
            print(e)
            traceback.print_exc()
            guild = client.get_guild(constants.GUILD_ID)
            spicy_member = get_member(guild, constants.SPICY_RAGU_ID, 'Error Notify') 
            await send_msg(message.channel, 'Whoops... An error occured. Let me notify staff. '+spicy_member.mention, 'Whoops message')
            err_channel = guild.get_channel(constants.ERROR_LOGS_CHANNEL)
            traceback_str = traceback.format_exc()
            await send_msg(err_channel, traceback_str, 'Error Channel')


    print('about to run client')
    client.run(constants.DISCORD_TOKEN)
    print('client ran')