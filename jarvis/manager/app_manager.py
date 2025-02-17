import os

# Function to open an application based on user input
def open_application(app_name):
    app_commands = {
        "brave": 'start brave',
        "chrome": 'start chrome',
        "notepad": 'start notepad',
        "calculator": 'start calc',
        "spotify": 'start spotify',
        "camera": 'start microsoft.windows.camera:',
        "whatsapp": 'start whatsapp://',
        
        # Add more applications here as needed
    }
    
    if app_name.lower() in app_commands:
        os.system(app_commands[app_name.lower()])
        print(f"{app_name.capitalize()} is now open.")
    else:
        print(f"Sorry, I don't know how to open {app_name}. Please add it to the command list.")

# Function to close an application based on user input
def close_application(app_name):
    app_processes = {
        "brave": "brave.exe",
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "whatsapp": "Whatsapp.exe",
        # Add more applications here as needed
    }
    
    if app_name.lower() in app_processes:
        try:
            os.system(f'taskkill /f /im {app_processes[app_name.lower()]}')
            print(f"{app_name.capitalize()} should now be closed.")
        except Exception as e:
            print(f"Error closing {app_name}: {e}")
    else:
        print(f"Sorry, I don't know how to close {app_name}. Please add it to the command list.")