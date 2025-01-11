import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from api.weather_api_accuweather import AccuweatherAPI
from api.weather_api_openmeteo import OpenmeteoAPI
from api.weather_api_tomorrowapi import TomorrowapiAPI

class TestAccuweatherAPI(unittest.TestCase):

    @patch('api.weather_api_tomorrowapi.requests.get')  # Patch the 'requests.get' function to mock API calls
    def test_get_raw_data(self, mock_get):
        # Mock the response for location search
        mock_location_response = MagicMock()
        # Ensure this returns a dictionary with the 'Key' for location search
        mock_location_response.json.return_value = {'Key': '12345'}
        # Mock the response for weather forecast
        mock_weather_response = MagicMock()
        # Return a list with sample weather forecast data
        mock_weather_response.json.return_value = [{'DateTime': '2025-01-05T00:00:00', 'Temperature': {'Value': 22.0}}]
        # Set up the side_effect as a list of mock responses
        mock_get.side_effect = [mock_location_response, mock_weather_response]
        # Instantiate the AccuweatherAPI class with a mock API key
        api = AccuweatherAPI(api_key='fake_api_key')
        # Call the method to test
        lat, lng = 40.7128, -74.0060  # Example coordinates (New York City)
        df = api.get_raw_data(lat, lng)
        # Apply the logic to extract the 'Value' from the 'Temperature' column
        df['temperature'] = df['Temperature'].apply(lambda x: x['Value'])
        # Assertions
        self.assertIsInstance(df, pd.DataFrame)  # Check if the result is a DataFrame
        self.assertEqual(df.shape[0], 1)  # Check if there's 1 row in the DataFrame (one forecast)
        self.assertEqual(df['DateTime'][0], '2025-01-05T00:00:00')  # Check if the date is correct
        self.assertEqual(df['temperature'][0], 22.0)  # Check if the extracted temperature is correct

class TestOpenmeteoAPI(unittest.TestCase):
    def setUp(self):
        self.api = OpenmeteoAPI()
        self.lat = 37.7749  # Example latitude
        self.lng = -122.4194  # Example longitude

    @patch("openmeteo_requests.Client")
    @patch("requests_cache.CachedSession")
    def test_get_raw_data_success(self, mock_cached_session, mock_client):
        # Mocking CachedSession and retry
        mock_session = MagicMock()
        mock_cached_session.return_value = mock_session

        # Mocking Client and API responses
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_response = MagicMock()

        # Mock the structure of the API response
        hourly_mock = MagicMock()
        hourly_mock.Time.return_value = 1672531200  # Mock start time (as a Unix timestamp)
        hourly_mock.TimeEnd.return_value = 1672534800  # Mock end time (as a Unix timestamp)
        hourly_mock.Interval.return_value = 3600  # Mock interval in seconds
        hourly_mock.Variables.side_effect = lambda index: MagicMock(
            ValuesAsNumpy=MagicMock(return_value=[10.0 + index])
        )

        mock_response.Hourly.return_value = hourly_mock
        mock_client_instance.weather_api.return_value = [mock_response]

        # Call the method
        result = self.api.get_raw_data(self.lat, self.lng)

        # Validate the DataFrame structure
        self.assertIsInstance(result, pd.DataFrame)
        expected_columns = [
            "date", "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "precipitation_probability", "cloud_cover", "wind_speed_120m",
            "wind_direction_120m", "wind_gusts_10m", "temperature_120m",
        ]
        self.assertListEqual(list(result.columns), expected_columns)

        # Validate DataFrame contents
        self.assertEqual(len(result), 1)  # Mocked data has only one entry
        self.assertEqual(result.loc[0, "temperature_2m"], 10.0)
        self.assertEqual(result.loc[0, "relative_humidity_2m"], 11.0)
        self.assertEqual(result.loc[0, "apparent_temperature"], 12.0)

class TestTomorrowapiAPI(unittest.TestCase):

    def setUp(self):
        """Set up test resources."""
        self.api_key = "test_api_key"
        self.weather_api = TomorrowapiAPI(self.api_key)

    @patch("api.weather_api_tomorrowapi.requests.get")  # Replace with your actual module name
    def test_get_raw_data_success(self, mock_get):
        """Test get_raw_data with a successful API response."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "timelines": {
                "hourly": [
                    {"time": "2025-01-06T00:00:00Z", "temperature": 5},
                    {"time": "2025-01-06T01:00:00Z", "temperature": 6},
                ]
            }
        }
        mock_get.return_value = mock_response

        # Call the method
        result = self.weather_api.get_raw_data(lat=40.7128, lng=-74.0060)

        # Check the result
        expected_df = pd.DataFrame(
            [
                {"time": "2025-01-06T00:00:00Z", "temperature": 5},
                {"time": "2025-01-06T01:00:00Z", "temperature": 6},
            ]
        )
        pd.testing.assert_frame_equal(result, expected_df)


if __name__ == "__main__":
    unittest.main()
