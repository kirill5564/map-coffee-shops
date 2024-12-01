import json
import requests
from geopy import distance
from pprint import pprint
import folium
import os
from dotenv import load_dotenv


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance_coffee(list_coffee_house):
    return list_coffee_house['distance']


def main():
    my_file = open('coffee.json', 'r')
    file_contents = my_file.read()
    coffee_houses = json.loads(file_contents)
    load_dotenv()
    apikey = os.getenv('API_KEY')
    print('Введите местоположение: ')
    user_coordinates = fetch_coordinates(apikey, input())
    user_coordinates = (user_coordinates[1], user_coordinates[0])
    list_coffee_houses = []
    m = folium.Map(location=user_coordinates)
    for i in range(len(coffee_houses)):
        title = coffee_houses[i]['Name']
        longitude = coffee_houses[i]['geoData']['coordinates'][0]
        latitude = coffee_houses[i]['geoData']['coordinates'][1]
        coordinates_coffee = (latitude, longitude)
        distance_coffee = distance.distance(user_coordinates, coordinates_coffee).km
        list_coffee_houses.append({
        'title': title,
        'distance': distance_coffee,
        'latitude': latitude,
        'longitude': longitude,
        })
    my_file.close()
    nearest_coffee = sorted(list_coffee_houses, key=get_distance_coffee)[:5]
    for i in range(len(nearest_coffee)):
        longitude = nearest_coffee[i]['longitude']
        latitude = nearest_coffee[i]['latitude']
        title = nearest_coffee[i]['title']
        folium.Marker(
        location=[latitude, longitude],
        tooltip="Нажми на меня",
        popup=title,
        icon=folium.Icon(icon="cloud"),
        ).add_to(m)
    m.save("index.html")


if __name__ == '__main__':
    main()
