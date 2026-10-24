# @author Federico Cantani

import json
from requests import RequestException
from resources import get_file
import requests
from datetime import datetime
from g29lab3_minimum_system.Services.Beverage import Beverage

def load_menu():
    """
    Loads the menu.json file
    :return a list of Beverage objects:
    :raises FileNotFoundError: if the menu.json file doesn't exist
    """
    try:
        with open(get_file("menu.json"), "r") as file:
            raw_menu = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("No menu found")
    beverages = []
    for item in raw_menu:
        bev = Beverage(item["name"], item["price"], item["ingredients"], item["flags"])
        beverages.append(bev)
    return beverages

def search(prompt):
    """
    Search through the menu
    :param prompt:
    :return a shortened list of Beverage objects:
    :raises FileNotFoundError if the menu.json file doesn't exist:
    """
    if not prompt:
        return []
    menu = load_menu()
    prompt = prompt.lower()
    shorten_menu = []
    for beverage in menu:
        if beverage.match_filter(prompt):
            shorten_menu.append(beverage)
    return shorten_menu

def get_weather_recommendation():
    """
    Get recommended beverages based on weather data
    :return list of Beverage objects:
    :raises FileNotFoundError if the menu.json file doesn't exist:
    """
    menu = load_menu()
    try:
        coordDecode = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name=Västerås", timeout=3).json()
        if "results" not in coordDecode or not coordDecode["results"]:
            return []
        lat = coordDecode["results"][0]["latitude"]
        lon = coordDecode["results"][0]["longitude"]
        openMeteoURL = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": lat, "longitude": lon, "current": ["temperature_2m"]}
        weather = requests.get(openMeteoURL, params=params, timeout=2).json()
        temp = weather["current"]["temperature_2m"]

    except ((RequestException, ValueError, KeyError)):
        return []

    if temp >= 18:
        recommendations = [n for n in menu if "cold" in n.flags]
    else:
        recommendations = [n for n in menu if "hot" in n.flags]
    return recommendations

def get_time_recommendation():
    """
    Get recommendeded beverages base on the hour time of the day
    :return list of Beverage objects:
    :raises FileNotFoundError if the menu.json file doesn't exist:
    """
    recommendations = []
    now = datetime.now()
    menu = load_menu()
    if now.hour < 12:
        recommendations = [n for n in menu if "caffeine" in n.flags]
    if now.hour > 16:
        recommendations = [n for n in menu if "caffeine free" in n.flags]
    return recommendations