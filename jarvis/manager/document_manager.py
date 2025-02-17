import os
from flask import send_from_directory
from personal_info import DOCUMENT_KEYWORDS

# Path to the 'jarvis/folder' where images and documents are stored
JARVIS_FOLDER = 'C:/Users/sarda/jarvis/folder'  # Use forward slashes for paths

# Ensure the folder exists
os.makedirs(JARVIS_FOLDER, exist_ok=True)

def download_file(filename):
    """
    Serve the requested file for download.
    
    :param filename: The name of the file to be downloaded.
    :return: A Flask response to send the file for download or an error message if not found.
    """
    file_path = os.path.join(JARVIS_FOLDER, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        return send_from_directory(JARVIS_FOLDER, filename, as_attachment=True)
    else:
        return f"Sorry, the document '{filename}' was not found.", 404

def find_document_in_keywords(user_input, document_formats):
    """
    Search for a document based on user input and return its file path if found.
    
    :param user_input: The user's input string.
    :param document_formats: List of allowed file formats (e.g., ['.pdf', '.jpg']). 
    :return: The file path if found, otherwise None.
    """
    for keyword, document_name in DOCUMENT_KEYWORDS.items():
        if keyword in user_input:
            for extension in document_formats:
                document_path = os.path.join(JARVIS_FOLDER, document_name + extension)
                if os.path.exists(document_path):
                    return document_path
    return None
