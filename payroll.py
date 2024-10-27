

from rewards import change_tokens
from user import user_exists
import time

SECONDS_IN_A_WEEK = 604800

async def check_payroll(db, channel):

    constants = db['constants']

    last_payroll = constants.find_one({'name': 'last_payroll'})
    last_val = last_payroll['value']
    cur_time = time.time()
    over_a_week = (cur_time - last_val) > SECONDS_IN_A_WEEK
    if not over_a_week:
        await channel.send('Not been over a week for payroll')
        return
    await channel.send('Been over a week, pay time')
    constants.update_one({"name": 'last_payroll'}, {"$set": {"value": cur_time}})

    payroll_constant = constants.find_one({'name': 'payroll'})
    pay_users = payroll_constant['value']

    for pay_user in pay_users:

        if pay_user['stopped']:
            await channel.send('Payments paused for '+pay_user['displayName'])
            continue

        user = user_exists(db, pay_user['discord_id'])
        if not user:
            continue

        await change_tokens(db, user, pay_user['salary'], 'staff-salary')
        await channel.send('Paid user '+pay_user['displayName']+' '+str(pay_user['salary'])+' Tokens for the role '+str(pay_user['role']))
