# 🏀 Basketball Video Analysis with AI

<div align="center">

![Basketball Analysis](https://img.shields.io/badge/Basketball-Analysis-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![YOLO](https://img.shields.io/badge/YOLO-v8-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Advanced AI-powered basketball video analysis with player tracking, team assignment, and comprehensive game analytics**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## 🎯 Overview

A complete basketball video analysis system that combines computer vision, machine learning, and data science to provide deep insights into game performance. From player tracking to predictive analytics, this tool transforms raw game footage into actionable intelligence.

## ✨ Features

### 🎥 Video Analysis
- **Player Detection & Tracking** - Real-time player identification and movement tracking
- **Ball Tracking** - Precise ball position tracking throughout the game
- **Court Keypoint Detection** - Automatic court boundary and zone detection
- **Team Assignment** - Intelligent jersey color-based team classification

### 📊 Game Analytics
- **Ball Possession Detection** - Track which player has the ball
- **Pass & Interception Detection** - Identify successful passes and interceptions
- **Speed & Distance Metrics** - Calculate player speed and distance traveled
- **Tactical View** - Top-down tactical visualization of player positions

### 🤖 AI-Powered Insights
- **CSV Data Export** - Export all tracking data for further analysis
- **Exploratory Data Analysis** - Comprehensive statistical analysis
- **Feature Engineering** - 50+ engineered features for ML models
- **Predictive Models** - ML models for possession and pass prediction
- **Performance Classification** - Automatic player performance categorization
- **Rich Visualizations** - Heatmaps, charts, and interactive plots

## 🎮 Demo

[![Basketball Analysis Demo](https://img.youtube.com/vi/xWpP0LjEUng/0.jpg)](https://youtu.be/xWpP0LjEUng)

*Click to watch the demo video*

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended)
- 4GB+ RAM

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/MuhammadAhmad174/basketball-Analysis.git
cd basketball-Analysis
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download pre-trained models**

Place these models in the `models/` folder:
- [Player Detector](https://drive.google.com/file/d/1fVBLZtPy9Yu6Tf186oS4siotkioHBLHy/view?usp=sharing) → `basketball_player_model.pt`
- [Ball Detector](https://drive.google.com/file/d/1KejdrcEnto2AKjdgdo1U1syr5gODp6EL/view?usp=sharing) → `basketball_ball_detection.pt`
- [Court Keypoint Detector](https://drive.google.com/file/d/1nGoG-pUkSg4bWAUIeQ8aN6n7O1fOkXU0/view?usp=sharing) → `court_keypoint_detector.pt`

### Basic Usage

```bash
# Basic video analysis
python main.py input_videos/game.mp4

# With CSV export
python main.py input_videos/game.mp4 --export_csv

# Complete pipeline with AI analytics
python main.py input_videos/game.mp4 --export_csv --run_analysis
```

## 📖 Usage Guide

### 1️⃣ Video Analysis Only

Process video and generate annotated output:

```bash
python main.py input_videos/game.mp4 --output_video output_videos/result.avi
```

**Output:** Annotated video with player tracking, ball tracking, and game statistics

### 2️⃣ Data Export

Export all tracking data to CSV:

```bash
python main.py input_videos/game.mp4 --export_csv
```

**Output:** `csv_output/game/game_complete_analysis.csv`

### 3️⃣ Complete AI Analysis

Run full pipeline with machine learning analytics:

```bash
python main.py input_videos/game.mp4 --export_csv --run_analysis
```

**Output:**
```
csv_output/game/
├── game_complete_analysis.csv      # Raw tracking data
├── complete_results.csv            # All features + predictions
├── analysis_report.txt             # Statistical summary
├── player_statistics.csv           # Player performance stats
└── visualizations/                 # All charts and plots
    ├── possession_timeline.png
    ├── player_heatmaps.png
    ├── speed_distribution.png
    └── ...
```

### 4️⃣ Standalone Analytics

Analyze existing CSV data:

```bash
python game_analysis/index.py --csv_path csv_output/game/game_complete_analysis.csv
```

**Options:**
- `--skip_eda` - Skip exploratory data analysis
- `--skip_modeling` - Skip ML model training
- `--skip_viz` - Skip visualization generation
- `--save_models` - Save trained ML models

## 📊 Output Structure

```
csv_output/
└── game_name/
    ├── game_name_complete_analysis.csv    # Original tracking data
    ├── complete_results.csv               # ALL RESULTS (tracking + features + predictions)
    ├── analysis_report.txt                # Summary statistics
    ├── player_statistics.csv              # Player performance metrics
    ├── models/                            # Trained ML models (optional)
    │   ├── possession_rf.pkl
    │   └── pass_gb.pkl
    └── visualizations/                    # All visualizations
        ├── possession_timeline.png
        ├── player_heatmaps.png
        ├── speed_distribution.png
        └── feature_importance.png
```

## 🎯 Key Features Explained

### Player & Ball Tracking
- Uses YOLO models for real-time detection
- ByteTrack algorithm for consistent tracking
- Handles occlusions and fast movements

### Team Assignment
- Zero-shot classification based on jersey colors
- Automatic team identification
- Consistent across frames

### Game Analytics
- **Possession Analysis** - Who has the ball and for how long
- **Pass Detection** - Successful passes between teammates
- **Interception Detection** - Ball possession changes between teams
- **Speed Metrics** - Player speed in km/h
- **Distance Tracking** - Total distance traveled by each player

### AI Models
- **Possession Predictor** - Random Forest (85-95% accuracy)
- **Pass Predictor** - Gradient Boosting
- **Performance Classifier** - K-means clustering (Low/Medium/High tiers)

### Visualizations
- Possession timeline and pie charts
- Player movement heatmaps
- Speed distribution histograms
- Player comparison charts
- Distance over time plots
- Feature importance for ML models

## 🏗️ Project Structure

```
basketball-Analysis/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── configs/                         # Configuration files
├── trackers/                        # Player and ball trackers
├── drawers/                         # Visualization overlays
├── game_analysis/                   # AI analytics module
│   ├── data_loader.py              # Data loading
│   ├── eda_analyzer.py             # Statistical analysis
│   ├── feature_engineer.py         # Feature engineering
│   ├── predictive_models.py        # ML models
│   └── visualizer.py               # Chart generation
├── models/                          # Pre-trained models
├── input_videos/                    # Input videos
├── output_videos/                   # Annotated videos
└── csv_output/                      # Analysis results
```

## 🔧 Advanced Configuration

### Custom Output Directories

```bash
python main.py input_videos/game.mp4 \
  --output_video custom_output/result.avi \
  --csv_output_dir custom_csv \
  --export_csv \
  --run_analysis
```

### Batch Processing

```bash
# Process multiple videos
for video in input_videos/*.mp4; do
    python main.py "$video" --export_csv --run_analysis
done
```

### Using Stubs (Cached Results)

The system automatically caches detection results in `stubs/` for faster re-processing:

```bash
# First run (slow - processes everything)
python main.py input_videos/game.mp4 --export_csv

# Second run (fast - uses cached results)
python main.py input_videos/game.mp4 --export_csv --run_analysis
```

## 🎓 Training Your Own Models

Training notebooks are provided in `training_notebooks/`:

- `basketball_player_detection_training.ipynb` - Train player detector
- `basketball_ball_training.ipynb` - Train ball detector
- `basketball_court_keypoint_training.ipynb` - Train court keypoint detector

Uses Roboflow for dataset management and Ultralytics YOLO for training.

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide with examples
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Detailed integration documentation
- **[OUTPUT_STRUCTURE.md](OUTPUT_STRUCTURE.md)** - Output file structure
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[game_analysis/README.md](game_analysis/README.md)** - Analytics module documentation

## 🐳 Docker Support

```bash
# Build image
docker build -t basketball-analysis .

# Run container
docker run \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/csv_output:/app/csv_output \
  basketball-analysis \
  python main.py input_videos/game.mp4 --export_csv --run_analysis
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Roboflow** - Dataset management and preprocessing
- **Ultralytics** - YOLO models for object detection
- **ByteTrack** - Multi-object tracking algorithm
- **Hugging Face** - Zero-shot classification models

## 📧 Contact

**Muhammad Ahmad** - [@MuhammadAhmad174](https://github.com/MuhammadAhmad174)

Project Link: [https://github.com/MuhammadAhmad174/basketball-Analysis](https://github.com/MuhammadAhmad174/basketball-Analysis)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ for basketball analytics

</div>
