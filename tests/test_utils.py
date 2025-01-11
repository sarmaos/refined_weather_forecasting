import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import json
import datetime
from utils import get_current_ts, normalize_df, get_coordinates, read_model_weights


class TestUtilityFunctions(unittest.TestCase):

    def test_get_current_ts(self):
        """Test if get_current_ts returns a properly formatted timestamp."""
        timestamp = get_current_ts()
        self.assertRegex(
            timestamp,
            r'^\d{4}-\d{2}-\d{2}\d{2}\d{2}\d{2}\d{6}$',
            "Timestamp format does not match expected format",
        )

    def test_normalize_df(self):
        """Test normalize_df with a sample DataFrame."""
        input_data = {
            "id": [1, 2],
            "data": [{"a": 10, "b": 20}, {"a": 30, "b": 40}],
        }
        df = pd.DataFrame(input_data)
        cols = ["id", "a", "b"]
        normalize_col = "data"
        expected_output = pd.DataFrame({"id": [1, 2], "a": [10, 30], "b": [20, 40]})

        result = normalize_df(df, cols, normalize_col)
        pd.testing.assert_frame_equal(result, expected_output)

    @patch("utils.pd.read_csv")
    def test_get_coordinates(self, mock_read_csv):
        """Test get_coordinates with mocked city data."""
        mock_data = pd.DataFrame({
            "city": ["Athens"],
            "country": ["Greece"],
            "lat": [37.9838],
            "lng": [23.7275],
        })
        mock_read_csv.return_value = mock_data

        city, country = "Athens", "Greece"
        lat, lng = get_coordinates(city, country)
        self.assertEqual(lat, 37.9838)
        self.assertEqual(lng, 23.7275)

    @patch("builtins.open", new_callable=mock_open, read_data='{"model1": 0.6, "model2": 0.4}')
    def test_read_model_weights(self, mock_file):
        """Test read_model_weights with mocked file data."""
        file_path = "./data/weights.json"
        expected_data = {"model1": 0.6, "model2": 0.4}

        result = read_model_weights(file_path)
        self.assertEqual(result, expected_data)


if __name__ == "__main__":
    unittest.main()
