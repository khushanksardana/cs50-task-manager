import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from manager.app_manager import open_application  # Import open_application function to launch Spotify

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-modify-playback-state,user-read-playback-state'))

def open_spotify():
    """Ensure Spotify is running by opening it if it's not already open."""
    try:
        open_application("spotify")  # You may need to add 'spotify' to your app_commands in app_manager.py
        print("Spotify has been opened.")
    except Exception as e:
        print(f"Error opening Spotify: {e}")

def play_song(track_name):
    """
    Search for a track by name and play it, retrying if Spotify isn't ready yet.
    
    Args:
        track_name (str): The name of the track to play.
    """
    # Ensure Spotify is running before trying to play the song
    open_spotify()
    
    # Wait until Spotify is ready
    retries = 0
    max_retries = 10  # Try 10 times before giving up
    while retries < max_retries:
        # Get the current playback state
        playback = sp.current_playback()
        
        # Check if there's an active device playing music
        if playback and playback.get('device') and playback['device'].get('is_active', False):
            # Spotify is ready, search for the track
            results = sp.search(q=track_name, type='track', limit=1)
            tracks = results['tracks']['items']
            
            if tracks:
                track_uri = tracks[0]['uri']
                sp.start_playback(uris=[track_uri])
                print(f"Playing: {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}")
                return  # Song started playing, exit the function
            else:
                print("Track not found.")
                return
        else:
            # Spotify is not ready yet, retry after 2 seconds
            print("Spotify is not ready yet. Retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying
            retries += 1
    
    print("Spotify is still not ready after several attempts. Please check the app.")
    
def pause_song():
    """Pause the currently playing song."""
    sp.pause_playback()
    print("Paused the current song.")

def skip_song():
    """Skip to the next track."""
    sp.next_track()
    print("Skipped to the next song.")

def previous_song():
    """Go back to the previous track."""
    sp.previous_track()
    print("Went back to the previous song.")
