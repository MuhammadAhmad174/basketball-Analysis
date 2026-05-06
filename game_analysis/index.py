"""
Basketball Game Analysis Pipeline

Complete data science pipeline for analyzing basketball game data.
Includes EDA, feature engineering, predictive modeling, and visualization.

Usage:
    python game_analysis/index.py --csv_path csv_output/video_2.csv
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_analysis.data_loader import DataLoader
from game_analysis.eda_analyzer import EDAAnalyzer
from game_analysis.feature_engineer import FeatureEngineer
from game_analysis.predictive_models import PredictiveModels
from game_analysis.visualizer import GameVisualizer


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Basketball Game Analysis Pipeline')
    parser.add_argument('--csv_path', type=str, required=True,
                       help='Path to combined CSV file')
    parser.add_argument('--output_dir', type=str, default='game_analysis/output',
                       help='Directory for output files')
    parser.add_argument('--skip_eda', action='store_true',
                       help='Skip exploratory data analysis')
    parser.add_argument('--skip_modeling', action='store_true',
                       help='Skip predictive modeling')
    parser.add_argument('--skip_viz', action='store_true',
                       help='Skip visualizations')
    parser.add_argument('--save_models', action='store_true',
                       help='Save trained models to disk')
    return parser.parse_args()


def main():
    """Run complete analysis pipeline."""
    args = parse_args()
    
    print("="*70)
    print("BASKETBALL GAME ANALYSIS PIPELINE")
    print("="*70)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Step 1: Load Data
    print("\n" + "="*70)
    print("STEP 1: DATA LOADING")
    print("="*70)
    
    loader = DataLoader(args.csv_path)
    df = loader.load_combined_csv()
    loader.validate_data()
    
    # Step 2: Exploratory Data Analysis
    if not args.skip_eda:
        print("\n" + "="*70)
        print("STEP 2: EXPLORATORY DATA ANALYSIS")
        print("="*70)
        
        eda = EDAAnalyzer(df)
        
        # Run analyses
        possession_stats = eda.analyze_possession()
        player_stats = eda.analyze_player_performance()
        pass_stats = eda.analyze_passes()
        interception_stats = eda.analyze_interceptions()
        speed_stats = eda.analyze_speed_distribution()
        
        # Generate summary report
        report = eda.generate_summary_report()
        print("\n" + report)
        
        # Save report
        report_path = os.path.join(args.output_dir, 'analysis_report.txt')
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {report_path}")
        
        # Save player stats
        player_stats_path = os.path.join(args.output_dir, 'player_statistics.csv')
        player_stats.to_csv(player_stats_path)
        print(f"Player stats saved to: {player_stats_path}")
    
    # Step 3: Feature Engineering
    print("\n" + "="*70)
    print("STEP 3: FEATURE ENGINEERING")
    print("="*70)
    
    engineer = FeatureEngineer(df)
    df_engineered = engineer.create_all_features()
    
    # Step 4: Predictive Modeling
    if not args.skip_modeling:
        print("\n" + "="*70)
        print("STEP 4: PREDICTIVE MODELING")
        print("="*70)
        
        models = PredictiveModels(df_engineered)
        
        # Train possession predictor
        possession_results = models.train_possession_predictor()
        
        # Train pass predictor
        pass_results = models.train_pass_predictor(lookahead_frames=30)
        
        # Player performance classification
        player_performance = models.predict_player_performance_category()
        
        # Merge player performance back into main dataframe
        df_engineered = df_engineered.merge(
            player_performance[['player_id', 'performance_category']], 
            on='player_id', 
            how='left'
        )
        
        # Save models if requested
        if args.save_models:
            models_dir = os.path.join(args.output_dir, 'models')
            models.save_models(models_dir)
    
    # Save complete results to single CSV
    complete_csv_path = os.path.join(args.output_dir, 'complete_results.csv')
    df_engineered.to_csv(complete_csv_path, index=False)
    print(f"\n✅ Complete results saved to: {complete_csv_path}")
    print(f"   Total rows: {len(df_engineered)}")
    print(f"   Total columns: {len(df_engineered.columns)}")
    
    # Step 5: Visualizations
    if not args.skip_viz:
        print("\n" + "="*70)
        print("STEP 5: VISUALIZATIONS")
        print("="*70)
        
        viz_dir = os.path.join(args.output_dir, 'visualizations')
        visualizer = GameVisualizer(df_engineered, output_dir=viz_dir)
        
        # Create all visualizations
        visualizer.create_all_visualizations()
        
        # Plot feature importance if models were trained
        if not args.skip_modeling and 'possession' in models.feature_importance:
            visualizer.plot_feature_importance(
                models.feature_importance['possession'],
                title='Possession Prediction - Feature Importance'
            )
        
        if not args.skip_modeling and 'pass' in models.feature_importance:
            visualizer.plot_feature_importance(
                models.feature_importance['pass'],
                title='Pass Prediction - Feature Importance'
            )
    
    # Final Summary
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\nAll outputs saved to: {args.output_dir}")
    print("\n📁 Generated files:")
    print(f"  ✅ Complete Results CSV: {args.output_dir}/complete_results.csv")
    print(f"  ✅ Analysis Report: {args.output_dir}/analysis_report.txt")
    print(f"  ✅ Player Statistics: {args.output_dir}/player_statistics.csv")
    if not args.skip_modeling and args.save_models:
        print(f"  ✅ Trained Models: {args.output_dir}/models/")
    if not args.skip_viz:
        print(f"  ✅ Visualizations: {args.output_dir}/visualizations/")
    print("\n" + "="*70)


if __name__ == '__main__':
    main()
