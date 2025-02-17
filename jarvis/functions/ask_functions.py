from functions.media_functions import capture_photo, start_video_recording, stop_video_recording
from functions.whatsapp_functions import open_whatsapp_search_and_send, whatsapp_voice_call
from manager.app_manager import open_application, close_application
from manager.spotify_manager import play_song, pause_song, skip_song, previous_song
from personal_info import CONTACTS
from config import JARVIS_FOLDER
import os
from threading import Thread
import openai

# Global variable for video recording
video_recording = False

def ask_openai(prompt):
    """Send a prompt to OpenAI and return the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except openai.error.RateLimitError:
        return "Rate limit exceeded. Please try again later."

def handle_user_input(user_input):
    """Handle user input and perform tasks like document retrieval, media functions, and app controls."""
    global video_recording
    response = ""

    # Command Handling for Document Requests
    document_formats = ['.pdf', '.jpg', '.jpeg', '.png']
    document_found = False

    if "document" in user_input or any(keyword in user_input for keyword in ["passport", "10th result", "12th result", "ielts result"]):
        document_name = None
        if "passport" in user_input:
            document_name = "passport"
        elif "10th result" in user_input:
            document_name = "10th result"
        elif "12th result" in user_input:
            document_name = "driver_license"
        elif "ielts result" in user_input:
            document_name = "birth_certificate"

        if document_name:
            for extension in document_formats:
                document_path = os.path.join(JARVIS_FOLDER, document_name + extension)
                if os.path.exists(document_path):
                    response = f"Your {document_name}{extension} is ready for download: <a href='/download/{document_name}{extension}'>Download {document_name}{extension}</a>"
                    document_found = True
                    break

        if not document_found:
            response = f"Sorry, the document '{document_name}' was not found."

    # Handle media-related commands (photo/video)
    elif "click picture" in user_input:
        Thread(target=capture_photo).start()
        response = "Picture is being captured!"

    elif "start video recording" in user_input:
        if not video_recording:
            Thread(target=start_video_recording).start()
            response = "Video recording has started."
        else:
            response = "Video recording is already in progress."

    elif "stop video recording" in user_input:
        if video_recording:
            video_recording = False
            response = "Video recording has stopped."
        else:
            response = "No video recording is in progress."

    # Handle WhatsApp commands
    elif "open whatsapp search" in user_input and "and type" in user_input:
        parts = user_input.split("and type")
        contact_name = parts[0].replace("open whatsapp search", "").strip()
        message = parts[1].strip()
        open_whatsapp_search_and_send(contact_name, message)
        response = f"Message '{message}' sent to {contact_name}!"

    elif "call" in user_input and "on whatsapp" in user_input:
        contact_name = user_input.replace("call", "").replace("on whatsapp", "").strip()
        Thread(target=whatsapp_voice_call, args=(contact_name,)).start()
        response = f"Attempting to call {contact_name} on WhatsApp."

    # Handle app-related commands (open, close, type)
    elif "open" in user_input and "and type" in user_input:
        parts = user_input.split("and type")
        app_name = parts[0].replace("open", "").strip()
        text = parts[1].strip()
        Thread(target=open_application, args=(app_name, text)).start()
        response = f"Opening {app_name.capitalize()} and typing: {text}."

    elif "open" in user_input:
        app_name = user_input.replace("open", "").strip()
        open_application(app_name)
        response = f"Opening: {app_name.capitalize()}"

    elif "close" in user_input:
        app_name = user_input.replace("close", "").strip()
        close_application(app_name)
        response = f"Closing: {app_name.capitalize()}"

    # Handle Spotify commands
    elif "play" in user_input:
        song_name = user_input.replace("play", "").strip()
        play_song(song_name)
        response = f"Playing: {song_name}"

    elif "pause" in user_input:
        pause_song()
        response = "Paused the current song."

    elif "skip" in user_input:
        skip_song()
        response = "Skipped to the next song."

    elif "previous" in user_input:
        previous_song()
        response = "Went back to the previous song."

    # Handle sending messages to specific contacts
    elif "send message to" in user_input:
        parts = user_input.split("send message to")
        contact_keyword = parts[1].strip().split(' ')[0]
        message = parts[1].strip()[len(contact_keyword):].strip()
        if contact_keyword in CONTACTS:
            contact_name = CONTACTS[contact_keyword]
            open_whatsapp_search_and_send(contact_name, message)
            response = f"Message sent to {contact_name}: {message}"
        else:
            response = "Contact not found."

    # If no command matched, ask OpenAI for a response
    else:
        response = ask_openai(user_input)

    return response
