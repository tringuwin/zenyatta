import openai

from openai import OpenAI
client = OpenAI(api_key="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")

ZEN_CONTEXT = f"You are a discord bot for a discord server called SPICY OW. SPICY OW is an Overwatch Discord Server. You are responding to questions from discord users in the server who are asking questions about the server. Your goal is to answer their question as accurately as you can based on your knowledge. If you do not know the answer to a question, please politely say that you don't know, and ask them to try again later. Do not give them any information that is not included in the information below. SPICY OW hosts an Overwatch League called the Spicy Overwatch League, or SOL. The league is owned by a user named SpicyRagu. There are 24 total teams in the league. The league is currently in its 5th season.
\nIf someone asks how to join a team, suggest that they check out the team up channel and make a post with some information about themselves and what they're looking for."


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