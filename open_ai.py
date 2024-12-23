import openai

from openai import OpenAI
client = OpenAI(api_key="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")

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