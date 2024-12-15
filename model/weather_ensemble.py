import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List
from sklearn.linear_model import LinearRegression
from api.weather_api_accuweather import AccuweatherAPI
from api.weather_api_openmeteo import OpenmeteoAPI
from api.weather_api_tomorrowapi import TomorrowapiAPI
from utils import get_current_ts
import os

class EnsembleStrategy(ABC):

    @abstractmethod
    def generate_ensemble(df):
        pass
    
    def combine(self, data_frames: List[pd.DataFrame]) -> pd.DataFrame:
        """Combine multiple data frames into a single ensemble."""
        df_master = pd.DataFrame()
        for df in data_frames:
            try:
                df_master = pd.concat([df_master, df])
            except Exception as e:
                print('There was an error with one of the dataframes, skipping this one')
                print(e)
                continue
        return df_master

class LinearRegressionEnsemble(EnsembleStrategy):
    def __init__(self):
        self.models = {}  # Store one model per target variable

    def generate_ensemble(self, data_frames: List[pd.DataFrame]) -> pd.DataFrame:
        """Combine data frames using linear regression models for multiple target variables."""
        # Combine all data frames
        df = self.combine(data_frames)

        # Identify numeric columns excluding 'source' and 'time'
        numeric_cols = [col for col in df.columns if col not in ['source', 'time']]

        # Dictionary to hold predictions for each target variable
        predictions = {}

        for target in numeric_cols:
            # Features for the current target variable
            features = [col for col in numeric_cols if col != target]

            # Prepare the input (X) and output (y) for the regression model
            X = df[features].values
            y = df[target].values

            # Handle NaN values
            if np.any(np.isnan(X)) or np.any(np.isnan(y)):
                print(f"Warning: NaN values found in target '{target}'. Dropping rows with NaN.")
                valid_rows = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
                X = X[valid_rows]
                y = y[valid_rows]

            # Train a separate model for each target
            model = LinearRegression()
            model.fit(X, y)
            self.models[target] = model

            # Make predictions for the target variable
            predictions[target] = model.predict(X)

        # Create an ensemble DataFrame
        ensemble_df = pd.DataFrame(predictions)
        ensemble_df['time'] = df['time'].iloc[:len(ensemble_df)].values
        ensemble_df['time'] = ensemble_df['time'].dt.tz_localize('UTC')  # Set timezone to UTC
        ensemble_df['time'] = ensemble_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S%z')  # Format time as desired
        ensemble_df['source'] = 'ensemble'

        # Combine the ensemble with the original data
        final_df = pd.concat([df, ensemble_df], ignore_index=True)
        return final_df
    
class LinearRegressionStackingEnsemble(EnsembleStrategy):
    def __init__(self):
        self.meta_models = {}  # Store one meta-model per target variable

    def generate_ensemble(self, data_frames: List[pd.DataFrame], observations: pd.DataFrame) -> pd.DataFrame:
        """Combine data frames using linear regression stacking for multiple target variables."""
        # Combine all data frames
        df = self.combine(data_frames)

        # Merge with observations to align with actual values
        df = pd.merge(df, observations, on="time", suffixes=("_forecast", "_obs"))

        # Identify numeric columns excluding 'source' and 'time'
        forecast_cols = [col for col in df.columns if col.endswith("_forecast")]
        target_cols = [col.replace("_forecast", "_obs") for col in forecast_cols]

        # Dictionary to hold predictions for each target variable
        predictions = {}

        for target_forecast, target_obs in zip(forecast_cols, target_cols):
            # Features: Predictions from all sources for the current target
            features = df[df['source'] != 'ensemble'][[target_forecast, 'source']].pivot(
                index="time", columns="source", values=target_forecast
            ).fillna(0)  # Handle missing values

            # Prepare the input (X) and output (y) for the meta-model
            X = features.values
            y = df[df['source'] == 'ensemble'][target_obs].values

            # Handle NaN values
            if np.any(np.isnan(X)) or np.any(np.isnan(y)):
                print(f"Warning: NaN values found in target '{target_obs}'. Dropping rows with NaN.")
                valid_rows = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
                X = X[valid_rows]
                y = y[valid_rows]

            # Train a meta-model for this target
            meta_model = LinearRegression()
            meta_model.fit(X, y)
            self.meta_models[target_obs] = meta_model

            # Make predictions for the target variable
            predictions[target_obs] = meta_model.predict(X)

        # Create an ensemble DataFrame
        ensemble_df = pd.DataFrame(predictions)
        ensemble_df['time'] = df['time'].iloc[:len(ensemble_df)].values
        ensemble_df['source'] = 'ensemble'

        # Combine the ensemble with the original data
        final_df = pd.concat([df, ensemble_df], ignore_index=True)
        return final_df

class SimpleAverageEnsemble(EnsembleStrategy):
    def generate_ensemble(self, data_frames: List[pd.DataFrame]) -> pd.DataFrame:
        """Combine data frames by calculating a simple average."""
        df = self.combine(data_frames)
        cols = [col for col in df.columns if col  not in ['source', 'time']]
        ensemble_df = df.groupby('time')[cols].mean().reset_index()
        ensemble_df['source'] = 'ensemble'
        final_df = pd.concat([df, ensemble_df], ignore_index=True)
        return final_df

class WeightedAverageEnsemble(EnsembleStrategy):
    def __init__(self, weights: List[float]):
        if not weights or len(weights) <= 0:
            raise ValueError("Weights must be a non-empty list.")
        self.weights = weights

    def generate_ensemble(self, data_frames: List[pd.DataFrame]) -> pd.DataFrame:
        """Combine data frames by calculating a weighted average."""
        if len(data_frames) != len(self.weights):
            raise ValueError("The number of data frames must match the number of weights.")
        
        weighted_sums = pd.DataFrame(0, index=data_frames[0].index, columns=data_frames[0].columns)
        for df, weight in zip(data_frames, self.weights):
            weighted_sums += df * weight
        
        return weighted_sums.sum(axis=1).to_frame(name="combined")

class EnsembleFactory:
    @staticmethod
    def get_ensemble_strategy(strategy_type: str, *args, **kwargs) -> EnsembleStrategy:
        if strategy_type == "simple_average":
            return SimpleAverageEnsemble()
        elif strategy_type == "weighted_average":
            return WeightedAverageEnsemble(*args, **kwargs)
        elif strategy_type == "linear_regression":
            return LinearRegressionEnsemble(*args, **kwargs)
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

