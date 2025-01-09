import pygame
import requests

# Get all planets (/api/v1/planets) 
def load_planets_data_from_api(api_url):
    response = requests.get(api_url)
    
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
def load_additional_planet_data(api_url):
    response = requests.get(api_url)

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
def set_planets(merged_planet_data, sprite_location, sprite_sheet):
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