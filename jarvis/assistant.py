import os
import time
import openai
import pyttsx3
import speech_recognition as sr
from config import OPENAI_API_KEY  # Import API key from config
from manager.app_manager import open_application, close_application  # Import functions from app_manager
from manager.spotify_manager import play_song, pause_song, skip_song, previous_song  # Import Spotify functions

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up text-to-speech engine
engine = pyttsx3.init()

# Function to speak the AI's response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice input from the user
def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand that. Please repeat.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")
        return None

# Function to interact with OpenAI and get a response
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 turbo for cost-efficiency
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Retrying after 30 seconds...")
        time.sleep(30)  # Pause before retrying
        return "I'm currently unavailable due to rate limits. Please try again later."

# Main function to handle user input and interaction with AI
def chat():
    print("Hello! I'm your AI assistant. Type 'quit' to exit or say 'quit' to stop.")
    speak("Hello! I'm your AI assistant. How can I help you today?")

    while True:
        user_input = listen()  # Use voice input instead of text input

        if user_input is None:
            continue  # If there's no input, continue listening

        if "quit" in user_input:
            speak("Goodbye!")
            print("Goodbye!")
            break

        elif "open" in user_input:
            app_name = user_input.replace("open", "").strip()
            open_application(app_name)
            speak(f"Opening {app_name}")

        elif "close" in user_input:
            app_name = user_input.replace("close", "").strip()
            close_application(app_name)
            speak(f"Closing {app_name}")

        elif "play" in user_input:
            # Extract the song name from the user input
            song_name = user_input.replace("play", "").strip()
            play_song(song_name)  # Call the play_song function with the song name
            speak(f"Playing {song_name}")

        elif "pause" in user_input:
            pause_song()
            speak("Pausing the song")

        elif "skip" in user_input:
            skip_song()
            speak("Skipping to the next song")

        elif "previous" in user_input:
            previous_song()
            speak("Going back to the previous song")


        else:
            response = ask_openai(user_input)
            print(f"AI: {response}")
            speak(response)  # Speak the AI's response


# Start the chat function
chat()
