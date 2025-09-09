
import uuid
from common_messages import not_registered_response
from exceptions import CommandError
from safe_send import safe_dm, safe_send
from user.user import user_exists
import constants



def verify_portal_for_ow(context):

    if context != 'OW':
        raise CommandError('Right now the league portal is only available for the Overwatch League.')


def create_portal_token(db, user):

    new_portal_token = str(uuid.uuid4())

    users = db['users']
    users.update_one(
        {'_id': user['_id']},
        {'$set': {'portal_token': new_portal_token}}
    )

    return new_portal_token


def get_portal_token_for_user(db, user):

    if 'portal_token' in user:
        return user['portal_token']
    
    new_portal_token = create_portal_token(db, user)
    return new_portal_token


def fetch_portal_url_for_user(db, user):

    portal_token = get_portal_token_for_user(db, user)

    return constants.WEBSITE_DOMAIN+'/portal/'+portal_token
    
    
async def portal_handler(db, message, context):

    verify_portal_for_ow(context)

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    portal_url = fetch_portal_url_for_user(db, user)

    try:
        await safe_dm(message.author, f"Here is your portal link: {portal_url}\n"
            f"Please note that this link is unique to you and should not be shared with anyone else."
        )
        await safe_send(message.channel, 'I sent you a DM with your portal link. Please check your DMs.')

    except Exception as e:
        raise CommandError('I tried to send you a DM, but I was unable to due to your privacy settings. Please check your DM settings and try again.')

