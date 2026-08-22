"""
config.py

This file handles the configuration for the entire project.
It loads secret API keys from the .env file and defines
constant values that are used throughout the project.
"""

import os
from dotenv import load_dotenv

# Load the .env file -- this pulls all key-value pairs from .env
# into Python's environment variables
load_dotenv()

# API Keys -- securely read from the .env file
# os.getenv() returns None if the key is not found (does not throw an error)
PLANTNET_API_KEY = os.getenv("PLANTNET_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# PlantNet API base URL -- used to call the plant identification endpoint
PLANTNET_API_URL = "https://my-api.plantnet.org/v2/identify/all"

# Groq model name -- the LLM that will generate the care guide for us
GROQ_MODEL = "llama-3.3-70b-versatile"

# Safety check: if any key is missing, raise a clear error immediately
# (this avoids confusing errors later while the app is running)
if not PLANTNET_API_KEY:
    raise ValueError("PLANTNET_API_KEY not found in .env file! Please check your .env file.")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file! Please check your .env file.")