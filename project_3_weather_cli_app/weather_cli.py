"""
Project 3, A: Weather CLI - API
"""
import os
import sys
from dotenv import load_dotenv
from requests import get
import urllib.parse
from requests.exceptions import HTTPError, RequestException

load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("API_KEY")

def construct_api_url(base_url, endpoint, params=None):
    """
    This function serves to construct the API URL using
    the open weather API

    args:
        base_url: The Base URL of the API.
        endpoint: The specific endpoint
        params: A dictionary of query parameters.

    returns:
        string: the constructed url.
    """
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"

    return url

def server_api_connection_test(final_url):
    """
    This function serves to test the connection of the servee
    with the API and returns the JSON data.

    args:
        final_url: The complete url request.

    return:
        dict: The JSON data from the API response if successful,
              otherwise None.
    """
    try:
        # Initializing final_url into response
        response = get(final_url)
        
        # Check for specific HTTP errors
        if response.status_code == 404:
            print("Error: City not found.")
            return None
        elif response.status_code == 401:
            print("Error: Invalid API key. Please check your .env file.")
            return None
            
        # Raise an exception for other HTTP errors (4xx or 5xx)
        response.raise_for_status()
        
        # Checks for successful value 200
        if response.status_code == 200:
            data = response.json()
            return data
    
    # Catch all other request-related exceptions
    except RequestException as e:
        print(f"An error occurred: {e}")
        return None

def fahrenheit(k):
    """
    This function simply converts and returns the value of kelvin
    to fahrenheit.

    args:
        k: temperature in kelvin

    returns:
        double: converted kelvin to fahrenheit
    """
    return (k - 273.15) * 9/5 + 32
    
def celcius(k):
    """
    This function simply converts and returns the value of kelvin
    to celcius.

    args:
        k: temperature in kelvin

    returns:
        double: converted kelvin to celcius
    """
    return k - 273.15

def get_and_display_weather(city_name):
    """
    This function serves to get and display weather data for a given city.

    args:
        city_name: string name of city

    returns:
        None
    """
    # important variables
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    ENDPOINT = "weather"

    # initializing city name and api_key into a dictionary.
    PARAMETERS = {"q": city_name, "appid": API_KEY}

    # geting the final url.
    final_url = construct_api_url(BASE_URL, ENDPOINT, params=PARAMETERS)

    # confirmation message
    print(f"Constructed URL: {final_url}")

    # capturing data from server_api_connection_test()
    data = server_api_connection_test(final_url)
    
    # check if data was successfully returned
    if data:
        # parsing specific information
        city = data['name']
        country = data['sys']['country']
        weather_description = data['weather'][0]['description']
        current_temperature_in_kelvin = data['main']['temp']
        humidity = data['main']['humidity']

        # converting temperatures
        temp_celsius = celcius(current_temperature_in_kelvin)
        temp_fahrenheit = fahrenheit(current_temperature_in_kelvin)

        # format and print the data
        print(f"""Weather in {city}, {country}----------------------------------Description: {weather_description}Temperature: {temp_celsius:.2f} °C / {temp_fahrenheit:.2f} °F Humidity: {humidity}%""")

    # --- New Logic for Chunk 4 ---
    
# Check for command-line arguments
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python weather_cli.py <city_name>")
        sys.exit(1)
    
    city_name = sys.argv[1]
    get_and_display_weather(city_name)
