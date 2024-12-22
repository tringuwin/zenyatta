print('start import')
import openai
import constants

from openai import OpenAI
client = OpenAI(api_key=constants.OPEN_AI_TOKEN)


def get_completion():

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    )

    print(completion.choices[0].message)




def wizard_test():
    # character_context = "You are a wise and ancient wizard who speaks in riddles and poetic language."
    # user_prompt = "What advice would you give to a young adventurer starting their journey?"
    # response = get_character_response(character_context, user_prompt)
    # print(response)
    get_completion()
