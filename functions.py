import json
import requests

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
        # for planet in planets_list:
        #     print(planet)

    return planets_list

def load_additional_planet_data(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
        return []
    
    planet_status_list = data.get("planetStatus", [])
    # for planet in planet_status_list:
    #     print(planet)

    return planet_status_list

def merge_planet_data(list1, list2):
    result = [
        {**item1, **item2}
        for item1 in list1
        for item2 in list2
        if item1['parent_number'] == item2['index']
    ]
    print(result[9])
    return result