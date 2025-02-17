from flask import Flask, render_template, request, send_from_directory
import os
import openai
import time
import pyautogui
import cv2
from datetime import datetime
from threading import Thread
from config import OPENAI_API_KEY, JARVIS_FOLDER
from manager.app_manager import open_application, close_application
from manager.spotify_manager import play_song, pause_song, skip_song, previous_song
from personal_info import CONTACTS
from functions.media_functions import capture_photo, start_video_recording, stop_video_recording
from functions.whatsapp_functions import open_whatsapp, open_whatsapp_search_and_send, whatsapp_voice_call
from functions.ask_functions import handle_user_input
from pocketsphinx import LiveSpeech  # Import for wake-word detection

# Flask app initialization
app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Ensure necessary directories exist
os.makedirs('static', exist_ok=True)
os.makedirs(JARVIS_FOLDER, exist_ok=True)

# Global variables for video recording
video_recording = False
video_writer = None
video_capture = None

# Activation logic for Jarvis
def activate_jarvis():
    """Logic to execute after the wake word is detected."""
    print("Hello Khushank, how can I assist you today?")
    # Add additional logic to interact with the assistant if required


# Flask Routes
@app.route('/download/<filename>')
def download_file(filename):
    """Serve the requested file for download."""
    file_path = os.path.join(JARVIS_FOLDER, filename)
    
    if os.path.exists(file_path):
        return send_from_directory(JARVIS_FOLDER, filename, as_attachment=True)
    else:
        return f"Sorry, the document '{filename}' was not found.", 404

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle user input and perform tasks."""
    user_input = request.form['user_input'].lower()
    response = handle_user_input(user_input)  # Call the function from ask_functions.py
    
    return render_template('index.html', user_input=user_input, response=response)

# Main Execution
if __name__ == '__main__':
  
    app.run(host='0.0.0.0', port=5000, debug=True)
