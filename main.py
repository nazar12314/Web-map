#Imports
import argparse
import folium
import re
from geopy.geocoders import Nominatim
from queue import PriorityQueue
from itertools import count
from haversine import haversine
from math import floor
from typing import Dict


def parser():
    """
    Parser of console arguments
    Returns 3 required arguments parsed from a user input into console
    """
    my_parser = argparse.ArgumentParser(description="Web map")
    my_parser.add_argument("year", type=str)
    my_parser.add_argument("latitude", type=float)
    my_parser.add_argument("longitude", type=float)
    return my_parser.parse_args()


def parse_info(data: str, year: str):
    """
    A function to parse info from a given file with films.
    Returns a dictionary of objects:
    Object example: {"name": str, "year": str, "places": []}

    (str, str) -> dictionary
    """
    result = {}
    i = 1
    with open(data, encoding='unicode_escape') as file:
        for line in file.readlines():
            year_or_publication = re.findall("([0-9]{4})", line)
            if year_or_publication == [year]:
                line = line.replace("\n", "").replace("\t", "")
                items = line.split(",")
                element_object = {
                    "name": re.findall("\".*\"", line) if re.findall("\".*\"", line) else line[:line.find("(")],
                    "year": year_or_publication,
                    "places": [items[0][items[0].rfind("}") + 1:] if "}" in items[0]
                               else items[0][items[0].rfind(")") + 1:],
                               *items[1:-1], re.sub(r'\(.*?\)', '', items[-1]) if len(items) > 1 else ""]
                }
                result[i] = element_object
                if i == 500:
                    break
                i += 1
    return result


def coordinates_maker(data: Dict):
    """
    This function converts places where films were made into coordinates via geopy module
    """
    cache = {}
    geolocator = Nominatim(user_agent="my_user_agent")
    for data_object in data:
        i = 1
        item = data[data_object]["places"]
        element = ",".join(item)
        if element not in cache:
            loc = geolocator.geocode(element)
            cache[element] = loc
            while loc is None:
                item = item[i:]
                element = ",".join(item)
                loc = geolocator.geocode(element)
                i += 1
                cache[element] = loc
                if i == len(data[data_object]["places"]):
                    break
            try:
                data[data_object]["places"] = (loc.latitude, loc.longitude)
            except AttributeError:
                pass
        else:
            element1 = cache.get(element)
            if element1 is not None:
                data[data_object]["places"] = (element1.latitude, element1.longitude)


def calculate_distances(data: Dict, args):
    """
    This function uses haversine formula to calculate distance between the given coordinates
     and coordinates of given places where films were made

    It uses PriorityQueue to sort places in rising order and optimize extracting info

    (Dict, List) -> PriorityQueue object
    """
    result = PriorityQueue()
    unique = count()
    for item_object in data:
        if not isinstance(data[item_object]["places"][0], str):
            latitude, longitude = data[item_object]["places"]
        if latitude is not None and longitude is not None:
            distance = haversine((args.latitude, args.longitude), (latitude, longitude))
            result.put((distance, next(unique), data[item_object]))
    return result


def take_ten_nearest_places(data: PriorityQueue):
    """
    This function takes a formed PriorityQueue of objects and returns 10 first elements
    (closest to the given coordinates)

    (PriorityQueue) -> List
    """
    items = []
    response = []
    while len(response) < 10:
        item = data.get()
        if item[2]["places"] in items:
            pass
        else:
            items.append(item[2]["places"])
            if not isinstance(item[2]["places"][0], str):
                response.append((item[0], item[2]))
    return response


def map_creator(args, data_for_markers):
    """
    This function creates a web-map from the given data via the folium module
    Returns generated HTML file named "map.html"
    """
    map_object = folium.Map(location=[args.latitude, args.longitude], zoom_start=6)
    feature_group = folium.FeatureGroup("Lines")
    feature_group1 = folium.FeatureGroup("Area")
    folium.Marker([args.latitude, args.longitude],
                  popup="<strong>Given coordinate</strong>",
                  icon=folium.Icon(color="red")).add_to(map_object),
    for item in data_for_markers:
        name = item[1]["name"]
        year = item[1]["year"]
        i_frame1 = folium.IFrame(f"<strong>{name[0]}</strong><br><br>Year: {year[0]}")
        i_frame2 = folium.IFrame(f"{name[0]}<br><br><strong>Area of filming</strong>")
        popup1 = folium.Popup(i_frame1, min_width=150, max_width=150)
        popup2 = folium.Popup(i_frame2, min_width=150, max_width=150)
        folium.Marker([*item[1]["places"]], popup=popup1).add_to(map_object),
        folium.Circle(location=[*item[1]["places"]],
                      radius=100000, popup=popup2,
                      color="blue", fill=True).add_to(feature_group1)
        folium.PolyLine([[args.latitude, args.longitude], [*item[1]["places"]]],
                        popup=f"{floor(item[0])} km").add_to(feature_group)
    feature_group.add_to(map_object)
    feature_group1.add_to(map_object)
    folium.LayerControl().add_to(map_object)
    map_object.save("map.html")


def main():
    """
    Executes all functions
    """
    args = parser()
    data = parse_info("locations.list", args.year)
    coordinates_maker(data)
    updated_data = calculate_distances(data, args)
    result = take_ten_nearest_places(updated_data)
    map_creator(args, result)


if __name__ == '__main__':
    main()
