# Training Notebooks

## ⚠️ Important: API Keys Required

The training notebooks require a Roboflow API key. For security reasons, the notebooks with API keys are not included in this repository.

## 🔑 Setup Instructions

1. **Get your Roboflow API key:**
   - Sign up at [Roboflow](https://roboflow.com/)
   - Go to your account settings
   - Copy your API key

2. **Create a config file:**
   ```python
   # Create roboflow_config.py in this directory
   ROBOFLOW_API_KEY = "your_api_key_here"
   ```

3. **Use in notebooks:**
   ```python
   from roboflow_config import ROBOFLOW_API_KEY
   from roboflow import Roboflow
   
   rf = Roboflow(api_key=ROBOFLOW_API_KEY)
   ```

## 📓 Available Notebooks

### 1. Basketball Player Detection Training
**File:** `basketball_player_detection_training.ipynb`

Trains a YOLO v11 model to detect basketball players.

**Dataset:** Basketball player detection dataset from Roboflow
**Model:** YOLOv11
**Output:** `basketball_player_model.pt`

### 2. Basketball Ball Training
**File:** `basketball_ball_training.ipynb`

Trains a YOLO v5 model to detect basketballs with motion blur augmentation.

**Dataset:** Basketball ball detection dataset from Roboflow
**Model:** YOLOv5
**Output:** `basketball_ball_detection.pt`

### 3. Basketball Court Keypoint Training
**File:** `basketball_court_keypoint_training.ipynb`

Trains a YOLO v8 model to detect court keypoints (lines, corners, zones).

**Dataset:** Basketball court keypoint dataset from Roboflow
**Model:** YOLOv8
**Output:** `court_keypoint_detector.pt`

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   pip install roboflow ultralytics
   ```

2. Create your config file with API key (see above)

3. Open notebook in Jupyter or Google Colab

4. Run all cells

5. Download trained model from the output

## 📦 Pre-trained Models

Don't want to train? Download pre-trained models:

- [Player Detector](https://drive.google.com/file/d/1fVBLZtPy9Yu6Tf186oS4siotkioHBLHy/view?usp=sharing)
- [Ball Detector](https://drive.google.com/file/d/1KejdrcEnto2AKjdgdo1U1syr5gODp6EL/view?usp=sharing)
- [Court Keypoint Detector](https://drive.google.com/file/d/1nGoG-pUkSg4bWAUIeQ8aN6n7O1fOkXU0/view?usp=sharing)

Place them in the `models/` directory.

## 🔒 Security Notes

- **Never commit API keys** to version control
- Use environment variables or config files (added to .gitignore)
- The `roboflow_config.py` file is automatically ignored by git
- Notebooks with API keys are excluded from the repository

## 📚 Resources

- [Roboflow Documentation](https://docs.roboflow.com/)
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [YOLO Training Guide](https://docs.ultralytics.com/modes/train/)

## 🤝 Contributing

If you create improved training notebooks:
1. Remove all API keys before committing
2. Use config file imports instead
3. Document any dataset changes
4. Include training metrics and results
