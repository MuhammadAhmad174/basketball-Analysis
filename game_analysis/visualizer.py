"""
Game Visualizer

Creates visualizations for basketball game analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional
import os


class GameVisualizer:
    """Creates visualizations for basketball game data."""
    
    def __init__(self, df: pd.DataFrame, output_dir: str = 'game_analysis/visualizations'):
        """
        Initialize visualizer.
        
        Args:
            df: DataFrame with game data
            output_dir: Directory to save visualizations
        """
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style('whitegrid')
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def plot_possession_timeline(self, save: bool = True) -> None:
        """
        Plot possession over time.
        
        Args:
            save: Whether to save the plot
        """
        print("Creating possession timeline...")
        
        possession_by_frame = self.df.groupby('frame_number').agg({
            'has_possession': 'any',
            'team_id': lambda x: x[self.df.loc[x.index, 'has_possession']].mode()[0] if any(self.df.loc[x.index, 'has_possession']) else -1,
            'timestamp': 'first'
        })
        
        plt.figure(figsize=(14, 6))
        
        for team_id in [1, 2]:
            team_possession = possession_by_frame[possession_by_frame['team_id'] == team_id]
            plt.scatter(team_possession['timestamp'], [team_id] * len(team_possession),
                       label=f'Team {team_id}', alpha=0.6, s=10)
        
        plt.xlabel('Time (seconds)')
        plt.ylabel('Team')
        plt.title('Ball Possession Timeline')
        plt.legend()
        plt.yticks([1, 2])
        plt.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(self.output_dir, 'possession_timeline.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved to {filepath}")
        
        plt.close()
    
    def plot_player_heatmap(self, player_id: int, save: bool = True) -> None:
        """
        Plot player movement heatmap.
        
        Args:
            player_id: Player ID to visualize
            save: Whether to save the plot
        """
        print(f"Creating heatmap for player {player_id}...")
        
        player_data = self.df[self.df['player_id'] == player_id]
        
        if len(player_data) == 0:
            print(f"No data for player {player_id}")
            return
        
        plt.figure(figsize=(12, 8))
        
        # Create 2D histogram
        plt.hist2d(
            player_data['tactical_court_x_meters'].dropna(),
            player_data['tactical_court_y_meters'].dropna(),
            bins=30,
            cmap='hot'
        )
        
        plt.colorbar(label='Frequency')
        plt.xlabel('Court X (meters)')
        plt.ylabel('Court Y (meters)')
        plt.title(f'Player {player_id} Movement Heatmap')
        plt.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(self.output_dir, f'player_{player_id}_heatmap.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved to {filepath}")
        
        plt.close()
    
    def plot_speed_distribution(self, save: bool = True) -> None:
        """
        Plot speed distribution across all players.
        
        Args:
            save: Whether to save the plot
        """
        print("Creating speed distribution plot...")
        
        plt.figure(figsize=(12, 6))
        
        speed_data = self.df['speed_speed_kmh'].dropna()
        
        plt.hist(speed_data, bins=50, edgecolor='black', alpha=0.7)
        plt.axvline(speed_data.mean(), color='red', linestyle='--', label=f'Mean: {speed_data.mean():.2f} km/h')
        plt.axvline(speed_data.median(), color='green', linestyle='--', label=f'Median: {speed_data.median():.2f} km/h')
        
        plt.xlabel('Speed (km/h)')
        plt.ylabel('Frequency')
        plt.title('Player Speed Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(self.output_dir, 'speed_distribution.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved to {filepath}")
        
        plt.close()
    
    def plot_player_comparison(self, save: bool = True) -> None:
        """
        Compare player performance metrics.
        
        Args:
            save: Whether to save the plot
        """
        print("Creating player comparison plot...")
        
        player_stats = self.df.groupby('player_id').agg({
            'speed_speed_kmh': 'mean',
            'distance_cumulative_distance_meters': 'max',
            'has_possession': 'sum'
        }).round(2)
        
        player_stats.columns = ['Avg Speed (km/h)', 'Total Distance (m)', 'Possession Count']
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        for idx, col in enumerate(player_stats.columns):
            player_stats[col].sort_values(ascending=False).plot(kind='bar', ax=axes[idx])
            axes[idx].set_title(col)
            axes[idx].set_xlabel('Player ID')
            axes[idx].set_ylabel(col)
            axes[idx].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, 'player_comparison.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved to {filepath}")
        
        plt.close()
    
    def plot_possession_pie(self, save: bool = True) -> None:
        """
        Plot possession percentage pie chart.
        
        Args:
            save: Whether to save the plot
        """
        print("Creating possession pie chart...")
        
        possession_frames = self.df[self.df['has_possession'] == True]
        team_possession = possession_frames.groupby('team_id').size()
        
        plt.figure(figsize=(8, 8))
        
        colors = ['#FF6B6B', '#4ECDC4']
        plt.pie(team_possession, labels=[f'Team {tid}' for tid in team_possession.index],
               autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Ball Possession Distribution')
        
        if save:
            filepath = os.path.join(self.output_dir, 'possession_pie.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved to {filepath}")
        
        plt.close()
    
    def plot_distance_over_time(self, player_ids: Optional[list] = None, save: bool = True) -> None:
        """
        Plot cumulative distance over time for players.
        
        Args:
            player_ids: List of player IDs to plot (None = all players)
            save: Whether to save the plot
        """
        print("Creating distance over time plot...")
        
        plt.figure(figsize=(14, 6))
        
        if player_ids is None:
            player_ids = self.df['player_id'].unique()[:5]  # Plot first 5 players
        
        for player_id in player_ids:
            player_data = self.df[self.df['player_id'] == player_id]
            plt.plot(player_data['timestamp'], 
                    player_data['distance_cumulative_distance_meters'],
                    label=f'Player {player_id}', alpha=0.7)
        
        plt.xlabel('Time (seconds)')
        plt.ylabel('Cumulative Distance (meters)')
        plt.title('Player Distance Traveled Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save:
            filepath = os.path.join(self.output_dir, 'distance_over_time.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved to {filepath}")
        
        plt.close()
    
    def plot_feature_importance(self, feature_importance: pd.DataFrame, 
                               title: str = 'Feature Importance', save: bool = True) -> None:
        """
        Plot feature importance from model.
        
        Args:
            feature_importance: DataFrame with feature importance
            title: Plot title
            save: Whether to save the plot
        """
        print(f"Creating {title} plot...")
        
        plt.figure(figsize=(10, 6))
        
        top_features = feature_importance.head(10)
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importance')
        plt.title(title)
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3)
        
        if save:
            filename = title.lower().replace(' ', '_') + '.png'
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved to {filepath}")
        
        plt.close()
    
    def create_all_visualizations(self) -> None:
        """Create all standard visualizations."""
        print("\n=== Creating All Visualizations ===")
        
        self.plot_possession_timeline()
        self.plot_speed_distribution()
        self.plot_player_comparison()
        self.plot_possession_pie()
        self.plot_distance_over_time()
        
        # Create heatmaps for first 3 players
        for player_id in self.df['player_id'].unique()[:3]:
            self.plot_player_heatmap(player_id)
        
        print(f"\nAll visualizations saved to: {self.output_dir}")
