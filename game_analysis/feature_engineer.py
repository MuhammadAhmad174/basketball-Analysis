"""
Feature Engineering

Creates derived features for machine learning models.
"""

import pandas as pd
import numpy as np
from typing import List


class FeatureEngineer:
    """Engineers features from basketball game data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize feature engineer.
        
        Args:
            df: DataFrame with game data
        """
        self.df = df.copy()
        
    def create_temporal_features(self) -> pd.DataFrame:
        """
        Create time-based features.
        
        Returns:
            DataFrame with temporal features added
        """
        print("Creating temporal features...")
        
        # Time-based features
        self.df['game_minute'] = (self.df['timestamp'] / 60).astype(int)
        self.df['game_quarter'] = (self.df['game_minute'] / 10).astype(int) + 1  # Assuming 10-min quarters
        
        # Rolling windows for speed
        self.df['speed_rolling_mean_5'] = self.df.groupby('player_id')['speed_speed_kmh'].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )
        
        self.df['speed_rolling_max_10'] = self.df.groupby('player_id')['speed_speed_kmh'].transform(
            lambda x: x.rolling(window=10, min_periods=1).max()
        )
        
        return self.df
    
    def create_possession_features(self) -> pd.DataFrame:
        """
        Create possession-related features.
        
        Returns:
            DataFrame with possession features added
        """
        print("Creating possession features...")
        
        # Possession duration
        self.df['possession_duration'] = self.df.groupby(
            (self.df['has_possession'] != self.df['has_possession'].shift()).cumsum()
        ).cumcount()
        
        # Time since last possession
        self.df['frames_since_possession'] = 0
        for player_id in self.df['player_id'].unique():
            player_mask = self.df['player_id'] == player_id
            possession_mask = player_mask & (self.df['has_possession'] == True)
            
            if possession_mask.any():
                last_possession_idx = self.df[possession_mask].index
                for idx in last_possession_idx:
                    future_mask = player_mask & (self.df.index > idx)
                    self.df.loc[future_mask, 'frames_since_possession'] = self.df.loc[future_mask].index - idx
        
        return self.df
    
    def create_spatial_features(self) -> pd.DataFrame:
        """
        Create position-based features.
        
        Returns:
            DataFrame with spatial features added
        """
        print("Creating spatial features...")
        
        # Distance from basket (assuming basket at x=28, y=7.5)
        basket_x, basket_y = 28.0, 7.5
        self.df['distance_to_basket'] = np.sqrt(
            (self.df['tactical_court_x_meters'] - basket_x)**2 + 
            (self.df['tactical_court_y_meters'] - basket_y)**2
        )
        
        # Court zone classification
        def classify_zone(x, y):
            if pd.isna(x) or pd.isna(y):
                return 'Unknown'
            
            # Paint zone (close to basket)
            if x > 22 and abs(y - 7.5) < 3:
                return 'Paint'
            # Three-point zone
            elif np.sqrt((x - basket_x)**2 + (y - basket_y)**2) > 6.75:
                return 'Three_Point'
            # Mid-range
            else:
                return 'Mid_Range'
        
        self.df['court_zone'] = self.df.apply(
            lambda row: classify_zone(row['tactical_court_x_meters'], row['tactical_court_y_meters']),
            axis=1
        )
        
        # Distance traveled per frame
        self.df['distance_per_frame'] = self.df.groupby('player_id')['distance_distance_meters'].diff().fillna(0)
        
        return self.df
    
    def create_interaction_features(self) -> pd.DataFrame:
        """
        Create features based on player interactions.
        
        Returns:
            DataFrame with interaction features added
        """
        print("Creating interaction features...")
        
        # Team possession indicator
        self.df['team_has_possession'] = self.df.groupby(['frame_number', 'team_id'])['has_possession'].transform('any')
        
        # Number of teammates nearby (simplified - same frame, same team)
        self.df['teammates_count'] = self.df.groupby(['frame_number', 'team_id'])['player_id'].transform('count') - 1
        
        # Speed relative to team average
        self.df['speed_vs_team_avg'] = self.df.groupby(['frame_number', 'team_id'])['speed_speed_kmh'].transform(
            lambda x: x - x.mean()
        )
        
        return self.df
    
    def create_performance_features(self) -> pd.DataFrame:
        """
        Create performance-based features.
        
        Returns:
            DataFrame with performance features added
        """
        print("Creating performance features...")
        
        # Acceleration (change in speed)
        self.df['acceleration'] = self.df.groupby('player_id')['speed_speed_kmh'].diff().fillna(0)
        
        # Cumulative stats per player
        self.df['cumulative_possessions'] = self.df.groupby('player_id')['has_possession'].cumsum()
        
        # Activity level (based on speed)
        self.df['activity_level'] = pd.cut(
            self.df['speed_speed_kmh'],
            bins=[-np.inf, 2, 6, 12, 20, np.inf],
            labels=['Stationary', 'Walking', 'Jogging', 'Running', 'Sprinting']
        )
        
        return self.df
    
    def create_all_features(self) -> pd.DataFrame:
        """
        Create all engineered features.
        
        Returns:
            DataFrame with all features added
        """
        print("\n=== Feature Engineering ===")
        
        self.create_temporal_features()
        self.create_possession_features()
        self.create_spatial_features()
        self.create_interaction_features()
        self.create_performance_features()
        
        print(f"Total features: {len(self.df.columns)}")
        print(f"New features created: {len(self.df.columns) - len(self.df.columns)}")
        
        return self.df
    
    def get_feature_importance_data(self) -> pd.DataFrame:
        """
        Prepare data for feature importance analysis.
        
        Returns:
            DataFrame with selected features for modeling
        """
        feature_cols = [
            'speed_speed_kmh', 'speed_rolling_mean_5', 'speed_rolling_max_10',
            'distance_to_basket', 'distance_per_frame',
            'possession_duration', 'frames_since_possession',
            'teammates_count', 'speed_vs_team_avg', 'acceleration',
            'cumulative_possessions'
        ]
        
        # Filter to existing columns
        available_cols = [col for col in feature_cols if col in self.df.columns]
        
        return self.df[available_cols + ['has_possession', 'player_id', 'team_id']].dropna()
