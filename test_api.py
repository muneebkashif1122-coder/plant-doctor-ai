"""
test_api.py

A quick script to test whether the PlantNet API integration works.
This is NOT part of the final app -- just for us to verify api.py works correctly.
"""

import io
from api import identify_plant
from utils import get_top_matches
from api import identify_plant

# Read the raw bytes of the test image
with open("images/images.jpeg", "rb") as f:
    image_bytes = f.read()

# Wrap the bytes in a BytesIO object -- unlike a plain file object,
# BytesIO is a pure-Python object, so we CAN attach custom attributes
# like .name and .type to it (this mimics what Streamlit's file_uploader gives us)
fake_uploaded_file = io.BytesIO(image_bytes)
fake_uploaded_file.name = "images.jpeg"
fake_uploaded_file.type = "image/jpeg"

# Call our function from api.py
result = identify_plant(fake_uploaded_file)

# Print the result so we can inspect its structure
print("Success:", result["success"])
print("Error:", result["error"])
print("Number of results:", len(result["results"]))

# Print the top match in detail
if result["results"]:
    top_match = result["results"][0]
    print("\n--- Top Match (full structure) ---")
    print(top_match)

    # Now test our clean extraction function from utils.py
    print("\n--- Clean Top 3 Matches (using utils.py) ---")
    clean_matches = get_top_matches(result["results"], top_n=3)
    for i, match in enumerate(clean_matches, start=1):
        print(f"\nMatch {i}:")
        print(f"  Common Name: {match['common_name']}")
        print(f"  Scientific Name: {match['scientific_name']}")
        print(f"  Family: {match['family']}")
        print(f"  Confidence: {match['confidence_percent']}%")

# ===== Testing Groq: Care Guide Generation =====
from api import generate_care_guide, identify_plant_from_text

print("\n\n=== Testing Groq Care Guide Generation ===")
care_result = generate_care_guide("Rose", "Rosa chinensis")
print("Success:", care_result["success"])
print("Error:", care_result["error"])
if care_result["success"]:
    print("Care Guide:")
    for key, value in care_result["care_guide"].items():
        print(f"  {key}: {value}")

# ===== Testing Groq: Text-based Plant Identification =====
print("\n\n=== Testing Groq Text Identification (Roman Urdu) ===")
text_result = identify_plant_from_text("gulab")
print("Success:", text_result["success"])
print("Error:", text_result["error"])
if text_result["success"]:
    print("Common Name:", text_result["common_name"])
    print("Scientific Name:", text_result["scientific_name"])