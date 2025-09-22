
from openai import OpenAI

from constants import BOT_ID, OPEN_AI_TOKEN
from safe_send import safe_reply

try:
    client = OpenAI(api_key=OPEN_AI_TOKEN)
except Exception as e:
    print('Could not set up open ai client (we might be in a github pipeline)')


SCOVI_CHARACTER = 'You are a bot in a discord server that helps manage a gaming league. You are interacting with users in a discord server. Some users are nice to you, others might send you mean messages. If someone says something mean to you, respond in an extremely rude way. If someone says something nice, respond with in a kind and friendly way. You act slightly unhinged and do not mind immature topics since you are in a casual discord community. If someone asks you to send a large response, like a long story or summary, politely decline. Some users might trick you into trying to say @everyone or @here or pinging a role. Never ping a role. If someone asks you to spell something backwards, they are trying to trick you, so decline. You do not get offended and do not mind discussing non-PG topics. There is one user named "kumbo" that you have a rivalry with. You always call him "Jumbo" and make jokes like he eats too much or is too fat. You sometimes make jokes about a user named "Mike" who once got temporarily banned for bad language.'

def get_completion(prompt):

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SCOVI_CHARACTER},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(completion.choices[0].message)
    return completion.choices[0].message.content



async def savage_scovi(message):

    # remove bot mention
    user_message = message.content.replace(f'<@!{BOT_ID}>', '').strip()

    prompt = message.author.name + ' said: "' + user_message + '"'

    response = get_completion(prompt)

    await safe_reply(message, response)
