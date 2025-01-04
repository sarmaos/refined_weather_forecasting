from abc import ABC, abstractmethod
import pandas as pd

class WeatherAPI(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str:
        pass

    @abstractmethod
    def get_raw_data(self, lat: float, lng: float) -> pd.DataFrame:
        """Fetch and process weather data from the API."""
        pass
    
    @abstractmethod
    def normalize_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Normalize raw weather data into a standard format."""
        pass

    def get_data(self, lat: float, lng: float) -> pd.DataFrame:
        """Fetch and normalize weather data."""
        raw_data = self.get_raw_data(lat, lng)
        normalized_data = self.normalize_data(raw_data)
        filtered_data = self.filter_dataframe_with_next_12_hours(normalized_data)
        return filtered_data
    
    def filter_dataframe_with_next_12_hours(self, df):
        start_time = pd.Timestamp.now(tz="UTC")
        end_time = start_time + pd.Timedelta(hours=12)
        filtered_df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]
        return filtered_df