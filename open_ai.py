import openai
from openai import OpenAI
from constants import OPEN_AI_TOKEN

client = OpenAI(api_key=OPEN_AI_TOKEN)

ZEN_CONTEXT = ''
with open('zen_ai_context.txt', 'r') as file:
    ZEN_CONTEXT = file.read()


def get_completion(character, prompt):

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": character},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(completion.choices[0].message)
    return completion.choices[0].message.content


def ask_zen(user_input):

    character_context = ZEN_CONTEXT

    zen_response = get_completion(character_context, user_input)
    return zen_response