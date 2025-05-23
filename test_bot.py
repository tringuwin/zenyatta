

from bot import run_discord_bot


def test_bot_smoke_test():

    fake_db = None
    is_smoke_test = True
    
    assert run_discord_bot(fake_db, is_smoke_test) == 'Started bot.py without errors'