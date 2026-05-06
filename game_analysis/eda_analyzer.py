"""
Exploratory Data Analysis (EDA) Analyzer

Performs statistical analysis and generates insights from basketball data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class EDAAnalyzer:
    """Performs exploratory data analysis on basketball game data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize EDA analyzer.
        
        Args:
            df: DataFrame with game data
        """
        self.df = df
        
    def analyze_possession(self) -> Dict[str, any]:
        """
        Analyze ball possession statistics.
        
        Returns:
            Dictionary with possession metrics
        """
        print("\n=== Possession Analysis ===")
        
        # Total possession by team
        possession_frames = self.df[self.df['has_possession'] == True]
        team_possession = possession_frames.groupby('team_id').size()
        
        total_frames = len(self.df['frame_number'].unique())
        
        results = {
            'total_frames': total_frames,
            'possession_frames': len(possession_frames),
            'team_possession_counts': team_possession.to_dict(),
            'team_possession_percentage': {}
        }
        
        # Calculate percentages
        for team_id, count in team_possession.items():
            pct = (count / len(possession_frames)) * 100
            results['team_possession_percentage'][team_id] = round(pct, 2)
            print(f"Team {team_id}: {count} frames ({pct:.2f}%)")
        
        # Possession changes
        possession_changes = (self.df['has_possession'] != self.df['has_possession'].shift()).sum()
        results['possession_changes'] = possession_changes
        print(f"Possession changes: {possession_changes}")
        
        return results
    
    def analyze_player_performance(self) -> pd.DataFrame:
        """
        Analyze individual player performance metrics.
        
        Returns:
            DataFrame with player statistics
        """
        print("\n=== Player Performance Analysis ===")
        
        player_stats = self.df.groupby('player_id').agg({
            'speed_speed_kmh': ['mean', 'max', 'std'],
            'distance_cumulative_distance_meters': 'max',
            'has_possession': 'sum',
            'frame_number': 'count'
        }).round(2)
        
        player_stats.columns = [
            'avg_speed_kmh', 'max_speed_kmh', 'speed_std',
            'total_distance_m', 'possession_count', 'frames_played'
        ]
        
        # Add team information
        player_teams = self.df.groupby('player_id')['team_id'].first()
        player_stats['team_id'] = player_teams
        
        # Sort by total distance
        player_stats = player_stats.sort_values('total_distance_m', ascending=False)
        
        print(player_stats)
        return player_stats
    
    def analyze_passes(self) -> Dict[str, any]:
        """
        Analyze passing statistics.
        
        Returns:
            Dictionary with pass metrics
        """
        print("\n=== Pass Analysis ===")
        
        pass_frames = self.df[self.df['is_pass_frame'] == True]
        
        if len(pass_frames) == 0:
            print("No passes detected in data")
            return {'total_passes': 0}
        
        results = {
            'total_passes': len(pass_frames),
            'passes_per_minute': len(pass_frames) / (self.df['timestamp'].max() / 60),
            'unique_passers': pass_frames['pass_passer_id'].nunique(),
            'unique_receivers': pass_frames['pass_receiver_id'].nunique()
        }
        
        print(f"Total passes: {results['total_passes']}")
        print(f"Passes per minute: {results['passes_per_minute']:.2f}")
        
        return results
    
    def analyze_interceptions(self) -> Dict[str, any]:
        """
        Analyze interception statistics.
        
        Returns:
            Dictionary with interception metrics
        """
        print("\n=== Interception Analysis ===")
        
        interception_frames = self.df[self.df['is_interception_frame'] == True]
        
        if len(interception_frames) == 0:
            print("No interceptions detected in data")
            return {'total_interceptions': 0}
        
        results = {
            'total_interceptions': len(interception_frames),
            'interceptions_per_minute': len(interception_frames) / (self.df['timestamp'].max() / 60),
            'interceptions_by_team': interception_frames.groupby('interception_team_id').size().to_dict()
        }
        
        print(f"Total interceptions: {results['total_interceptions']}")
        print(f"Interceptions per minute: {results['interceptions_per_minute']:.2f}")
        
        return results
    
    def analyze_court_zones(self) -> pd.DataFrame:
        """
        Analyze player positioning by court zones.
        
        Returns:
            DataFrame with zone statistics
        """
        print("\n=== Court Zone Analysis ===")
        
        # Define court zones based on tactical coordinates
        def classify_zone(row):
            x = row['tactical_court_x_meters']
            y = row['tactical_court_y_meters']
            
            if pd.isna(x) or pd.isna(y):
                return 'Unknown'
            
            # Simple zone classification (adjust based on court dimensions)
            if x < 9.33:  # Defensive third
                return 'Defensive'
            elif x < 18.66:  # Middle third
                return 'Midcourt'
            else:  # Offensive third
                return 'Offensive'
        
        self.df['court_zone'] = self.df.apply(classify_zone, axis=1)
        
        zone_stats = self.df.groupby(['player_id', 'court_zone']).size().unstack(fill_value=0)
        zone_stats['total_frames'] = zone_stats.sum(axis=1)
        
        # Calculate percentages
        for col in zone_stats.columns[:-1]:
            zone_stats[f'{col}_pct'] = (zone_stats[col] / zone_stats['total_frames'] * 100).round(2)
        
        print(zone_stats.head())
        return zone_stats
    
    def analyze_speed_distribution(self) -> Dict[str, any]:
        """
        Analyze speed distribution across players.
        
        Returns:
            Dictionary with speed statistics
        """
        print("\n=== Speed Distribution Analysis ===")
        
        speed_data = self.df['speed_speed_kmh'].dropna()
        
        results = {
            'mean_speed': speed_data.mean(),
            'median_speed': speed_data.median(),
            'max_speed': speed_data.max(),
            'std_speed': speed_data.std(),
            'speed_ranges': {
                'stationary (0-2 km/h)': len(speed_data[speed_data < 2]),
                'walking (2-6 km/h)': len(speed_data[(speed_data >= 2) & (speed_data < 6)]),
                'jogging (6-12 km/h)': len(speed_data[(speed_data >= 6) & (speed_data < 12)]),
                'running (12-20 km/h)': len(speed_data[(speed_data >= 12) & (speed_data < 20)]),
                'sprinting (>20 km/h)': len(speed_data[speed_data >= 20])
            }
        }
        
        print(f"Mean speed: {results['mean_speed']:.2f} km/h")
        print(f"Max speed: {results['max_speed']:.2f} km/h")
        print("\nSpeed ranges:")
        for range_name, count in results['speed_ranges'].items():
            pct = (count / len(speed_data)) * 100
            print(f"  {range_name}: {count} ({pct:.1f}%)")
        
        return results
    
    def generate_summary_report(self) -> str:
        """
        Generate comprehensive summary report.
        
        Returns:
            String with formatted report
        """
        report = []
        report.append("="*60)
        report.append("BASKETBALL GAME ANALYSIS SUMMARY REPORT")
        report.append("="*60)
        
        # Basic info
        report.append(f"\nGame Duration: {self.df['timestamp'].max():.2f} seconds")
        report.append(f"Total Frames: {self.df['frame_number'].nunique()}")
        report.append(f"Total Players: {self.df['player_id'].nunique()}")
        
        # Possession
        possession = self.analyze_possession()
        report.append(f"\nPossession:")
        for team_id, pct in possession['team_possession_percentage'].items():
            report.append(f"  Team {team_id}: {pct}%")
        
        # Player performance
        player_stats = self.analyze_player_performance()
        report.append(f"\nTop 3 Players by Distance:")
        for idx, (player_id, row) in enumerate(player_stats.head(3).iterrows(), 1):
            report.append(f"  {idx}. Player {player_id}: {row['total_distance_m']:.2f}m")
        
        # Passes and interceptions
        passes = self.analyze_passes()
        interceptions = self.analyze_interceptions()
        report.append(f"\nPasses: {passes.get('total_passes', 0)}")
        report.append(f"Interceptions: {interceptions.get('total_interceptions', 0)}")
        
        report.append("\n" + "="*60)
        
        return "\n".join(report)
