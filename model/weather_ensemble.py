import pandas as pd
from abc import ABC, abstractmethod
from typing import List
from utils import read_model_weights

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
    def __init__(self):
        """
        Initialize with a dictionary of weights for each source.
        Example: {'source1': 0.5, 'source2': 0.3, 'source3': 0.2}
        """
        self.weights = read_model_weights('data/model_weights.json')['weight']

    def generate_ensemble(self, data_frames: List[pd.DataFrame]) -> pd.DataFrame:
        """Combine data frames by calculating a weighted average."""
        # Combine all data frames
        df = self.combine(data_frames)

        # Columns to compute the weighted average for
        cols = [col for col in df.columns if col not in ['source', 'time']]

        # Ensure all sources have a weight
        missing_sources = set(df['source'].unique()) - set(self.weights.keys())
        if missing_sources:
            raise ValueError(f"Weights are missing for sources: {missing_sources}")

        # Map weights to each source
        df['weight'] = df['source'].map(self.weights)

        # Calculate weighted sum and total weight within each group
        def calculate_weighted_average(group):
            weighted_sum = (group[cols].multiply(group['weight'], axis=0)).sum()
            total_weight = group['weight'].sum()
            return weighted_sum / total_weight if total_weight > 0 else weighted_sum * 0

        # Apply the weighted average calculation for each group
        ensemble_df = df.groupby('time').apply(calculate_weighted_average).reset_index()
        ensemble_df['source'] = 'ensemble'

        # Combine the original data with the ensemble data
        final_df = pd.concat([df, ensemble_df], ignore_index=True)
        return final_df

class EnsembleFactory:
    @staticmethod
    def get_ensemble_strategy(strategy_type: str, *args, **kwargs) -> EnsembleStrategy:
        if strategy_type == "simple_average":
            return SimpleAverageEnsemble()
        elif strategy_type == "weighted_average":
            return WeightedAverageEnsemble()
        # elif strategy_type == "linear_regression":
        #     return LinearRegressionEnsemble(*args, **kwargs)
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

