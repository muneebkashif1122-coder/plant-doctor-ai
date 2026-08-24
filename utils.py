"""
utils.py

Helper functions for processing and transforming data.
This file does NOT make any network calls -- it only works with
data that has already been fetched (e.g. by api.py).
"""


def extract_plant_info(plantnet_result):
    """
    Takes one raw match from PlantNet's response and extracts
    only the fields we actually need for our UI, in a clean flat format.

    Args:
        plantnet_result: A single dictionary from PlantNet's "results" list
                          (e.g. results[0] for the top match).

    Returns:
        A dictionary with clean, easy-to-use keys:
            - common_name
            - scientific_name
            - family
            - confidence_percent
    """

    # Navigate into the nested "species" dictionary
    species = plantnet_result.get("species", {})

    # commonNames is a list -- we take the first one if it exists,
    # otherwise fall back to the scientific name (some plants have no common name)
    common_names_list = species.get("commonNames", [])
    common_name = common_names_list[0] if common_names_list else species.get("scientificNameWithoutAuthor", "Unknown")

    # Scientific name (e.g. "Tulipa agenensis")
    scientific_name = species.get("scientificNameWithoutAuthor", "Unknown")

    # Family name is nested one level deeper (species -> family -> name)
    family_info = species.get("family", {})
    family = family_info.get("scientificNameWithoutAuthor", "Unknown")

    # PlantNet gives score as a decimal (0.41482) -- we convert it to
    # a human-friendly percentage (41.5%) for display in the UI
    confidence_percent = round(plantnet_result.get("score", 0) * 100, 1)

    return {
        "common_name": common_name,
        "scientific_name": scientific_name,
        "family": family,
        "confidence_percent": confidence_percent
    }


def get_top_matches(results, top_n=3):
    """
    Takes the full list of PlantNet results and returns a clean,
    extracted list of the top N matches.

    Args:
        results: The full "results" list from PlantNet's response.
        top_n: How many top matches to return (default 3, per our spec).

    Returns:
        A list of clean dictionaries (see extract_plant_info above),
        limited to top_n items.
    """
    # results[:top_n] takes only the first top_n items from the list
    # (PlantNet already returns results sorted by confidence, highest first)
    top_results = results[:top_n]

    # Apply extract_plant_info() to each raw result, building a clean list
    return [extract_plant_info(result) for result in top_results]