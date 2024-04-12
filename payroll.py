

from rewards import change_tokens
from user import user_exists


async def check_payroll(db, channel):

    constants = db['constants']
    payroll_constant = constants.find({'name': 'payroll'})
    pay_users = payroll_constant['value']

    for pay_user in pay_users:

        user = user_exists(db, pay_user['discord_id'])
        if not user:
            continue

        await change_tokens(db, user, user['salary'])
        await channel.send('Paid user '+user['displayName']+' '+str(user['salary'])+' Tokens for the role '+str(user['role']))
