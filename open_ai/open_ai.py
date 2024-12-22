print('start import')
import openai
import constants

openai.api_key = constants.OPEN_AI_TOKEN
print('after api key')

def get_character_response(character_context, user_prompt):
    """
    Sends a character context and user prompt to OpenAI's API and retrieves the response.
    
    Args:
        character_context (str): The description or background of the character.
        user_prompt (str): The prompt for the AI to respond to in character.
    
    Returns:
        str: The AI's response in character.
    """
    # Send the prompt to OpenAI's GPT model
    response = openai.Chat.create(
        model="gpt-4",  # Use "gpt-4" or another model depending on your needs
        messages=[
            {"role": "system", "content": character_context},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=150,  # Adjust as needed
        temperature=0.7  # Adjust for more/less creative responses
    )
    
    # Extract and return the AI's response
    return response['choices'][0]['message']['content']

# Example usage
def wizard_test():
    character_context = "You are a wise and ancient wizard who speaks in riddles and poetic language."
    user_prompt = "What advice would you give to a young adventurer starting their journey?"
    response = get_character_response(character_context, user_prompt)
    print(response)
