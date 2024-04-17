import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('GPT_TOKEN')

def ask_gpt(plantInput):
    plantInput = plantInput.lower()
    filename = f"./backend/database/crops/{plantInput}.txt"  # File name based on user input
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content  # Ensure to return both values
    else:
        try:
            # Initialize the chat session
            chat_session = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": 'You are an application for people to '
                            'tell the users how to plant the crop the most optimal way and '
                            'take care of it for the future. The user will ' 
                            'input a crop and you will respond strictly only with the steps to '
                            'plant the crop and a short biography of the crop. Then after that you will respond with how to take care of it. '
                            'In the directions to take care of the crop, you will give precise details. '
                            'For example, you will give the exact amount someone will have to '
                            'water the plant for it to have the best life. '
                            'The output will be sorted by biography, how to plant, then how to take care of the crop.'
                            'The header of all the outputs will start with -- then the name of the output. '
                            'An example header is: --bio'},
                    {"role": "user", "content": plantInput}
                ]
            )
            reply = chat_session.choices[0].message["content"]
            with open(filename, 'w') as file:
                file.write(reply)
            return reply  # Return both filename and content
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"  # Handle errors gracefully

# Example usage
user_input = "tomato"
reply = ask_gpt(plantInput=user_input)
print(reply)