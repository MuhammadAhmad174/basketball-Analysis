"""
Data Loader

Loads and validates CSV data from basketball analysis.
"""

import pandas as pd
import os
from typing import Dict, Optional


class DataLoader:
    """Loads basketball analysis CSV data."""
    
    def __init__(self, csv_path: str):
        """
        Initialize data loader.
        
        Args:
            csv_path: Path to combined CSV file or directory with separate CSVs
        """
        self.csv_path = csv_path
        self.df = None
        
    def load_combined_csv(self) -> pd.DataFrame:
        """
        Load combined CSV file.
        
        Returns:
            DataFrame with all game data
        """
        print(f"Loading data from: {self.csv_path}")
        
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        self.df = pd.read_csv(self.csv_path)
        
        print(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        print(f"Frames: {self.df['frame_number'].nunique()}")
        print(f"Players: {self.df['player_id'].nunique()}")
        print(f"Duration: {self.df['timestamp'].max():.2f} seconds")
        
        return self.df
    
    def load_separate_csvs(self, csv_dir: str) -> Dict[str, pd.DataFrame]:
        """
        Load separate CSV files.
        
        Args:
            csv_dir: Directory containing CSV files
            
        Returns:
            Dictionary mapping data type to DataFrame
        """
        print(f"Loading CSVs from directory: {csv_dir}")
        
        data = {}
        csv_files = {
            'player_tracks': 'player_tracks.csv',
            'ball_tracks': 'ball_tracks.csv',
            'possession': 'possession.csv',
            'passes': 'passes.csv',
            'interceptions': 'interceptions.csv',
            'tactical_positions': 'tactical_positions.csv',
            'speed_metrics': 'speed_metrics.csv',
            'distance_metrics': 'distance_metrics.csv'
        }
        
        for key, filename in csv_files.items():
            filepath = os.path.join(csv_dir, filename)
            if os.path.exists(filepath):
                data[key] = pd.read_csv(filepath)
                print(f"  Loaded {key}: {len(data[key])} rows")
            else:
                print(f"  Warning: {filename} not found")
        
        return data
    
    def validate_data(self) -> Dict[str, any]:
        """
        Validate loaded data.
        
        Returns:
            Dictionary with validation results
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_combined_csv() first.")
        
        validation = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum(),
            'frame_range': (self.df['frame_number'].min(), self.df['frame_number'].max()),
            'player_count': self.df['player_id'].nunique(),
            'team_ids': self.df['team_id'].unique().tolist(),
            'duration_seconds': self.df['timestamp'].max()
        }
        
        print("\n=== Data Validation ===")
        for key, value in validation.items():
            print(f"{key}: {value}")
        
        return validation
    
    def get_summary_stats(self) -> pd.DataFrame:
        """
        Get summary statistics for numerical columns.
        
        Returns:
            DataFrame with summary statistics
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_combined_csv() first.")
        
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        return self.df[numeric_cols].describe()
