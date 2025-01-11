import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import pandas as pd
import datetime


class TestStreamlitApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Streamlit app test object."""
        cls.app_test = AppTest.from_file("test_main.py")

    def run_app(self):
        """Run the app and assert no exceptions occurred."""
        self.app_test.run()
        self.assertIsNotNone(self.app_test.exception)

    def test_title(self):
        self.run_app()
        self.assertEqual(self.app_test.title[0].value, 'Weather Forecast App 🌦️')

    @patch("app.data.fetch_weather_data")
    def test_fetch_weather_data_with_mocked_data(self, mock_fetch_weather_data):
        dummy_data = pd.DataFrame({
            "time": [
                datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)
            ],
            "temperature_c": [20 + i for i in range(12)],
            "feels_like": [19 + i for i in range(12)],
            "precipitation_probability": [10 * i for i in range(12)],
            "wind_speed": [5 + i for i in range(12)],
            "wind_direction": [180 + i for i in range(12)],
            "relative_humidity": [50 - i for i in range(12)],
            "source": ["ensemble"] * 12,
        })

       
        self.run_app()
        self.app_test.sidebar.selectbox('select_strategy').set_value('simple_average').run()
        self.app_test.sidebar.selectbox('select_country').set_value('Greece').run()
        self.app_test.sidebar.selectbox('select_city').set_value('Athens').run()

        mock_fetch_weather_data.return_value = dummy_data
        mock_fetch_weather_data.assert_called_once_with("Athens", "Greece", "simple_average")

   

if __name__ == "__main__":
    unittest.main()
