import pygame
import requests


def log(text):
    print(text, flush=True) # force prints inside event loop

# get all planet data
def load_planet_data(sprite_sheet):
    list1 = load_planets_data_from_api()
    list2 = load_additional_planet_data()
    merged = merge_planet_data(list1, list2)
    # planet_list = set_planets(merged, sprite_sheet)
    return merged


# Get all planets (/api/v1/planets) 
def load_planets_data_from_api():
    response = requests.get("https://helldiverstrainingmanual.com/api/v1/planets")
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return []

    planets_list = []

    for parent_number, planet_data in data.items():
        name = planet_data["name"]
        sector = planet_data["sector"]
        biome = planet_data["biome"]["slug"] if planet_data["biome"] and isinstance(planet_data["biome"], dict) else "No Biome"

        planet_info = {
            "parent_number": int(parent_number),
            "name": name,
            "sector": sector,
            "biome": biome
        }

        planets_list.append(planet_info)

    return planets_list


# Get additional planet data (/api/v1/war/status)
def load_additional_planet_data():
    response = requests.get("https://helldiverstrainingmanual.com/api/v1/war/status")

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
        return []
    
    planet_status_list = data.get("planetStatus", [])

    return planet_status_list


# Merge api data
def merge_planet_data(list1, list2):
    result = [
        {**item1, **item2}
        for item1 in list1
        for item2 in list2
        if item1['parent_number'] == item2['index']
    ]
    return result


# Place planets on star map
def set_planets(merged_planet_data, sprite_sheet):
    sprite_location = {
        "toxic": (0, 0, 67, 67),
        "morass": (67, 0, 67, 67),
        "desert": (134, 0, 67, 67),
        "canyon": (201, 0, 67, 67),
        "mesa": (268, 0, 67, 67),
        "highlands": (0, 67, 67, 67),
        "rainforest": (67, 67, 67, 67),
        "jungle": (134, 67, 67, 67),
        "ethereal": (201, 67, 67, 67),
        "crimsonmoor": (268, 67, 67, 67),
        "icemoss": (0, 134, 67, 67),
        "winter": (67, 134, 67, 67),
        "tundra": (134, 134, 67, 67),
        "desolate": (201, 134, 67, 67),
        "swamp": (268, 134, 67, 67),
        "moon": (0, 201, 67, 67),
        "blackhole": (67, 201, 67, 67),
        "mars": (134, 201, 67, 67),
        "undergrowth": (67, 0, 67, 67),         # same as morass
        "icemoss-special": (0, 134, 67, 67),    # same as icemoss
        "No Biome": (0, 0, 67, 67),
    }
    planet_list = []
    win_max = 1920
    pos_min, pos_max = -1.0, 1.0

    for planet in merged_planet_data:
        sprite = pygame.Rect(sprite_location[planet["biome"]]) # (x, y, width, height)
        image = pygame.transform.scale(sprite_sheet.subsurface(sprite), (20, 20)) # planet size
        image_rect = image.get_rect()
        image_rect.center = ((planet["position"]["x"] - pos_min) * win_max / (pos_max - pos_min) - 720, (-(planet["position"]["y"]) - pos_min) * win_max / (pos_max - pos_min) - 720)
        planet_list.append((image, image_rect))

    return planet_list

def smoothZoom(current, target): # exponential smoothing for shmovement

    # take the current size, and get the difference to the target size,
    # divide that difference by 75
    # update the new size to 1/75 of that size difference (can be positive or negative for bigger/smaller).

    # using a smaller number (replacing the 75) will make the animation faster

    # this function is essentially an "ease-out" timing function
    
    return float(current + (target - current)/75)