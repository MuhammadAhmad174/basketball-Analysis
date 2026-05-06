"""
Example Usage of Game Analysis Pipeline

This script demonstrates how to use the game analysis modules programmatically.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_analysis.data_loader import DataLoader
from game_analysis.eda_analyzer import EDAAnalyzer
from game_analysis.feature_engineer import FeatureEngineer
from game_analysis.predictive_models import PredictiveModels
from game_analysis.visualizer import GameVisualizer


def example_basic_analysis():
    """Example: Basic analysis workflow."""
    print("="*60)
    print("EXAMPLE 1: Basic Analysis")
    print("="*60)
    
    # Load data
    loader = DataLoader('csv_output/video_2.csv')
    df = loader.load_combined_csv()
    
    # Run EDA
    eda = EDAAnalyzer(df)
    possession_stats = eda.analyze_possession()
    player_stats = eda.analyze_player_performance()
    
    print("\nTop 3 players by distance:")
    print(player_stats.head(3))


def example_feature_engineering():
    """Example: Feature engineering workflow."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Feature Engineering")
    print("="*60)
    
    # Load data
    loader = DataLoader('csv_output/video_2.csv')
    df = loader.load_combined_csv()
    
    # Engineer features
    engineer = FeatureEngineer(df)
    df_engineered = engineer.create_all_features()
    
    print(f"\nOriginal columns: {len(df.columns)}")
    print(f"After engineering: {len(df_engineered.columns)}")
    print(f"\nNew features: {set(df_engineered.columns) - set(df.columns)}")


def example_predictive_modeling():
    """Example: Predictive modeling workflow."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Predictive Modeling")
    print("="*60)
    
    # Load and engineer features
    loader = DataLoader('csv_output/video_2.csv')
    df = loader.load_combined_csv()
    
    engineer = FeatureEngineer(df)
    df_engineered = engineer.create_all_features()
    
    # Train models
    models = PredictiveModels(df_engineered)
    
    # Possession predictor
    possession_results = models.train_possession_predictor()
    print(f"\nPossession Predictor Accuracy: {possession_results['accuracy']:.4f}")
    
    # Player performance classification
    player_performance = models.predict_player_performance_category()
    print("\nPlayer Performance Categories:")
    print(player_performance)


def example_visualization():
    """Example: Visualization workflow."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Visualizations")
    print("="*60)
    
    # Load data
    loader = DataLoader('csv_output/video_2.csv')
    df = loader.load_combined_csv()
    
    # Create visualizer
    visualizer = GameVisualizer(df, output_dir='game_analysis/example_viz')
    
    # Create specific visualizations
    visualizer.plot_possession_pie()
    visualizer.plot_speed_distribution()
    visualizer.plot_player_comparison()
    
    print("\nVisualizations saved to: game_analysis/example_viz/")


def example_custom_analysis():
    """Example: Custom analysis."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Analysis")
    print("="*60)
    
    # Load data
    loader = DataLoader('csv_output/video_2.csv')
    df = loader.load_combined_csv()
    
    # Custom analysis: Find fastest sprint
    fastest_sprint = df.loc[df['speed_speed_kmh'].idxmax()]
    print(f"\nFastest sprint:")
    print(f"  Player: {fastest_sprint['player_id']}")
    print(f"  Speed: {fastest_sprint['speed_speed_kmh']:.2f} km/h")
    print(f"  Time: {fastest_sprint['timestamp']:.2f} seconds")
    
    # Custom analysis: Most active player
    player_activity = df.groupby('player_id').agg({
        'speed_speed_kmh': 'mean',
        'distance_cumulative_distance_meters': 'max'
    })
    player_activity['activity_score'] = (
        player_activity['speed_speed_kmh'] * 0.5 +
        player_activity['distance_cumulative_distance_meters'] * 0.5
    )
    most_active = player_activity['activity_score'].idxmax()
    
    print(f"\nMost active player: {most_active}")
    print(player_activity.loc[most_active])


if __name__ == '__main__':
    # Check if CSV file exists
    if not os.path.exists('csv_output/video_2.csv'):
        print("Error: CSV file not found!")
        print("Please run video analysis first:")
        print("  python main.py input_videos/video_2.mp4 --export_csv")
        sys.exit(1)
    
    # Run examples
    try:
        example_basic_analysis()
        example_feature_engineering()
        example_predictive_modeling()
        example_visualization()
        example_custom_analysis()
        
        print("\n" + "="*60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
