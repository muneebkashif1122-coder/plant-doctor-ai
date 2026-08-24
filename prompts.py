"""
prompts.py

This file stores the prompt templates we send to the Groq LLM.
Keeping prompts separate from api.py makes them easy to find, read,
and improve without touching the actual API-calling logic.
"""


def build_care_guide_prompt(plant_name, scientific_name):
    """
    Builds the instruction text we send to Groq to generate a plant care guide.

    Args:
        plant_name: The common name of the plant (e.g. "Rose").
        scientific_name: The scientific name (e.g. "Rosa chinensis").

    Returns:
        A string containing the full prompt for the LLM.
    """

    prompt = f"""You are a professional botanist and plant care expert.

Generate a detailed care guide for the following plant:
Common Name: {plant_name}
Scientific Name: {scientific_name}

Respond ONLY with a valid JSON object (no extra text, no markdown formatting,
no code fences) using EXACTLY this structure:

{{
  "water_requirement": "short description of watering needs",
  "sunlight": "short description of sunlight needs",
  "soil_type": "short description of ideal soil",
  "temperature": "ideal temperature range",
  "fertilizer": "fertilizer recommendations",
  "pruning_tips": "pruning advice",
  "common_diseases": "common diseases or pests to watch for",
  "toxicity": "whether the plant is toxic or safe for pets/humans",
  "flowering_season": "when the plant typically flowers, or 'N/A' if not applicable",
  "humidity": "humidity requirements",
  "best_growing_conditions": "summary of ideal growing environment",
  "interesting_fact": "one interesting fact about this plant"
}}

Keep each value concise (1-2 sentences). Do not include any text outside the JSON object."""

    return prompt


def build_plant_name_identification_prompt(user_input):
    """
    Builds a prompt asking Groq to identify the correct English plant name
    from user input that may be in English, Urdu, or Roman Urdu.

    Args:
        user_input: Raw text typed by the user (any of the 3 supported languages).

    Returns:
        A string containing the full prompt for the LLM.
    """

    prompt = f"""You are a botanist assistant that identifies plant names.

The user has typed the following text, which may be in English, Urdu script,
or Roman Urdu (Urdu written using English letters):

"{user_input}"

Identify what plant they are referring to and respond ONLY with a valid JSON
object (no extra text, no markdown, no code fences) using EXACTLY this structure:

{{
  "common_name": "the plant's common English name",
  "scientific_name": "the plant's scientific name",
  "recognized": true
}}

If you cannot confidently identify a real plant from the input, respond with:

{{
  "common_name": "",
  "scientific_name": "",
  "recognized": false
}}"""

    return prompt