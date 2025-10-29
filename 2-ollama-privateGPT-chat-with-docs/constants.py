import os

# Define the folder for storing database
PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY', 'db')

# Define the Chroma settings - using None for newer versions
CHROMA_SETTINGS = None
