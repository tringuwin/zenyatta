

from rewards import change_tokens
from user import user_exists


async def check_payroll(db, channel):

    pay_users = db['payroll'].find()
    pay_users = list(pay_users)

    for pay_user in pay_users:

        user = user_exists(db, pay_user['discord_id'])
        if not user:
            continue

        await change_tokens(db, user, user['salary'])
        await channel.send('Paid user '+user['displayName']+' '+str(user['salary'])+' Tokens for the role '+str(user['role']))
