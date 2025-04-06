from prompt_builder import prompt_builder
from groq import Groq
from config import GROQ_API_KEY

def get_groq_completion(content : str, api_key=GROQ_API_KEY):
    """
    Gets a chat completion from the Groq API.

    :param api_key: API key for the Groq service.
    :param content: The content to be sent to the model.
    :return: The response message content from the API.
    """
    # Initialize the Groq client with the provided API key
    client = Groq(api_key=api_key)

    # Request a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": content},
        ],
        model="llama3-70b-8192",
        # response_format={"type": "json_object"},
        # temperature=0.7

    )

    # Return the content of the first choice's message
    return chat_completion.choices[0].message.content

def get_car_data(user_input: dict) -> str:
    """
    Generates a travel itinerary based on the user input.

    :param user_input: The user input dictionary.
    :return: The generated travel itinerary.
    """
    # Generate the prompt for the user input
    prompt = prompt_builder(user_input)

    # Get the completion from the Groq API
    completion = get_groq_completion(prompt)

    return completion