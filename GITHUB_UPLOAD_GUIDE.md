# 📤 GitHub Upload Guide

## Step-by-Step Instructions

### Step 1: Clean Up the Repository

Run the cleanup script:

```powershell
.\cleanup_for_github.ps1
```

This will:
- Remove extra documentation files
- Clean output directories
- Remove Python cache
- Create necessary empty directories with .gitkeep files

### Step 2: Initialize Git Repository

```bash
git init
```

### Step 3: Configure Git (if not already done)

```bash
git config user.name "Muhammad Ahmad"
git config user.email "your-email@example.com"
```

### Step 4: Add All Files

```bash
git add .
```

### Step 5: Create Initial Commit

```bash
git commit -m "🎉 Initial commit: Basketball Analysis with AI-powered game analytics

Features:
- Player and ball tracking with YOLO models
- Team assignment and possession detection
- Pass and interception detection
- Speed and distance metrics
- CSV data export
- AI-powered game analysis with ML models
- Comprehensive visualizations and reports
- 50+ engineered features
- Predictive models for possession and passes
- Player performance classification"
```

### Step 6: Add Remote Repository

```bash
git remote add origin https://github.com/MuhammadAhmad174/basketball-Analysis.git
```

### Step 7: Create Main Branch and Push

```bash
git branch -M main
git push -u origin main
```

## 🎨 Making Your Repository Beautiful

### 1. Add Repository Description

On GitHub, go to your repository and click "About" (gear icon):
- **Description**: "🏀 AI-powered basketball video analysis with player tracking, game analytics, and ML-based insights"
- **Website**: (if you have one)
- **Topics**: Add these tags:
  - `basketball`
  - `computer-vision`
  - `yolo`
  - `object-tracking`
  - `machine-learning`
  - `sports-analytics`
  - `data-science`
  - `python`
  - `opencv`
  - `deep-learning`

### 2. Enable GitHub Pages (Optional)

If you want to host documentation:
1. Go to Settings → Pages
2. Select source: Deploy from a branch
3. Select branch: main
4. Select folder: /docs (if you create one)

### 3. Add Repository Social Preview

1. Go to Settings
2. Scroll to "Social preview"
3. Upload an image (1280x640px recommended)
   - Use a screenshot of your analysis output
   - Or create a banner with your project name

### 4. Create GitHub Issues Templates

Create `.github/ISSUE_TEMPLATE/` folder with templates for:
- Bug reports
- Feature requests
- Questions

### 5. Add Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE.md`

## 📊 Repository Structure After Upload

```
basketball-Analysis/
├── .github/                         # GitHub specific files
│   └── workflows/                   # CI/CD workflows (optional)
├── ball_aquisition/                 # Ball possession detection
├── configs/                         # Configuration files
├── court_keypoint_detector/         # Court detection
├── csv_output/                      # Analysis results (empty)
├── drawers/                         # Visualization overlays
├── game_analysis/                   # AI analytics module
│   ├── data_loader.py
│   ├── eda_analyzer.py
│   ├── feature_engineer.py
│   ├── predictive_models.py
│   ├── visualizer.py
│   └── README.md
├── images/                          # Court images
├── input_videos/                    # Sample videos
├── models/                          # Pre-trained models
├── output_videos/                   # Annotated videos (empty)
├── pass_and_interception_detector/  # Pass detection
├── speed_and_distance_calculator/   # Metrics calculation
├── stubs/                           # Cached results (empty)
├── tactical_view_converter/         # Tactical view
├── team_assigner/                   # Team classification
├── trackers/                        # Player/ball trackers
├── training_notebooks/              # Model training
├── utils/                           # Utility functions
├── .gitignore                       # Git ignore rules
├── CHANGELOG.md                     # Version history
├── Dockerfile                       # Docker configuration
├── INTEGRATION_GUIDE.md             # Integration docs
├── LICENSE                          # MIT License
├── main.py                          # Main entry point
├── OUTPUT_STRUCTURE.md              # Output documentation
├── QUICKSTART.md                    # Quick start guide
├── README.md                        # Main documentation
├── requirements.txt                 # Python dependencies
└── TROUBLESHOOTING.md               # Troubleshooting guide
```

## 🔒 Important: Don't Upload These

Make sure `.gitignore` excludes:
- `__pycache__/`
- `*.pyc`
- `*.pt` (model files - too large, provide download links instead)
- `*.pkl` (stub files)
- `output_videos/*.avi`
- `csv_output/*/`
- `*.mp4` (video files - too large)

## 📝 After Upload Checklist

- [ ] Repository is public
- [ ] README.md displays correctly
- [ ] Description and topics are added
- [ ] License is visible
- [ ] All documentation files are accessible
- [ ] .gitignore is working correctly
- [ ] No sensitive data is uploaded
- [ ] Model download links work
- [ ] Demo video link works

## 🎯 Optional Enhancements

### Add GitHub Actions for CI/CD

Create `.github/workflows/python-app.yml`:

```yaml
name: Python Application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Add Badges to README

Already included in the README:
- Python version
- License
- Build status (if you add CI/CD)

### Create a CONTRIBUTING.md

Guidelines for contributors.

### Add a CODE_OF_CONDUCT.md

Community guidelines.

## 🚀 Promoting Your Repository

1. **Share on social media** with hashtags:
   - #basketball #AI #computervision #machinelearning #python

2. **Post on Reddit**:
   - r/MachineLearning
   - r/computervision
   - r/basketball
   - r/Python

3. **Share on LinkedIn** with a demo video

4. **Write a blog post** explaining the project

5. **Submit to awesome lists**:
   - awesome-computer-vision
   - awesome-sports-analytics

## 📧 Need Help?

If you encounter any issues:
1. Check the error message
2. Review the TROUBLESHOOTING.md
3. Search existing GitHub issues
4. Create a new issue with details

---

**Good luck with your repository! 🎉**
