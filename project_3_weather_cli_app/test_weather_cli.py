"""
Project 3, B - WeatherCli.py

Description:
This program serves to test the core functionalities of the weather app
before running.
"""
import unittest
from unittest import mock
from weather_cli import get_and_display_weather

# Mock JSON data for a successful API response
MOCK_API_DATA = {
	"coord": {"lon": -74.006, "lat": 40.7143},
	"weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}],
	"base": "stations",
	"main": {"temp": 285.5, "feels_like": 284.99, "temp_min": 283.71, "temp_max": 287.05, "pressure": 1014, "humidity": 75},
	"visibility": 10000,
	"wind": {"speed": 2.06, "deg": 280},
	"clouds": {"all": 100},
	"dt": 1678886973,
	"sys": {"type": 2, "id": 2039045, "country": "US", "sunrise": 1678871923, "sunset": 1678912853},
	"timezone": -18000,
	"id": 5128581,
	"name": "New York",
	"cod": 200
}

# The expected formatted output
EXPECTED_OUTPUT = """
Weather in New York, US
----------------------------------
Description: overcast clouds
Temperature: 12.35 °C / 54.23 °F
Humidity: 75%
		"""

class TestWeatherCli(unittest.TestCase):
	"""
	This classs serves to test all of weather_cli's core 
	functionalities.
	"""
	def setUp(self):
		"""
		This method serves to create a mock test object, and will always
		be the first function to run before every test.
		"""
		self.mock_test = mock.Mock()
		self.mock_test.status_code = 200
		self.mock_test.json.return_value = MOCK_API_DATA

		# Create a mock response object for 404 status code
		self.mock_response_404 = mock.Mock()
		self.mock_response_404.status_code = 404

		# Create a mock response object for a 401 status code
		self.mock_response_401 = mock.Mock()
		self.mock_response_401.status_code = 401

	@mock.patch('sys.exit', side_effect=ValueError("Test exit"))
	@mock.patch('requests.get')
	@mock.patch('builtins.print')
	def test_api_call(self, mock_print, mock_get, mock_sys_exit):
		"""
		This function serves to test that a successful API call results
		in the correct output.
		"""
		mock_get.return_value = self.mock_test
		get_and_display_weather("New York")
		expected_output_string = EXPECTED_OUTPUT.strip()
		mock_print.assert_called_once()
		actual_output_string = mock_print.call_args[0][0].strip()
		self.assertEqual(actual_output_string, expected_output_string)

	# using mock in testing for invalid cities
	@mock.patch('sys.exit', side_effect=ValueError("Test Exit"))
	@mock.patch('requests.get')
	@mock.patch('builtins.print')
	def test_for_invalid_city(self, mock_print, mock_get, mock_sys_exit):
		"""
		This function serves to test for if there is
		an invalid city.

                args:
        
		"""
		mock_get.return_value = self.mock_response_404
		get_and_display_weather("Hong Kong")
		mock_print.assert_called_once_with("Error: City not found.")

	# adding same decorators to this function
	@mock.patch('sys.exit', side_effect=ValueError("Test Exit"))
	@mock.patch('requests.get')
	@mock.patch('builtins.print')
	def test_for_invalid_api_key(self, mock_print, mock_get, mock_sys_exit):
		"""
		This function serves to test the validity of API keys.
		"""
		# configuring request.get to return the self.mock_response_404
		#object.
		mock_get.return_value = self.mock_response_401 # <-------- here it is, what are you on about?
		
		# calling get_and_display_weather() with a city name
		get_and_display_weather("London")
		
		# using assert_called to check if the print function was called
		# during the error message.
		mock_print.assert_called_once_with("Error: Invalid API key. Please check your .env file.")

	@mock.patch('sys.exit', side_effect=ValueError("Test Exit"))
	@mock.patch('requests.get')
	@mock.patch('builtins.print')
	def test_for_network_error(self, mock_print, mock_get, mock_sys_exit):
		"""
		This function serves to rest for network error issues.
		"""
		mock_get.side_effect = RequestException("Testing network error.") # <-------- here it is, what are you on about? 
		get_and_display_weather("London")
		mock_print.assert_called_once_with("An error occurred: Testing network error.") # <-------- here it is, what capitalization are you on about? 


if __name__ == "__main__":
	"""
	main function: executes test
	"""	
	unittest.main()
