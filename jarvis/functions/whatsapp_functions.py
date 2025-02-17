import time
import pyautogui
from manager.app_manager import open_application

def open_whatsapp():
    """Open WhatsApp application."""
    open_application("whatsapp")
    time.sleep(3)

def open_whatsapp_search_and_send(contact_name, message):
    """Open WhatsApp, search for a contact, and send a message."""
    open_whatsapp()  # Ensure WhatsApp is open
    pyautogui.hotkey('ctrl', 'f')  # Open the search bar
    time.sleep(1)
    pyautogui.write(contact_name)  # Type the contact's name
    time.sleep(1)
    pyautogui.hotkey('ctrl', '1')  # Use Ctrl+1 to open the first search result
    time.sleep(2)
    pyautogui.write(message)  # Type the message
    pyautogui.press('enter')  # Send the message
    print(f"Message sent to {contact_name}: {message}")

def whatsapp_voice_call(contact_name):
    """Initiate a WhatsApp voice call."""
    try:
        open_whatsapp()  # Ensure WhatsApp is open
        pyautogui.hotkey('ctrl', 'f')  # Open the search bar
        time.sleep(1)
        pyautogui.write(contact_name)  # Type the contact's name
        time.sleep(1)
        pyautogui.hotkey('ctrl', '1')  # Use Ctrl+1 to open the first search result
        time.sleep(2)

        # Navigate to the voice call button
        for _ in range(11):  # Press Tab 11 times to reach the call button
            pyautogui.press('tab')
            time.sleep(0.2)
        pyautogui.press('enter')  # Press Enter to make the call

        print(f"Voice call initiated with {contact_name}!")
    except Exception as e:
        print(f"An error occurred while trying to call {contact_name}: {e}")
