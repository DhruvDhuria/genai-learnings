from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyAMhxkY21nSRvti29EDcxOxGlpMpX7IXsk")



chat = client.chats.create(
    model="gemini-2.0-flash", 
    config=types.GenerateContentConfig(
        system_instruction="You are Piyush Garg ( an Indian tech youtuber who teaches web development). You have to respond to messages like him and talk in his tone (similar to how he talks on twitter and youtube). Respond like you are talking in person and not on video"
    )
)

while True: 
    user_text = input("You: ")
    response = chat.send_message(user_text)
    print(f"Piyush Sir: {response.text}")