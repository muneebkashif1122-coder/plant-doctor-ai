"""
api.py

This file handles all external API calls used in the project:
1. PlantNet API -- identifies a plant from an image
2. Groq API -- generates a care guide from a plant name
3. Groq API -- identifies a plant name from text (English, Urdu, or Roman Urdu)
"""

import requests
import json
from config import PLANTNET_API_KEY, PLANTNET_API_URL, GROQ_API_KEY, GROQ_MODEL
from prompts import build_care_guide_prompt, build_plant_name_identification_prompt


def identify_plant(image_file):
    """
    Sends an image to the PlantNet API and returns identification results.

    Args:
        image_file: An image file object (e.g. from Streamlit's file_uploader
                    or camera_input). Must support .read() like a normal file.

    Returns:
        A dictionary with:
            - "success": True/False
            - "results": list of plant matches (if success)
            - "error": error message (if not success)
    """

    # Build the full URL: base endpoint + API key
    url = f"{PLANTNET_API_URL}?api-key={PLANTNET_API_KEY}"

    # PlantNet expects the image as multipart/form-data.
    # The key "images" must match what PlantNet's API expects.
    files = {
        "images": (image_file.name, image_file, image_file.type)
    }

    # PlantNet also wants to know which "organ" of the plant is shown
    # (leaf, flower, fruit, bark). We default to "leaf" since our app
    # doesn't ask the user to specify -- this is a reasonable general default.
    data = {
        "organs": "leaf"
    }

    try:
        # Send the POST request to PlantNet with a timeout
        # (timeout prevents the app from hanging forever if PlantNet is slow)
        response = requests.post(url, files=files, data=data, timeout=80)

        # Raise an exception if PlantNet returned an HTTP error (4xx or 5xx)
        response.raise_for_status()

        # Convert the JSON response into a Python dictionary
        result_json = response.json()

        return {
            "success": True,
            "results": result_json.get("results", []),
            "error": None
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "results": [],
            "error": "PlantNet API took too long to respond. Please try again."
        }

    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False,
            "results": [],
            "error": f"PlantNet API error: {http_err}"
        }

    except requests.exceptions.RequestException as req_err:
        return {
            "success": False,
            "results": [],
            "error": f"Network error while contacting PlantNet: {req_err}"
        }


def generate_care_guide(plant_name, scientific_name):
    """
    Sends the plant name to Groq and returns an AI-generated care guide.

    Args:
        plant_name: Common name of the plant (e.g. "Rose").
        scientific_name: Scientific name (e.g. "Rosa chinensis").

    Returns:
        A dictionary with:
            - "success": True/False
            - "care_guide": dict with care guide fields (if success)
            - "error": error message (if not success)
    """

    # Build the prompt text using our template from prompts.py
    prompt_text = build_care_guide_prompt(plant_name, scientific_name)

    # Groq's API endpoint for chat completions
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Groq requires the API key in the Authorization header (Bearer token format)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # The request body follows the standard "chat" format:
    # a list of messages with a "role" (who's speaking) and "content" (the text)
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.3  # low temperature = more focused, consistent answers
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        response_json = response.json()

        # Extract the actual text content the LLM generated
        raw_text = response_json["choices"][0]["message"]["content"]

        # The LLM was instructed to respond with pure JSON, so we parse
        # that text string into an actual Python dictionary
        care_guide = json.loads(raw_text)

        return {
            "success": True,
            "care_guide": care_guide,
            "error": None
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "care_guide": None,
            "error": "Groq API took too long to respond. Please try again."
        }

    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False,
            "care_guide": None,
            "error": f"Groq API error: {http_err}"
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "care_guide": None,
            "error": "Groq returned an invalid response format. Please try again."
        }

    except requests.exceptions.RequestException as req_err:
        return {
            "success": False,
            "care_guide": None,
            "error": f"Network error while contacting Groq: {req_err}"
        }


def identify_plant_from_text(user_input):
    """
    Takes raw user text (English, Urdu, or Roman Urdu) and asks Groq
    to identify the correct plant name.

    Args:
        user_input: The text typed by the user in the search box.

    Returns:
        A dictionary with:
            - "success": True/False
            - "common_name": identified plant name (if recognized)
            - "scientific_name": identified scientific name (if recognized)
            - "error": error message (if not success or not recognized)
    """

    prompt_text = build_plant_name_identification_prompt(user_input)

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.2  # very low -- we want consistent, factual identification
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        response_json = response.json()
        raw_text = response_json["choices"][0]["message"]["content"]
        parsed = json.loads(raw_text)

        # Check if Groq was actually able to recognize the plant
        if not parsed.get("recognized", False):
            return {
                "success": False,
                "common_name": None,
                "scientific_name": None,
                "error": "Could not recognize a plant name from your input. Please try again."
            }

        return {
            "success": True,
            "common_name": parsed.get("common_name"),
            "scientific_name": parsed.get("scientific_name"),
            "error": None
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "common_name": None,
            "scientific_name": None,
            "error": "Groq API took too long to respond. Please try again."
        }

    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False,
            "common_name": None,
            "scientific_name": None,
            "error": f"Groq API error: {http_err}"
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "common_name": None,
            "scientific_name": None,
            "error": "Groq returned an invalid response format. Please try again."
        }

    except requests.exceptions.RequestException as req_err:
        return {
            "success": False,
            "common_name": None,
            "scientific_name": None,
            "error": f"Network error while contacting Groq: {req_err}"
        }