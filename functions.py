import pygame
import requests
from concurrent.futures import ThreadPoolExecutor


def log(text):
    print(text, flush=True) # force prints inside event loop

# Asynchronous function to load planet data concurrently
def load_planet_data(sprite_sheet):
    with ThreadPoolExecutor() as executor:
        # Fetch the data concurrently
        list1_future = executor.submit(load_planets_data_from_api)
        list2_future = executor.submit(load_additional_planet_data)
        
        list1 = list1_future.result()
        list2 = list2_future.result()
    
    return merge_planet_data(list1, list2)


# Get all planets (/api/v1/planets) 
def load_planets_data_from_api():
    try:
        response = requests.get("https://helldiverstrainingmanual.com/api/v1/planets")
        response.raise_for_status()  # Raises an exception for 4xx/5xx status codes
        data = response.json()
        
        return [
            {
                "parent_number": int(parent_number),
                "name": planet_data["name"],
                "sector": planet_data["sector"],
                "biome": planet_data["biome"]["slug"] if planet_data.get("biome") else "No Biome"
            }
            for parent_number, planet_data in data.items()
        ]
    except requests.RequestException as e:
        print(f"Error loading planet data: {e}")
        return []


# Get additional planet data (/api/v1/war/status)
def load_additional_planet_data():
    try:
        response = requests.get("https://helldiverstrainingmanual.com/api/v1/war/status")
        response.raise_for_status()
        data = response.json()
        
        return data.get("planetStatus", [])
    except requests.RequestException as e:
        print(f"Error loading additional planet data: {e}")
        return []


# Merge API data more efficiently
def merge_planet_data(list1, list2):
    # Convert list2 into a dictionary to optimize lookup time
    status_dict = {item['index']: item for item in list2}
    
    return [
        {**item1, **status_dict.get(item1['parent_number'], {})}
        for item1 in list1
    ]

def smoothZoom(current, target): # exponential smoothing for shmovement

    # take the current size, and get the difference to the target size,
    # divide that difference by 75
    # update the new size to 1/75 of that size difference (can be positive or negative for bigger/smaller).

    # using a smaller number (replacing the 75) will make the animation faster

    # this function is essentially an "ease-out" timing function
    
    return float(current + (target - current)/75)