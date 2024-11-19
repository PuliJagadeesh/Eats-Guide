import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from gtts import gTTS

# Load environment variables
load_dotenv()

# Ensure API key is loaded from the environment variables
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Initialize ChatGroq with the LLM model and API key
llm = ChatGroq(model_name='llama-3.2-1b-preview', api_key=groq_api_key)

def generate_welcome_message(profile_data):
    # Define the prompt with ChatPromptTemplate, as a list of message templates
    chat_prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "Based on the following LinkedIn profile information, create a personalized welcome message.\n\nProfile Data:\n{profile_data}\n\nWelcome Message:"
            )
        ]
    )

    # Format the data as JSON string for the template input
    profile_json = json.dumps(profile_data, indent=2)
    prompt_inputs = {"profile_data": profile_json}

    # Generate the response using the LLM
    response = llm(chat_prompt.format_prompt(**prompt_inputs).to_messages())
    return response.content

# Load JSON profile data
with open("D:/Projects/Liminal/Linkedin_webscrap/sourabh_profile.json", 'r') as file:
    profile_data = json.load(file)

# Access the profile information from the JSON
profile = profile_data[0]['profile']

# Generate the welcome message
welcome_message = generate_welcome_message(profile)

# Print the output
print("Generated Welcome Message:")
print(welcome_message)



def create_audio_from_text(text, filename="D:/Projects/Liminal/Linkedin_webscrap/sourabh_welcome_message.mp3"):
    # Initialize gTTS with the welcome message text and set language to English
    tts = gTTS(text=text, lang='en')

    # Save the audio file
    tts.save(filename)
    print(f"Audio file saved as {filename}")


# Example usage
#welcome_message = "Welcome Saurabh! We're thrilled to have you join us."
create_audio_from_text(welcome_message)

#"D:/Projects/Liminal/Linkedin_webscrap/sourabh_profile.json"