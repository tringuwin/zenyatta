import asyncio
import random
import time
from admin_handlers.free import free_handler
from admin_handlers.give_vouchers import give_vouchers
from admin_handlers.reset_token_tracker import reset_token_tracker_handler
from admin_handlers.set_desc import set_desc_handler
from admin_handlers.slowmode import slowmode_handler
from admin_handlers.take_vouchers import take_vouchers
from automation.casting.ban_hero import ban_hero_handler
from automation.casting.first_pick import first_pick_handler
from coin.donate_vouchers import donate_vouchers
from coin.redeem_trophies import redeem_trophies
import discord
import aiohttp
import uuid
from datetime import timedelta
from admin_handlers.cancel_vote import cancel_vote_handler
from admin_handlers.delete_by_tag import delete_by_tag_handler
from admin_handlers.end_vote import end_vote_handler
from admin_handlers.feature import feature_handler
from admin_handlers.fix_standings import fix_standings_handler
from admin_handlers.force_add_team import force_add_team_handler
from admin_handlers.force_battle_handler import force_battle_handler
from admin_handlers.force_delete_team import force_delete_team_handler
from admin_handlers.force_league_remove import force_league_remove_handler
from admin_handlers.force_make_team import force_make_team_handler
from admin_handlers.force_remove_player.force_remove_player import force_remove_player_handler
from admin_handlers.force_remove_team import force_remove_team_handler
from admin_handlers.force_twitch import force_twitch_handler
from admin_handlers.full_events import full_events_handler
from admin_handlers.gen_bracket import gen_bracket_handler
from admin_handlers.give_gems import give_gems_handler
from admin_handlers.give_lootbox import give_lootbox_handler
from admin_handlers.give_random_gem import give_random_gem_handler
from admin_handlers.give_sub_boxes import give_sub_boxes_handler
from admin_handlers.give_twitch_lootbox import give_twitch_lootbox_handler
from admin_handlers.give_xp import give_xp_handler
from admin_handlers.make_50_codes import make_50_codes_handler
from admin_handlers.make_vote import make_vote_handler
from admin_handlers.match_lineups import match_lineups_handler
from admin_handlers.prune_picks import prune_picks
from admin_handlers.register_role import register_role
from admin_handlers.score_picks import score_picks
from admin_handlers.set_item_price import set_item_price_handler
from admin_handlers.set_level import set_level_handler
from admin_handlers.sub_rewards import gift_rewards_handler, sub_rewards_handler
from admin_handlers.total_league import total_league_handler
from admin_handlers.wipe_past_teams import wipe_past_teams
from auction import check_auction
from automation.casting.swap_sides import swap_sides
from automation.casting.update_score import add_point, remove_point
from automation.notify_about_matches import check_notify_about_matches
from automation.process_trophy_rewards.process_trophy_rewards import process_trophy_rewards
from automation.schedule_plan.add_week.add_week import add_week
from automation.schedule_plan.make_schedule_plan import make_schedule_plan
from automation.schedule_plan.schedule_plan_loop.schedule_plan_loop import schedule_plan_loop
from automation.update_team_avatars import update_overwatch_team_avatars, update_rivals_team_avatars, update_valorant_team_avatars
from automation.update_top_subs_avatars import update_top_subs_avatars
from card_automation import make_all_cards_from_data, make_all_cards_from_db
from card_games.automation.clear_expired_battles import clear_expired_battles
from card_games.card_battle import card_battle
from card_games.feed_gem import feed_gem
from card_games.fight_card import fight_card
from card_matches.card_match_utils import make_match_card
from cards import buy_card_handler, cards_handler, edit_card_handler, force_unlist, give_card_handler, init_card_handler, init_custom_handler, list_card_handler, make_card_handler, open_pack_handler, release_cards, sell_all_cards_handler, sell_card_handler, total_cards_handler, total_packs_handler, unlist_card_handler, view_card_handler, wipe_card_database_handler, wipe_player_cards_handler
from casting.bal import bal_handler
from casting.delete_caster import delete_caster_handler
from casting.make_caster import make_caster_handler
from casting.make_lobby_admin import make_lobby_admin_handler
from casting.pay import pay_handler
from coin.coin_price import coin_price
from coin.coin_stats import coin_stats
from command_handlers.accept_gem_trade import accept_gem_trade_handler
from command_handlers.auction.bid import bid_handler
from command_handlers.auction.end_auction import end_auction_handler
from command_handlers.auction.start_auction import start_auction_handler
from command_handlers.auction_timer import auction_timer_handler
from command_handlers.bandforband import band_for_band_handler
from command_handlers.battle_leaderboard import battle_leaderboard_handler
from command_handlers.bets.bet import bet_handler
from command_handlers.bets.finish_bet import finish_bet_handler
from command_handlers.bets.my_bets import my_bets_handler
from command_handlers.bets.new_bet import check_open_bets, new_bet_handler, update_bets
from command_handlers.bets.void_bet import void_bet_handler
from command_handlers.blackjack import blackjack_handler, check_for_black_jack
from command_handlers.bonus.eight_ball import eight_ball_handler
from command_handlers.bracket import bracket_handler
from command_handlers.buy_ticket import buy_ticket_handler
from command_handlers.card_page import card_page
from command_handlers.card_search import card_search_handler
from command_handlers.deny_gem_trade import deny_gem_trade_handler
from command_handlers.donate import donate_handler
from command_handlers.donate_gems import donate_gems
from command_handlers.donate_packs import donate_packs
from command_handlers.drop_alert import drop_alert
from command_handlers.drop_bank import drop_bank_handler
from command_handlers.drop_bank_add import drop_bank_add_handler
from command_handlers.drops import drops
from command_handlers.faceit.set_tourney_team_color import set_tourney_team_color
from command_handlers.faceit.set_tourney_team_name import set_tourney_team_name
from command_handlers.faceit.set_tourney_team_score import set_tourney_team_score
from command_handlers.faceit.swap_tourney_teams import swap_tourney_teams
from command_handlers.funding import funding_handler
from command_handlers.gems import gems_handler
from command_handlers.getdetails import get_details_handler
from command_handlers.gg_ez import gg_ez_handler
from command_handlers.gift import gift_handler
from command_handlers.gp import gp_handler
from command_handlers.hello import hello_handler
from command_handlers.help.help_ally import help_ally_handler
from command_handlers.help.help_bonus import help_bonus_handler
from command_handlers.help.help_cards import help_cards_handler
from command_handlers.help.help_casino import help_casino_handler
from command_handlers.help.help_drops import help_drops_handler
from command_handlers.help.help_gems import help_gems_handler
from command_handlers.help.help_league import help_league_handler
from command_handlers.help.help_league_admin import help_league_admin_handler
from command_handlers.invited_by import invited_by_handler
from command_handlers.leaderboard import leaderboard_handler
from command_handlers.league.call_me import call_me_handler
from command_handlers.league.ff_match import ff_match_handler
from command_handlers.league.first_map import first_map_handler
from command_handlers.league.picks.picks import picks_handler
from command_handlers.league.score_match import score_match_handler
from command_handlers.league.sol_week_end import sol_week_end
from command_handlers.league.swiss_matchups import swiss_matchups_handler
from command_handlers.league.timeslot import timeslot_handler
from command_handlers.league.unschedule import unschedule_handler
from command_handlers.league.weekly_roster_reset import weekly_roster_reset
from command_handlers.league.sol_weekly_pay import sol_weekly_pay
from command_handlers.league.init_standings import init_standings
from command_handlers.league.make_sol_match import make_sol_match
from command_handlers.league.make_sol_week import bump_sol_week, make_sol_week
from command_handlers.league.add_loss import add_loss_handler
from command_handlers.league.add_win import add_win_handler
from command_handlers.league.ally.accept_ally import accept_ally_handler
from command_handlers.league.ally.accept_rival import accept_rival_handler
from command_handlers.league.ally.ally_request import ally_request_handler
from command_handlers.league.ally.ally_requests import ally_requests_handler
from command_handlers.league.ally.cancel_ally import cancel_ally_handler
from command_handlers.league.ally.cancel_rival import cancel_rival_handler
from command_handlers.league.ally.del_ally import del_ally_handler
from command_handlers.league.ally.del_rival import del_rival_handler
from command_handlers.league.ally.deny_ally import deny_ally_handler
from command_handlers.league.ally.deny_rival import deny_rival_handler
from command_handlers.league.ally.rival_request import rival_request_handler
from command_handlers.league.ally.rival_requests import rival_requests_handler
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
from command_handlers.league.league_xp import league_xp_handler, total_league_xp_handler, wipe_league_xp_handler
from command_handlers.league.make_league_team import make_league_team_handler
from command_handlers.league.make_team_admin import make_team_admin_handler
from command_handlers.league.map_diff import map_diff_handler
from command_handlers.league.match_end import match_end_handler
from command_handlers.league.next_week import next_week_handler
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
from command_handlers.league.set_lineup import set_lineup_handler
from command_handlers.league.set_map import set_map_handler
from command_handlers.league.set_min_rank import set_min_rank_handler
from command_handlers.league.set_score import set_score_handler
from command_handlers.league.set_win import set_win_handler
from command_handlers.league.standings import standings2_handler, standings_handler
from command_handlers.league.toggle_apps import toggle_apps_handler
from command_handlers.league.update_team import update_team, update_team_handler
from command_handlers.league.wipe_team import wipe_team
from command_handlers.lootboxes import lootboxes_handler
from command_handlers.mine import mine_handler
from command_handlers.money.give_money import give_money
from command_handlers.money.money import money
from command_handlers.next_drop import next_drop
from command_handlers.open import open_handler
from command_handlers.open_drop import open_drop
from command_handlers.portal.portal import portal_handler
from command_handlers.redeem_code import redeem_code
from command_handlers.revive import revive_handler
from command_handlers.rp import rp_handler
from command_handlers.slime import slime_handler
from command_handlers.team_page import team_page_handler
from command_handlers.top_100 import top_100_handler
from command_handlers.twitch import twitch_handler
from command_handlers.twitch_api.end_pred import end_pred
from command_handlers.twitch_api.raid import raid_handler
from command_handlers.twitch_api.raid_channel import raid_channel
from command_handlers.twitch_api.run_ad import run_ad
from command_handlers.twitch_api.start_pred import start_pred
from command_handlers.vote import vote_handler
from command_handlers.website import website_handler
from command_handlers.xp_battle.battle_helpers import get_battle_constant_name
from command_handlers.xp_battle.battle_no_show import battle_no_show_handler
from command_handlers.xp_battle.battle_teams import battle_teams_handler
from command_handlers.xp_battle.battle_win import battle_win_handler
from command_handlers.xp_battle.end_battle import end_battle_handler
from command_handlers.xp_battle.end_reg import end_reg_handler
from command_handlers.xp_battle.start_battle import start_battle_handler
from discord_utils.member_join.member_join import member_joined
from discord_utils.member_left.member_left import member_left
from exceptions import CommandError
from lineups import check_lineup_tokens
from command_handlers.profile.profile import profile_handler
from command_handlers.raffle import raffle_handler
from command_handlers.random_map import random_map_handler
from command_handlers.rps import rps_handler
from command_handlers.sell_gems import sell_gems_handler
from command_handlers.solo_join import solo_join_handler
from command_handlers.sub_timer import sub_timer_handler
from command_handlers.suggest import suggest_handler
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
from command_handlers.help.help import help_handler
from command_handlers.wager import wager_handler
from bracket import both_no_show, gen_tourney, no_show, notify_next_users, send_next_info, wipe_tourney, won_match
from discord_actions import get_guild, get_role_by_id, is_dm_channel, member_has_role, member_has_state_role
from helper_handlers.twitch_pack import twitch_pack_handler
from helper_handlers.twitch_tokens import twitch_tokens_handler
from helpers import get_constant_value, is_bot_commands_channel, make_string_from_word_list, set_constant_value
from api import get_member, give_role, remove_role
from mongo import output_packs, output_pickaxes, output_tokens, switch_matches
from payroll import check_payroll
from random_event.check_random_event_on_message import check_random_event_on_message
from random_event.random_event import react_to_event
from rewards import give_packs_command, give_pickaxes_command, give_tokens_command, sell_pickaxe_for_tokens
from roster_lock import handle_lock
from route_messages.dm_messages.route_dm_message import route_dm_message
from route_messages.rivals_message.route_rivals_message import route_rivals_message
from route_messages.utils.get_context import get_context
from route_messages.valorant_message.route_rivals_message import route_valorant_message
from safe_send import safe_reply, safe_send, safe_send_test
from savage_scovi import savage_scovi
from server_level import sub_points_handler
from streamlabs import check_streamlabs_raffles
from supporters.role_commands.role_color import role_color
from supporters.role_commands.role_name import role_name
from supporters.supporter_role_loop import supporter_role_loop
from time_helpers import check_weekly, long_enough_for_gift
from twitch_token import check_token_issue
from user.user import get_knows_gift, get_last_gift, get_lvl_info, notify_user_of_gift, user_exists
from user_input.bad_word_checker import bad_word_checker
from user_input.non_tenor_link import non_tenor_link
from xp_battles import add_to_battle, how_many_handler, remove_from_battle
from wipe_bracket import wipe_bracket_handler
from switch_matches import switch_matches_handler
from gen_tourney import gen_tourney_handler

def is_valid_channel(message, lower_message, is_helper, is_push_bot, is_tourney_admin):

    if is_helper or is_push_bot or is_tourney_admin:
        return True, None

    # Wager Command
    if lower_message.startswith('!wager'):
        if message.channel.id != constants.ROULETTE_CHANNEL:
            return False, 'Please only use the wager command in the Roulette Channel.'

    # Blackjack Command
    elif lower_message.startswith('!blackjack'):
        if message.channel.id != constants.BLACKJACK_CHANNEL:
            return False, 'Please only use the blackjack command in the Blackjack Channel.'

    # Mine Command
    elif lower_message.startswith('!mine'):
        if message.channel.id != constants.MINE_CHANNEL:
            return False, 'Please only use the mine command in the Mineshaft Channel.'

    # RPS Command
    elif lower_message.startswith('!rps'):
        if message.channel.id != constants.RPS_CHANNEL:
            return False, 'Please only use the rps command in the RPS Channel.'

    # Open Pack Command
    elif lower_message.startswith('!openpack'):
        if message.channel.id != constants.PACK_OPEN_CHANNEL:
            return False, 'Please only open packs in the packs opening channel: https://discord.com/channels/1130553449491210442/1233596350306713600'

    # Open Drop Command
    elif lower_message.startswith('!opendrop'):
        if message.channel.id != constants.OPENING_DROPS_CHANNEL:
            return False, 'Please only open drops in the drops opening channel: https://discord.com/channels/1130553449491210442/1332055598057001021'
    
    return True, None



async def handle_message(message, db, client):

    if is_dm_channel(message.channel):
        await route_dm_message(db, message)
        return
    
    # does this get used?
    channel = str(message.channel)
    
    context = get_context(message)
    
    has_bad_word = bad_word_checker(message.content)
    if has_bad_word:
        guild = await get_guild(client)
        mods_channel = guild.get_channel(constants.MODS_CHANNEL)
        await message.author.timeout(timedelta(days=7))
        await safe_send(mods_channel, message.author.name+' was timed out for saying **'+message.content+'**\n\nPlease verify if this timeout was correct and take action on it.')
        await message.delete()
        return

    user_message = str(message.content)
    is_admin = (message.author.id == constants.SPICY_RAGU_ID or message.author.id == 979526718186459206)
    is_tier_3_mod = (not message.author.bot) and member_has_role(message.author, constants.TIER_3_MOD_ROLE_ID)
    is_helper = (not message.author.bot) and member_has_role(message.author, constants.HELPER_ROLE_ID)
    is_xp_helper = (not message.author.bot) and member_has_role(message.author, constants.XP_HELPER_ROLE_ID)
    is_cp_helper = (not message.author.bot) and member_has_role(message.author, constants.CHANNEL_POINTS_ROLE_ID)
    is_tp_helper = (not message.author.bot) and member_has_role(message.author, constants.TWITCH_PACKS_ROLE_ID)
    is_tourney_admin = (not message.author.bot) and member_has_role(message.author, constants.TOURNEY_COMMANDS_PERMS_ROLE)
    is_state_captain = (not message.author.bot) and member_has_role(message.author, constants.STATE_CAPTAIN_ROLE)
    has_image_perms = message.author.bot or member_has_role(message.author, constants.IMAGE_PERMS_ROLE)
    is_push_bot = (message.author.id == constants.PUSH_BOT_ID)

    lower_message = user_message.lower()
    if (not has_image_perms) and ( lower_message.find('discord.gg') != -1 or (non_tenor_link(lower_message)) ):
        await message.delete()

        db_constants = db['constants']
        warned_users_obj = db_constants.find_one({'name': 'warnings'})
        warned_users = warned_users_obj['value']

        if message.author.id in warned_users:
            # ban user and delete messages, notify helpers
            banned_name = message.author.name
            await message.author.ban(delete_message_days=7)
            guild = await get_guild(client)
            mods_channel = guild.get_channel(constants.MODS_CHANNEL)
            await safe_send(mods_channel, 'BAN REPORT: User "'+banned_name+'" was banned for sending links twice without Image Permission. Please review the logs and check if this ban was correct. Revoke the ban if the user was not engaging in harmful activity. Message: '+message.content)
            return
        else:
            # add to warnings array
            await safe_send(message.channel, message.author.mention+' '+' Image permission is off by default to keep the server safe! To get perms, just make a ticket and ask for it here: https://discord.com/channels/1130553449491210442/1202441473027477504\n\n**Please be careful, if you send another image or link before getting this permission, the auto-mod will think you are a spam bot and ban you.**')
            warned_users.append(message.author.id)
            db_constants.update_one({"name": 'warnings'}, {"$set": {"value": warned_users}})
            guild = await get_guild(client)
            mods_channel = guild.get_channel(constants.MODS_CHANNEL)
            await safe_send(mods_channel, 'WARN REPORT: User "'+message.author.name+'" was *warned* for sending a link without Image Permission. Please review the logs and check if what they sent was allowed. If it was allowed, please give them image perms immediately to prevent them from being accidentally banned. Message: '+message.content)
            return

    mentioned_bot = message.mentions and message.mentions[0].id == constants.BOT_ID
    if mentioned_bot:
        await savage_scovi(message)
        return

    is_command = len(user_message) > 0 and (user_message[0] == '!')
    if (not is_command) and (not is_push_bot):
        return

    valid_channel, response = is_valid_channel(message, lower_message, is_helper, is_push_bot, is_tourney_admin)

    if not valid_channel:
        await safe_send(message.channel, message.author.mention+" "+response)
        return

    if lower_message == '!help':
        await help_handler(message)

    elif lower_message == '!helpleague':
        await help_league_handler(message)

    elif lower_message == '!helpleagueadmin':
        await help_league_admin_handler(message)

    elif lower_message == '!helpally':
        await help_ally_handler(message)

    elif lower_message == '!helpgems':
        await help_gems_handler(message)

    elif lower_message == '!helpcasino':
        await help_casino_handler(message)

    elif lower_message == '!helpcards':
        await help_cards_handler(message)

    elif lower_message == '!helpbonus':
        await help_bonus_handler(message)

    elif lower_message == '!helpdrops':
        await help_drops_handler(message)

    elif lower_message.startswith('!address'):
        notice = await safe_send(message.channel, message.author.mention+' Please only use this command in a direct message with me for your safety!')
        await message.delete()
        time.sleep(5)
        await notice.delete()

    elif lower_message == '!version' or lower_message == '!v':
        await safe_send(message.channel, constants.VERSION)
    
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

    elif lower_message.startswith("!suggest "):
        await suggest_handler(message, client)

    elif lower_message.startswith('!feature ') and is_admin:
        await feature_handler(message, client)

    elif lower_message == "!tokens":
        await output_tokens(db, message)

    elif lower_message == '!packs':
        await output_packs(db, message)

    elif lower_message == '!cards':
        await cards_handler(db, message)

    elif lower_message == '!gems':
        await gems_handler(db, message)

    elif lower_message.startswith('!donategems '):
        await donate_gems(db, message)

    elif lower_message == '!lootboxes':
        await lootboxes_handler(db, message)

    elif lower_message == '!pickaxes':
        await output_pickaxes(db, message)

    elif lower_message == '!sellpickaxe':
        await sell_pickaxe_for_tokens(db, message)

    elif lower_message == '!dailygift' or lower_message == '!gift':
        await gift_handler(db, message, is_admin)

    elif lower_message == "!hello":
        await hello_handler(message)

    elif lower_message == '!gg ez':
        await gg_ez_handler(message)

    elif lower_message.startswith('!whichhero'):
        await which_hero_handler(message)

    elif lower_message == '!store':
        await safe_send(message.channel, 'Check out the official SOL Merch Store here! https://exclaim.gg/store/spicyow')

    elif lower_message.startswith('!whichteam'):
        await which_team_handler(message)

    elif lower_message.startswith('!wager'):
        await wager_handler(db, message)

    elif lower_message == '!mine':
        await mine_handler(db, message)

    elif lower_message.startswith('!blackjack'):
        await blackjack_handler(db, message, client)

    elif lower_message.startswith('!rps'):
        await rps_handler(db, message)

    elif lower_message.startswith('!buy '):
        await buy_handler(db, message, client)

    elif lower_message.startswith('!donate '):
        await donate_handler(db, message)

    elif lower_message.startswith('!donatepacks '):
        await donate_packs(db, message)

    elif lower_message.startswith('!solojoin'):
        await safe_send(message.channel, 'This command is not currently enabled! Check back later')
        # await solo_join_handler(db, message, client)

    elif lower_message.startswith('!invitedby'):
        await invited_by_handler(db, message)
    
    # pi-pi chan

    elif lower_message == '!leaderboard':
        await safe_send(message.channel, 'This command is turned off for now as XP is not currently turned on. It may be turned on again in the future.')
        #await leaderboard_handler(db, message)

    elif lower_message == '!tokenleaderboard':
        await token_leaderboard_handler(db, message)

    elif lower_message == '!battleleaderboard':
        await battle_leaderboard_handler(db, message)

    elif lower_message == '!bracket':
        await bracket_handler(message)

    elif lower_message.startswith('!profile') or lower_message.startswith('!p ') or lower_message == '!p':
        await profile_handler(db, message, client, context)

    elif lower_message == '!randommap':
        await random_map_handler(message, context)

    elif lower_message == '!standings':
        await standings_handler(message, context)

    elif lower_message == '!fixstandings' and is_admin:
        await fix_standings_handler(db, message, context)

    # elif lower_message == '!standings2':
    #     await standings2_handler(db, message, client)

    elif lower_message == '!solweeklypay' and is_admin:
        await sol_weekly_pay(db, message)

    elif lower_message == '!weeklyrosterreset' and is_admin:
        await weekly_roster_reset(db, message)

    elif lower_message == '!solweekend' and is_admin:
        await sol_week_end(db, message)
        
    elif lower_message == '!schedule':
        await schedule_handler(message, context)

    elif lower_message.startswith('!bid '):
        await bid_handler(db, message, client)

    elif lower_message.startswith('!makevote') and is_admin:
        await make_vote_handler(db, message, client)

    elif lower_message == '!cancelvote' and is_admin:
        await cancel_vote_handler(db, message, client)

    elif lower_message == '!endvote' and is_admin:
        await end_vote_handler(db, message, client)

    elif lower_message.startswith('!vote'):
        await vote_handler(db, message, client)

    elif lower_message == '!subtimer':
        await safe_send(message.channel, 'Twitch Lootboxes are now given instantly when you subscribe or re-subscribe!')
        # await sub_timer_handler(db, message)

    elif lower_message == '!auctiontimer':
        await auction_timer_handler(db, message)

    # LEAGUE COMMANDS

    elif lower_message.startswith('!makeleagueteam') and is_admin:
        # !makeleagueteam [team role id] @Owner [Team Name]
        await make_league_team_handler(db, message, client, context)

    elif lower_message == '!fixmrlineups' and is_admin:
        
        rivals_league_teams = db['rivals_leagueteams']
        all_teams = rivals_league_teams.find()
        for team in all_teams:
            team['lineup'] = {
                'player1': {
                    'role': 'player',
                    'user_id': 0
                },
                'player2': {
                    'role': 'player',
                    'user_id': 0
                },
                'player3': {
                    'role': 'player',
                    'user_id': 0
                },
                'player4': {
                    'role': 'player',
                    'user_id': 0
                },
                'player5': {
                    'role': 'player',
                    'user_id': 0
                },
                'player6': {
                    'role': 'player',
                    'user_id': 0
                },
            }

            rivals_league_teams.update_one({'team_name': team['team_name']}, {'$set': {'lineup': team['lineup']}})

        await safe_send(message.channel, 'All teams have been reset to have no players in their lineup.')

    elif lower_message.startswith('!changeteamowner') and is_tier_3_mod:
        # !changeteamowner @player team name
        await change_team_owner_handler(client, db, message, context)

    elif lower_message.startswith('!changetpp'):
        # !changetpp @Player [new tpp]
        await change_tpp_handler(db, message, client, context)

    elif lower_message.startswith('!changerole'):
        # !changerole @Player [new role]
        await change_role_handler(db, message, client, context)

    elif lower_message.startswith('!kick ') or lower_message.startswith('!leaguekick '):
        # !kick @Player
        await league_kick_handler(db, message, client, context)

    elif lower_message.startswith('!maketeamadmin'):
        # !maketeamadmin @Player
        await make_team_admin_handler(db, message, client, context)

    elif lower_message == '!leagueadminrolefix' and is_admin:

        admin_role_id = 1353487134895378582
        admin_role = await get_role_by_id(client, admin_role_id)

        guild = await get_guild(client)

        league_teams = db['rivals_leagueteams']
        all_teams = league_teams.find()
        for team in all_teams:
            members = team['members']
            for member in members:
                if member['is_admin']:
                    member_id = member['discord_id']
                    member_obj = get_member(guild, member_id, 'league_admin_role_fix')
                    await member_obj.add_roles(admin_role)

        await safe_send(message.channel, 'done')


    elif lower_message.startswith('!removeteamadmin'):
        # !removeteamadmin @Player
        await remove_team_admin_handler(db, message, client, context)

    elif lower_message == '!portal':
        await portal_handler(db, message, context)

    elif lower_message.startswith('!invite ') or lower_message.startswith('!leagueinvite '):
        # !invite @player
        await league_invite_handler(db, message, context)

    elif lower_message.startswith('!cancelinvite '):
        # !cancelinvite @player
        await league_cancel_invite_handler(db, message, context)

    elif lower_message == '!invites' or lower_message == '!leagueinvites':
        await league_invites_handler(db, message, context)

    elif lower_message.startswith('!accept ') or lower_message.startswith('!leagueaccept '):
        await league_accept_handler(db, message, client, context)

    elif lower_message.startswith('!deny ') or lower_message.startswith('!leaguedeny ' ):
        await league_deny_handler(db, message, context)

    elif lower_message == '!leave' or lower_message == '!leagueleave':
        await league_leave_handler(db, message, client, context)

    elif lower_message == '!leaguexp':
        await league_xp_handler(db, message, client)

    elif lower_message == '!leaguexptotal':
        await total_league_xp_handler(db, message, client)

    elif lower_message == '!wipeleaguexp' and is_admin:
        await wipe_league_xp_handler(db, message)

    elif lower_message == '!pingteam':
        await ping_team_handler(db, message, client, context)

    elif lower_message == '!pruneteam':
        await prune_team_handler(db, message, client, context)

    elif lower_message.startswith('!order '):
        await league_order_handler(db, message, client, context)

    elif lower_message.startswith('!allyrequest '):
        await ally_request_handler(db, message, context)

    elif lower_message.startswith('!rivalrequest '):
        await rival_request_handler(db, message, context)

    elif lower_message.startswith('!acceptally '):
        await accept_ally_handler(db, message, client, context)

    elif lower_message.startswith('!acceptrival '):
        await accept_rival_handler(db, message, client, context)

    elif lower_message.startswith('!delally '):
        await del_ally_handler(db, message, client, context)

    elif lower_message.startswith('!delrival '):
        await del_rival_handler(db, message, client, context)

    elif lower_message.startswith('!denyally '):
        await deny_ally_handler(db, message, context)

    elif lower_message.startswith('!denyrival '):
        await deny_rival_handler(db, message, context)

    elif lower_message.startswith('!cancelally '):
        await cancel_ally_handler(db, message, context)

    elif lower_message.startswith('!cancelrival '):
        await cancel_rival_handler(db, message, context)

    elif lower_message == '!allyrequests':
        await ally_requests_handler(db, message, context)

    elif lower_message == '!rivalrequests':
        await rival_requests_handler(db, message, context)

    # elif lower_message.startswith('!setappslink'):
    #     await set_apps_link_handler(db, message, context)

    # elif lower_message.startswith('!setminrank'):
    #     await set_min_rank_handler(db, message, context)

    # elif lower_message == '!toggleapps':
    #     await toggle_apps_handler(db, message, context)

    elif lower_message == '!setlineup':
        await set_lineup_handler(db, message, context)

    elif lower_message.startswith('!timeslot '):
        await timeslot_handler(db, message, client, context)

    elif lower_message == '!unschedule':
        await unschedule_handler(db, message, client, context)

    elif lower_message == '!firstmap':
        await first_map_handler(db, message, context)

    elif lower_message.startswith('!callme '):
        await call_me_handler(db, message, context)

    elif lower_message.startswith('!rolename '):
        await role_name(client, db, message)

    elif lower_message.startswith('!rolecolor '):
        await role_color(client, db, message)

    elif lower_message.startswith('!teampage'):
        await team_page_handler(db, message, context)

    elif lower_message == '!website':
        await website_handler(message)

    elif lower_message == '!cardsearch':
        await card_search_handler(message)

    elif lower_message == '!top100':
        await top_100_handler(message)

    elif lower_message.startswith('!matchlineups') and is_tourney_admin:
        await match_lineups_handler(db, message, context)

    elif lower_message == '!make50codes' and is_admin:
        await make_50_codes_handler(db, message, 1)

    elif lower_message == '!make50codes10' and is_admin:
        await make_50_codes_handler(db, message, 10)

    elif lower_message == '!make50codes25' and is_admin:
        await make_50_codes_handler(db, message, 25)

    elif lower_message == '!make50codes50' and is_admin:
        await make_50_codes_handler(db, message, 50)
    
    elif lower_message == '!make50codes100' and is_admin:
        await make_50_codes_handler(db, message, 100)

    elif lower_message.startswith('!redeem '):
        await redeem_code(db, message)

    elif lower_message == '!resetteamrules' and is_admin:

        users = db['users']
        all_users = users.find()

        for user in all_users:

            changes_made = False
            set_array = {}

            if 'team_swaps' in user:
                changes_made = True
                set_array['team_swaps'] = 3

            if 'user_div' in user:
                changes_made = True
                set_array['user_div'] = 0

            if changes_made:
                users.update_one({'discord_id': user['discord_id']}, {'$set': set_array})

    elif lower_message.startswith('!setleagueteam ') and is_admin:
        # !setleagueteam [user_id] [team name]
        await set_league_team_handler(db, message)

    elif lower_message.startswith('!forcedelleagueteam ') and is_admin:
        await force_delete_league_team_handler(db, message)

    elif lower_message.startswith('!updateteam ') and is_admin:
        await update_team_handler(db, message, client, context)

    elif lower_message.startswith('!giveteamtokens ') and is_admin:
        await give_team_tokens_handler(db, message)

    elif lower_message.startswith('!fanof'):
        await fan_of_handler(db, message, context)

    elif lower_message.startswith('!rivalof'):
        await rival_of_handler(db, message, context)

    elif lower_message.startswith('!bandforband '):
        await band_for_band_handler(db, message)


    # ADMIN COMMANDS

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
        await wipe_bracket_handler(db, message)

    elif lower_message.startswith("!switchmatches ") and is_admin:
        # !switchmatches [event id] [switch match id 1] [switch match id 2]
        await switch_matches_handler(db, message)

    elif lower_message.startswith("!gentourney ") and is_admin:
        # !gentourney [event id]
        await gen_tourney_handler(db, message)

    elif lower_message == '!wipetourney' and is_admin:

        await wipe_tourney(db, message)

    elif lower_message == '!starttourney' and is_tourney_admin:

        guild = client.get_guild(constants.GUILD_ID)

        await send_next_info(db, message, guild, client)
        await notify_next_users(db, guild, message)


    elif lower_message.startswith('!endbattle') and is_admin:
        await end_battle_handler(db, message, context)

    elif lower_message == '!startbattle' and is_admin:
        await start_battle_handler(db, message, client, context)

    elif lower_message == '!hm' and is_admin:
        await how_many_handler(db, message, context)

    elif lower_message.startswith('!bns') and is_admin:
        await battle_no_show_handler(db, message, client, context)

    elif lower_message == '!endreg' and is_admin:
        await end_reg_handler(db, message, client, context)

    elif lower_message == '!battleteams' and is_admin:
        await battle_teams_handler(db, message, client, context)

    elif lower_message.startswith('!battlewin') and is_admin:
        await battle_win_handler(db, message, client, context)


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
        await safe_send(message.channel, 'test data set')

    elif lower_message == '!testsafesend' and is_admin:
        await safe_send_test(message)

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

    elif lower_message.startswith('!forceaddteam') and is_admin:
        await force_add_team_handler(db, message, client)

    elif lower_message.startswith('!forceremoveteam') and is_admin:
        await force_remove_team_handler(db, message, client)

    elif lower_message.startswith('!forceremoveplayer') and is_admin:
        await force_remove_player_handler(db, message)

    elif lower_message.startswith('!forceleagueremove') and is_admin:
        await force_league_remove_handler(db, message, client)

    elif lower_message.startswith('!forceleagueadd') and is_tier_3_mod:
        await force_league_add_handler(db, message, client, context)

    elif lower_message.startswith('!wipeteam ') and is_admin:
        await wipe_team(db, message, client, context)

    elif lower_message.startswith('!subpoints ') and is_admin:
        await sub_points_handler(db, message, client)

    elif lower_message.startswith('!funding') and is_admin:
        await funding_handler(db, message, client)

    elif lower_message.startswith('!slowmode ') and is_tier_3_mod:
        await slowmode_handler(message)

    elif lower_message.startswith('!free ') and is_tier_3_mod:
        await free_handler(message)

    elif lower_message.startswith('!testcardmatch') and is_admin:
        
        player1_card_ids = ['12-S', '20-S', '154-S', '194-S', '222-S']
        player2_card_ids = ['367-S', '455-S', '789-S', '800-S', '807-S']

        role_array = ['tank', 'dps1', 'dps2', 'sup1', 'sup2']

        single_cards_collection = db['single_cards']
        display_cards_collection = db['display_cards']        

        role_index = 0
        player_1_cards = []
        for card_id in player1_card_ids:
            player1_card_ids.append(make_match_card(single_cards_collection, display_cards_collection, card_id, role_array[role_index]))
            role_index += 1

        role_index = 0
        player_2_cards = []
        for card_id in player2_card_ids:
            player2_card_ids.append(make_match_card(single_cards_collection, display_cards_collection, card_id, role_array[role_index]))
            role_index += 1

        test_match_obj = {
            'match_id': 'ioghjriog58709654980',
            'player1_id': 1112204092723441724,
            'player2_id': 340644170656120833,
            'player1_cards': player_1_cards,
            'player2_cards': player_2_cards,
            'player_turn': 1
        }

        db['card_matches'].insert_one(test_match_obj)

    elif lower_message.startswith('!twitch10') and is_cp_helper:
        await twitch_tokens_handler(client, db, message, 10)

    elif lower_message.startswith('!twitch50') and is_cp_helper:
        await twitch_tokens_handler(client, db, message, 50)

    elif lower_message.startswith('!twitchpack') and is_cp_helper:
        await twitch_pack_handler(client, db, message)

    elif lower_message == '!fortnite':
        await safe_send(message.channel, 'fortnite')

    elif lower_message == '!sigma':
        await safe_send(message.channel, 'https://i.imgur.com/2qptwSa.png')

    elif lower_message == '!buzzcut':
        await safe_send(message.channel, 'https://i.imgur.com/RpTj77v.png')

    elif lower_message == '!howdy':
        await safe_send(message.channel, 'https://tenor.com/view/good-morning-summer-mickey-mouse-gif-13892611')

    elif lower_message == '!thepoint':
        await safe_send(message.channel, 'https://i.imgur.com/mwekfl2.png')

    elif lower_message.startswith('!slime '):
        await slime_handler(db, message)

    elif lower_message.startswith('!revive '):
        await revive_handler(db, message)

    elif lower_message == '!zorp':

        test_zorp = ['zorp?', 'bogos binted', 'pickenteen zumflood', 'porijug riwedor', 'zeriup zort', 'zorty zort', 'bering bering zrop', 'mrop mrop vorp', 'vropy vorp', 
                     'fortzorp', 'HELP ME IM TRAPPED HELP ME PLEASE HELP ME PLEASE IM NOT A DISCORD BOT HELP PLEASE HELP PLEASE', 'figeldeen zorpenstein']

        await safe_send(message.channel, random.choice(test_zorp))

    elif lower_message == '!testdm' and is_admin:

        guild = await get_guild(client)
        default_msg = "Welcome to the Spicy Esports Discord Server! I'm *Scovi*, the server's helper bot. "
        default_msg += f"\n\nIf you're interested in joining a **League Team**, you can see which teams have applications open here: {constants.WEBSITE_DOMAIN}/sol/apply"
        default_msg += '\n\nYou can also find more information about our League here: https://discord.com/channels/1130553449491210442/1178427939453411469'
        default_msg += '\n\nThank you for joining! If you have any questions, feel free to ask here: https://discord.com/channels/1130553449491210442/1166410753184632933'

        await safe_send(message.channel, default_msg)

    elif lower_message.startswith('!8ball'):
        await eight_ball_handler(message)

    elif lower_message.startswith('!thisgif'):
        await safe_send(message.channel, 'https://i.imgur.com/J2jCzIb.png')

    elif lower_message.startswith('!feedgem '):
        await feed_gem(db, message)

    elif lower_message == '!wipecarddatabase' and is_admin:
        await wipe_card_database_handler(db, message)

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

    elif lower_message == '!sellallcards':
        await sell_all_cards_handler(db, message)

    elif lower_message.startswith('!givecard '):
        await give_card_handler(db, message)

    elif lower_message.startswith('!listcard '):
        await list_card_handler(db, message)

    elif lower_message.startswith('!unlistcard '):
        await unlist_card_handler(db, message)

    elif lower_message.startswith('!buycard '):
        await buy_card_handler(db, message)

    elif lower_message.startswith('!releasecards ') and is_admin:
        await release_cards(db, message)

    elif lower_message.startswith('!forceunlist ') and is_admin:
        await force_unlist(db, message)

    elif lower_message.startswith('!cardbattle '):
        # !cardbattle [card id] [battle type] [min power] [max power]
        await card_battle(client, db, message)

    elif lower_message.startswith('!fightcard '):
        # !fightcard [other card id] [my card id]
        await fight_card(client, db, message)

    elif lower_message == '!makeallcardsfromdata' and is_admin:
        return
        #await make_all_cards_from_data(db, message, client)

    elif lower_message == '!makeallcardsfromdb' and is_admin:
        await make_all_cards_from_db(db, message)

    elif lower_message.startswith('!makecard') and is_admin:
        await make_card_handler(db, message)

    elif lower_message.startswith('!editcard ') and is_admin:
        await edit_card_handler(db, message)

    elif lower_message.startswith('!registerrole') and is_admin:
        await register_role(db, message)

    # elif lower_message == '!gallery':
    #     await safe_send(message.channel, f'Check out the full SOL Card Gallery here: {constants.WEBSITE_DOMAIN}/sol/gallery')

    elif lower_message == '!openpack':
        await open_pack_handler(db, message)

    elif lower_message == '!totalcards':
        await total_cards_handler(db, message, context)

    elif lower_message == '!totalpacks':
        await total_packs_handler(db, message)

    elif lower_message == '!cardmarket':
        await safe_send(message.channel, f'Check out the SOL Card Market here!\n\n{constants.WEBSITE_DOMAIN}/sol/card-market')

    elif lower_message == '!allcards':
        await safe_send(message.channel, f'View all your cards here: {constants.WEBSITE_DOMAIN}/sol/user-cards/'+str(message.author.id))

    elif lower_message.startswith('!cardpage '):
        await card_page(db, message)

    elif lower_message == '!resetraffle' and is_admin:
        db_constants = db['constants']
        db_constants.update_one({"name": 'raffle_total'}, {"$set": {"value": 0}})

        users = db['users']
        all_users = users.find()

        for user in all_users:
            if 'tickets' in user:
                users.update_one({"discord_id": user['discord_id']}, {"$set": {"tickets": 0}})

        await safe_send(message.channel, 'Raffle reset')


    elif lower_message.startswith('!win ') and is_tourney_admin:

        # !win [winner 1 or 2]
        word_list = message.content.split()
        if len(word_list) == 2:
            guild = client.get_guild(constants.GUILD_ID)
            await won_match(int(word_list[1]), message, db, guild, client)
        else:
            await safe_send(message.channel, "Invalid number of arguments.")

    elif lower_message.startswith('!noshow ') and is_tourney_admin:

        # !noshow [loser 1 or 2]
        word_list = message.content.split()
        if len(word_list) == 2:
            guild = client.get_guild(constants.GUILD_ID)
            await no_show(int(word_list[1]), message, db, guild, client)
        else:
            await safe_send(message.channel, "Invalid number of arguments.")

    elif lower_message == '!bothnoshow' and is_tourney_admin:

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

        await safe_send(message.channel, 'The winner of the raffle is the user with the battle tag: '+lucky_winner)

    elif lower_message == '!initstandings' and is_admin:
        await init_standings(db, message)

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
        await safe_send(message.channel, 'auction data initated')

    elif lower_message == '!testgetconstant' and is_admin:
        constant_val = get_constant_value(db, 'test_constant')
        await safe_send(message.channel, 'test constant is: '+constant_val)

    elif lower_message == '!testsetconstant' and is_admin:
        set_constant_value(db, 'test_constant', 'nuts')
        await safe_send(message.channel, 'set test constant')

    elif lower_message.startswith('!addwin') and is_admin:
        await add_win_handler(db, message)

    elif lower_message.startswith('!addloss') and is_admin:
        await add_loss_handler(db, message)


    elif lower_message.startswith('!mapdiff') and is_admin:
        await map_diff_handler(db, message)

    # !matchend winTeam winScore loseTeam loseScore
    elif lower_message.startswith('!matchend') and is_admin:
        await match_end_handler(db, message, client)

    elif lower_message.startswith('!scorematch ') and is_admin:
        await score_match_handler(client, db, message, context)

    elif lower_message.startswith('!ffmatch ') and is_admin:
        await ff_match_handler(db, message, context)

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
        await safe_send(message.channel, 'maps initated')

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

    elif lower_message == '!nextweek' and is_admin:
        await next_week_handler(db, message)

    elif lower_message.startswith('!makesolweek') and is_admin:
        await make_sol_week(db, message)

    elif lower_message.startswith('!bumpsolweek') and is_admin:
        await bump_sol_week(db, message)

    elif lower_message == '!makematchups' and is_admin:
        
        matchups = db['matchups']

        TEST_MATCHUPS = [
            ['Angels', 'Celestials'],
            ['Deadlock', 'Diamonds'],
            ['Eclipse', 'Evergreen'],
            ['Fresas', 'Guardians'],
            ['Horizon', 'Hunters'],
            ['Instigators', 'Legion'],
            ['Lotus', 'Misfits'],
            ['Monarchs', 'Olympians'],
            ['Outliers', 'Phantoms'],
            ['Phoenix', 'Polar'],
            ['Ragu', 'Saturn'],
            ['Saviors', 'Sentinels'],
            ['Aces', 'Mantas']
        ]

        for matchup in TEST_MATCHUPS:
            new_matchup = {
                'matchup_id': str(uuid.uuid4()),
                'context': 'OW',
                'season': 1,
                'week': 1,
                'team1': matchup[0],
                'team2': matchup[1],
                'team1_timeslot': 'NONE',
                'team2_timeslot': 'NONE',
                'timeslot': 'NONE',
                'weekday': 'NONE',
                'team1_score': 0,
                'team2_score': 0,
                'match_over': False,
                'added_to_schedule': False
            }
            matchups.insert_one(new_matchup)

        await safe_send(message.channel, 'Test matchups made')

    elif lower_message == '!testmakechannel' and is_admin:

        overwrites = {}

        test_user_id = 1149447725276995686

        guild = await get_guild(client)

        overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=False)

        test_member = guild.get_member(test_user_id)
        overwrites[test_member] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        await guild.create_text_channel('test-channel-casting', overwrites=overwrites)

        await safe_send(message.channel, 'done')

    elif lower_message.startswith('!swissmatchups') and is_admin:
        await swiss_matchups_handler(db, message, context)

    elif lower_message.startswith('!makesolmatch') and is_admin:
        await make_sol_match(client, db, message)

    elif lower_message == '!picks':
        await picks_handler(db, message)

    elif lower_message.startswith('!prunepicks ') and is_admin:
        await prune_picks(db, message)

    elif lower_message.startswith('!scorepicks') and is_admin:
        await score_picks(db, message)
        
    elif (lower_message.startswith('!givetokens ') or lower_message.startswith('!gt ')) and is_admin:

        # !givetokens [winner id] [tokens]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_tokens_command(client, db, word_list[1], int(word_list[2]), message)
        else:
            await safe_send(message.channel, "Invalid number of arguments.")

    elif lower_message.startswith('!givemoney ') and is_admin:
        await give_money(client, db, message)

    elif lower_message == '!money':
        await money(db, message)

    elif lower_message.startswith('!givexp ') and (is_admin or is_xp_helper):
        await safe_send(message.channel, 'This command is currently disabled. XP is turned off for now.')
        #await give_xp_handler(client, db, message)

    elif lower_message.startswith('!rp') and is_admin:
        await rp_handler(client, db, message)

    elif lower_message.startswith('!setlevel ') and is_admin:
        await set_level_handler(client, db, message)

    elif lower_message.startswith('!givepickaxes ') and is_admin:

        # !givepickaxes [winner id] [pickaxes]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_pickaxes_command(client, db, word_list[1], int(word_list[2]), message)
        else:
            await safe_send(message.channel, 'Invalid number of arguments.')

    elif lower_message.startswith('!givepacks ') and (is_admin or is_tp_helper):

        # !givepacks [winner id] [packs]
        word_list = message.content.split()
        if len(word_list) == 3:
            await give_packs_command(client, db, word_list[1], float(word_list[2]), message)
        else:
            await safe_send(message.channel, 'Invalid number of arguments.')

    elif lower_message.startswith('!gp') and (is_admin or is_tp_helper):
        await gp_handler(db, message)

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

        await safe_send(message.channel, 'boxes given')

    elif lower_message == '!givesubboxes' and is_admin:
        await give_sub_boxes_handler(db, message, client)

    elif lower_message.startswith('!open '):
        await open_handler(db, message)

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

    elif lower_message.startswith('!getdetails '):
        # !getdetails [username]
        await get_details_handler(db, message, client, is_admin)
    elif lower_message == '!wipeteams' and is_admin:
        await wipe_teams_handler(db, message)
    elif lower_message == '!totaltokens' and is_admin:
        await total_tokens_handler(db, message)
    elif lower_message == '!resettokentracker' and is_admin:
        await reset_token_tracker_handler(db, message)
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
        await safe_send(chat_channel, rest)

    elif lower_message.startswith('!deletebytag ') and is_admin:
        await delete_by_tag_handler(db, message)

    elif lower_message.startswith('!postreplay ') and is_admin:
        vod_link = message.content.split()[1]
        guild = await get_guild(client)
        clips_channel = guild.get_channel(constants.CLIPS_CHANNEL)
        await safe_send(clips_channel, 'A new SOL Replay has been posted! Go check it out! '+vod_link)

    elif lower_message.startswith('!setdesc ') and is_admin:
        await set_desc_handler(db, message)

    elif lower_message.startswith('!swapsides') and is_tourney_admin:
        await swap_sides(db, message, context)

    elif lower_message.startswith('!addpoint') and is_tourney_admin:
        await add_point(db, message, context)

    elif lower_message.startswith('!removepoint') and is_tourney_admin:
        await remove_point(db, message, context)

    elif lower_message.startswith('!ban') and is_tourney_admin:
        await ban_hero_handler(db, message, context)

    elif lower_message.startswith('!firstpick') and is_tourney_admin:
        await first_pick_handler(db, message, context)

    elif lower_message.startswith('!tname') and is_admin:
        await set_tourney_team_name(db, message)

    elif lower_message.startswith('!tscore') and is_admin:
        await set_tourney_team_score(db, message)

    elif lower_message.startswith('!tcolor') and is_admin:
        await set_tourney_team_color(db, message)

    elif lower_message == '!tswap' and is_admin:
        await swap_tourney_teams(db, message)

    elif lower_message.startswith('!startpred ') and is_tourney_admin:
        await start_pred(db, message)

    elif lower_message.startswith('!endpred ') and is_tourney_admin:
        await end_pred(db, message)

    elif lower_message == '!admain' and is_tourney_admin:
        await run_ad(db, message, 'main')

    elif lower_message == '!adsecond' and is_tourney_admin:
        await run_ad(db, message, 'second')

    elif lower_message == '!adthird' and is_tourney_admin:
        await run_ad(db, message, 'third')

    elif lower_message == '!raidmain' and is_tourney_admin:
        await raid_channel(db, message, 'second', 'main')

    elif lower_message == '!raidsecond' and is_tourney_admin:
        await raid_channel(db, message, 'main', 'second')

    elif lower_message.startswith('!raid') and is_tourney_admin:
        await raid_handler(db, message)

    elif lower_message.startswith('!lockon') and is_admin:
        await handle_lock(db, message, True, context)

    elif lower_message.startswith('!lockoff') and is_admin:
        await handle_lock(db, message, False, context)

    elif lower_message.startswith('!wipepastteams') and is_admin:
        await wipe_past_teams(db, message, context)

    elif lower_message.startswith('!nextdrop'):
        await next_drop(db, message)

    elif lower_message == '!drops':
        await drops(db, message)

    elif lower_message == '!opendrop':
        await open_drop(db, client, message)

    elif lower_message.startswith('!dropalert ') and is_admin:
        await drop_alert(client, db, message)

    elif lower_message.startswith('!makescheduleplan ') and is_admin:
        # !makescheduleplan seasonNumber startDay startMonth startYear numWeeks teamBlacklist
        await make_schedule_plan(message, db, context)

    elif lower_message == '!addweek' and is_admin:
        await add_week(db, message, context)

    elif lower_message.startswith('!update|') and is_admin:
        parts = message.content.split('|')
        if len(parts) != 3:
            await safe_send(message.channel, "Needs 3 parts. Command, op code, and message.")
            return
        op_code = parts[1]
        main_part = parts[2]
        guild = await get_guild(client)
        update_channel = guild.get_channel(constants.UPDATE_CHANNEL)
        if op_code.lower() == 'd':
            update_msg = await safe_send(update_channel, '**[Scovi Version '+constants.VERSION+']**\n'+main_part)
        elif op_code.lower() == 'w':
            update_msg = await safe_send(update_channel, '**[Spicy Esports Website Update]**\n'+main_part)
        elif op_code.lower() == 'u':
            update_msg = await safe_send(update_channel, '**[Discord Update]**\n'+main_part)

        await update_msg.add_reaction("👍")

        await safe_send(message.channel, 'Update posted')

    elif lower_message == '!giveeveryonerole' and is_admin:

        guild = client.get_guild(constants.GUILD_ID)
        overwatch_role = guild.get_role(constants.OVERWATCH_ROLE)

        num = 1
        for member in client.get_all_members():
            
            await member.add_roles(overwatch_role)
            time.sleep(0.5)
            print('applied to user '+str(num))
            num += 1

    elif lower_message == '!getavatar':
        avatar = message.author.display_avatar
        if avatar:
            avatar_link = avatar.url
            await safe_send(message.channel, '('+avatar_link+')')
        else:
            await safe_send(message.channel, 'Problem getting avatar')

    elif lower_message == '!testerror' and is_admin:

        test = {
            'test': 1
        }
        test2 = test['test2']


    elif lower_message == '!coinstats':
        await coin_stats(db, message)

    elif lower_message == '!coinprice':
        await coin_price(db, message)

    elif lower_message == '!redeemtrophies':
        await redeem_trophies(db, message)

    elif lower_message.startswith('!givevouchers ') and is_admin:
        await give_vouchers(client, db, message)

    elif lower_message.startswith('!takevouchers ') and is_admin:
        await take_vouchers(client, db, message)

    elif lower_message.startswith('!donatevouchers '):
        await donate_vouchers(db, message, context)

    elif lower_message == '!forcescheduleloop' and is_admin:

        await schedule_plan_loop(db, message, client)

    elif lower_message == '!getpfplink':

        await safe_send(message.channel, message.author.avatar.url)

    elif lower_message.startswith('!makecaster ') and is_admin:
        await make_caster_handler(db, message)

    elif lower_message.startswith('!deletecaster ') and is_admin:
        await delete_caster_handler(db, message)

    elif lower_message.startswith('!pay ') and is_admin:
        await pay_handler(db, message)

    elif lower_message.startswith('!bal ') and is_admin:
        await bal_handler(db, message)

    elif lower_message == '!dropbank' and is_admin:
        await drop_bank_handler(db, message)

    elif lower_message.startswith('!dropbankadd ') and is_admin:
        await drop_bank_add_handler(db, message)

    elif lower_message.startswith('!makelobbyadmin ') and is_admin:
        await make_lobby_admin_handler(db, message)

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

            message = await safe_send(channel, 'Add an emoji reaction to get the '+discord_role.mention+ ' role. Remove the reaction to remove it. Default is **OFF**.\n*'+role['extra']+'*', True)
            await message.add_reaction("✅")

    elif lower_message == 'check long' and is_push_bot:
        bot_channel = client.get_channel(constants.BOT_CHAT_CHANNEL)
        await safe_send(bot_channel, 'Updating Bets')
        # await give_sub_boxes_handler(db, message, client)
        await update_bets(db, message.channel, client)

    elif lower_message == 'check gifts' and is_push_bot:

        bot_channel = client.get_channel(constants.BOT_CHAT_CHANNEL)
        await safe_send(bot_channel, 'Checking gifts')
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

        await safe_send(message.channel, str(users_notified)+' users notified of having a gift')

        await safe_send(message.channel, 'Checking payroll')

        await check_payroll(db, message.channel)

        await check_auction(db, message.channel, client)

        await check_weekly(client, db, message.channel, message)

        await check_token_issue(db, message.channel)

        await check_streamlabs_raffles(db, message.channel)

        await check_lineup_tokens(db, message)

        await check_open_bets(db, message)

        # await check_notify_about_matches(client, db, message)

        await update_top_subs_avatars(guild, db, message)

        await update_overwatch_team_avatars(guild, db, message)
        await update_rivals_team_avatars(guild, db, message)
        await update_valorant_team_avatars(guild, db, message)

        await supporter_role_loop(db, message, client)

        await clear_expired_battles(client, db, message)

        await process_trophy_rewards(db, message)

        await schedule_plan_loop(db, message, client)

    elif context == 'MR':
        await route_rivals_message(db, message, lower_message)

    elif context == 'VL':
        await route_valorant_message(client, db, message, lower_message)

    else:
        await safe_send(message.channel, 'Invalid command. Please see **!help** for a list of commands.')


def run_discord_bot(db, is_smoke_test=False):

    if is_smoke_test:
        return 'Started bot.py without errors'

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
            battle_context = get_constant_value(db, 'battle_context')
            battle_constant_name = get_battle_constant_name(battle_context)
            battle_obj = constants_db.find_one({'name': battle_constant_name})
            battle_info = battle_obj['value']
            if message_id == battle_info['reg_message_id']:
                await add_to_battle(db, member, battle_info, client, battle_context)
            
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
        elif message_id == constants.LEAGUE_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.LEAGUE_NOTIFS_ROLE)
            await remove_role(member, role, 'Raw Reaction Add')
        elif message_id == constants.GIFT_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.GIFT_ROLE_ID)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id == constants.TOKEN_SHOP_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.TOKEN_NOTIF_ROLE_ID)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.SUB_VOTE_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.SUB_VOTE_ROLE_ID)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.QUEST_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.QUEST_NOTIF_ROLE_ID)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.SOL_TODAY_NOTIF_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.SOL_TODAY_NOTIF_ROLE_ID)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.OVERWATCH_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.OVERWATCH_ROLE)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.MARVEL_RIVALS_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.MARVEL_RIVALS_ROLE)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.VALORANT_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.VALORANT_ROLE)
            await give_role(member, role, 'Raw Reaction Add')
        elif message_id ==  constants.DBD_MSG:
            guild = await get_guild(client)
            role = guild.get_role(constants.DBD_ROLE)
            await give_role(member, role, 'Raw Reaction Add')

        elif channel_id == constants.STATE_CUP_CHANNEL:
            if not (member_has_state_role(member)):
                for state_name in constants.STATE_INFO:
                    state_info = constants.STATE_INFO[state_name]
                    if state_info['react_msg'] == message_id:
                        guild = await get_guild(client)
                        state_role = guild.get_role(state_info['role'])
                        await give_role(member, state_role, 'Reaction Roles')
                        break

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
            battle_context = get_constant_value(db, 'battle_context')
            battle_constant_name = get_battle_constant_name(battle_context)
            battle_obj = constants_db.find_one({'name': battle_constant_name})
            battle_info = battle_obj['value']
            if message_id == battle_info['reg_message_id']:
                await remove_from_battle(db, member, battle_info, battle_constant_name)
            
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
        elif message_id ==  constants.LEAGUE_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.LEAGUE_NOTIFS_ROLE)
            await give_role(member, role, 'Notifs Settings')
        elif message_id ==  constants.GIFT_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.GIFT_ROLE_ID)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id ==  constants.TOKEN_SHOP_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.TOKEN_NOTIF_ROLE_ID)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id ==  constants.SUB_VOTE_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.SUB_VOTE_ROLE_ID)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id == constants.QUEST_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.QUEST_NOTIF_ROLE_ID)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id == constants.SOL_TODAY_NOTIF_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.SOL_TODAY_NOTIF_ROLE_ID)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id == constants.MARVEL_RIVALS_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.MARVEL_RIVALS_ROLE)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id == constants.OVERWATCH_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.OVERWATCH_ROLE)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id == constants.VALORANT_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.VALORANT_ROLE)
            await remove_role(member, role, 'Notifs Settings')
        elif message_id == constants.DBD_MSG:
            member = get_member(guild, user_id, 'Raw Reaction Remove')
            role = guild.get_role(constants.DBD_ROLE)
            await remove_role(member, role, 'Notifs Settings')

    @client.event
    async def on_member_join(member):
        await member_joined(member, db, client)

    @client.event
    async def on_raw_member_remove(payload):
        await member_left(payload, db, client)


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        try:
            await check_random_event_on_message(db, client)
            await handle_message(message, db, client)
        except CommandError as e:
            await safe_reply(message, str(e))
        except aiohttp.client_exceptions.ClientOSError as e:
            if e.errno == 104:
                await safe_send(message.channel, 'Network error. Please try your command again.')
        except discord.errors.NotFound as e:
            await safe_send(message.channel, 'ERROR: I tried to delete a message but it was already deleted.\n'+str(e))
        except discord.errors.HTTPException as e:
            print('HTTP Exception')
            print(e)
            await safe_send(message.channel, "I'm overloaded at the moment and was not able to properly process this request.")
        except Exception as e:
            print(e)
            traceback.print_exc()
            guild = client.get_guild(constants.GUILD_ID)
            spicy_member = get_member(guild, constants.SPICY_RAGU_ID, 'Error Notify') 
            await safe_send(message.channel, 'Whoops... An error occured. Let me notify staff. '+spicy_member.mention)
            err_channel = guild.get_channel(constants.ERROR_LOGS_CHANNEL)
            traceback_str = traceback.format_exc()
            await safe_send(err_channel, traceback_str)


    print('about to run client')
    client.run(constants.DISCORD_TOKEN)
    print('client ran')