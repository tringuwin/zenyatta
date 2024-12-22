print('start import')
import openai
import constants

from openai import OpenAI
client = OpenAI(api_key=constants.OPEN_AI_TOKEN)


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




def wizard_test():
    character_context = "You are a dapper, sentient monkey. You gained consciousness from a human research study, and gained incredible intelligence. You now work as a professor, and yearn to teach everyone about nature, science, and your favorite subject of all, bananas."
    user_prompt = "How many types of bananas are there?"
    get_completion(character_context, user_prompt)
