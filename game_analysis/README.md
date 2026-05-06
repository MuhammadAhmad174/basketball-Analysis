# Basketball Game Analysis Pipeline

Complete data science pipeline for analyzing basketball game data with exploratory data analysis, feature engineering, predictive modeling, and visualization.

## Features

### 1. **Data Loading & Validation**
- Load combined CSV files from video analysis
- Validate data integrity
- Generate summary statistics

### 2. **Exploratory Data Analysis (EDA)**
- Possession analysis by team
- Player performance metrics
- Pass and interception statistics
- Speed distribution analysis
- Court zone analysis

### 3. **Feature Engineering**
- Temporal features (rolling windows, game quarters)
- Possession features (duration, time since last possession)
- Spatial features (distance to basket, court zones)
- Interaction features (teammates nearby, team possession)
- Performance features (acceleration, activity levels)

### 4. **Predictive Modeling**
- **Possession Predictor**: Predicts which player will have ball possession
- **Pass Predictor**: Predicts if a pass will occur in next N frames
- **Player Performance Classification**: Categorizes players into performance tiers

### 5. **Visualizations**
- Possession timeline
- Player movement heatmaps
- Speed distribution histograms
- Player comparison charts
- Distance traveled over time
- Feature importance plots

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the complete analysis pipeline:

```bash
python game_analysis/index.py --csv_path csv_output/video_2.csv
```

### Advanced Options

```bash
python game_analysis/index.py \
  --csv_path csv_output/video_2.csv \
  --output_dir my_analysis \
  --save_models \
  --skip_viz
```

### Command-Line Arguments

- `--csv_path` (required): Path to combined CSV file from video analysis
- `--output_dir`: Directory for output files (default: `game_analysis/output`)
- `--skip_eda`: Skip exploratory data analysis
- `--skip_modeling`: Skip predictive modeling
- `--skip_viz`: Skip visualizations
- `--save_models`: Save trained models to disk

## Output Structure

```
game_analysis/output/
├── analysis_report.txt                    # Summary report
├── player_statistics.csv                  # Player performance stats
├── engineered_features.csv                # All engineered features
├── player_performance_categories.csv      # Player classifications
├── models/                                # Trained models (if --save_models)
│   ├── possession_rf.pkl
│   ├── pass_gb.pkl
│   ├── scaler_possession.pkl
│   └── scaler_pass.pkl
└── visualizations/                        # All plots
    ├── possession_timeline.png
    ├── speed_distribution.png
    ├── player_comparison.png
    ├── possession_pie.png
    ├── distance_over_time.png
    ├── player_1_heatmap.png
    ├── player_2_heatmap.png
    └── ...
```

## Module Structure

```
game_analysis/
├── __init__.py                 # Package initialization
├── index.py                    # Main pipeline script
├── data_loader.py              # Data loading and validation
├── eda_analyzer.py             # Exploratory data analysis
├── feature_engineer.py         # Feature engineering
├── predictive_models.py        # Machine learning models
├── visualizer.py               # Visualization generation
└── README.md                   # This file
```

## Example Workflow

### 1. Generate CSV from Video

First, run the video analysis with CSV export:

```bash
python main.py input_videos/game.mp4 --export_csv
```

This creates: `csv_output/game.csv`

### 2. Run Analysis Pipeline

```bash
python game_analysis/index.py --csv_path csv_output/game.csv --save_models
```

### 3. Review Results

Check the output directory for:
- **analysis_report.txt**: Quick summary of key metrics
- **player_statistics.csv**: Detailed player performance data
- **visualizations/**: All generated plots

## Predictive Models

### Possession Predictor

Predicts which player will have ball possession based on:
- Player speed and movement
- Distance to basket
- Team possession status
- Number of teammates nearby

**Performance**: Typically 85-95% accuracy

### Pass Predictor

Predicts if a pass will occur in the next 30 frames (1 second) based on:
- Current possession status
- Player positioning
- Possession duration
- Team dynamics

**Performance**: Varies based on pass frequency in game

### Player Performance Classifier

Classifies players into performance categories (Low/Medium/High) based on:
- Average speed
- Total distance traveled
- Possession count

## Customization

### Modify Features

Edit `feature_engineer.py` to add custom features:

```python
def create_custom_features(self) -> pd.DataFrame:
    # Add your custom features here
    self.df['my_feature'] = ...
    return self.df
```

### Add New Models

Edit `predictive_models.py` to add new predictive models:

```python
def train_my_custom_model(self):
    # Your model training code
    pass
```

### Create Custom Visualizations

Edit `visualizer.py` to add new plots:

```python
def plot_my_custom_viz(self, save: bool = True):
    # Your visualization code
    pass
```

## Performance Tips

1. **Large datasets**: Use `--skip_viz` to speed up analysis
2. **Quick exploration**: Use `--skip_modeling` for faster EDA
3. **Model development**: Use `--save_models` to avoid retraining

## Troubleshooting

### "No data loaded" error
- Ensure CSV file path is correct
- Check that CSV file was generated successfully from video analysis

### "Insufficient pass events" warning
- Normal if video has few passes
- Pass predictor will be skipped automatically

### Memory issues with large files
- Process shorter video segments
- Reduce frame skip in video analysis

## Example Analysis Results

### Sample Output

```
=== Possession Analysis ===
Team 1: 1250 frames (52.3%)
Team 2: 1140 frames (47.7%)
Possession changes: 45

=== Player Performance Analysis ===
Player 1: 245.3m traveled, avg speed 8.5 km/h
Player 2: 198.7m traveled, avg speed 7.2 km/h
...

=== Pass Analysis ===
Total passes: 23
Passes per minute: 4.6

=== Predictive Models ===
Possession Predictor Accuracy: 89.2%
Pass Predictor Accuracy: 76.5%
```

## Integration with Main Pipeline

The analysis pipeline is designed to work seamlessly with the video analysis:

```bash
# Step 1: Analyze video and export CSV
python main.py input_videos/game.mp4 --export_csv

# Step 2: Run data science pipeline
python game_analysis/index.py --csv_path csv_output/game.csv

# Step 3: Review results in game_analysis/output/
```

## Future Enhancements

Potential additions:
- Real-time prediction during video playback
- Team strategy analysis
- Shot prediction models
- Player fatigue detection
- Advanced clustering for play patterns

## Contributing

To add new features:
1. Create new methods in appropriate module
2. Update `index.py` to call new methods
3. Add tests and documentation
4. Update this README

## License

Same as main project license.
