# Pre-trained Models

## 📥 Download Required Models

The trained models are too large to include in the repository. Download them from the links below and place them in this directory.

### Required Models

| Model | Description | Size | Download Link |
|-------|-------------|------|---------------|
| `basketball_player_model.pt` | Player detection (YOLOv11) | ~50MB | [Download](https://drive.google.com/file/d/1fVBLZtPy9Yu6Tf186oS4siotkioHBLHy/view?usp=sharing) |
| `basketball_ball_detection.pt` | Ball detection (YOLOv5) | ~14MB | [Download](https://drive.google.com/file/d/1KejdrcEnto2AKjdgdo1U1syr5gODp6EL/view?usp=sharing) |
| `court_keypoint_detector.pt` | Court keypoint detection (YOLOv8) | ~6MB | [Download](https://drive.google.com/file/d/1nGoG-pUkSg4bWAUIeQ8aN6n7O1fOkXU0/view?usp=sharing) |

## 📂 Installation

1. Download all three model files from the links above
2. Place them in this `models/` directory
3. Verify the files are named correctly:
   ```
   models/
   ├── basketball_player_model.pt
   ├── basketball_ball_detection.pt
   └── court_keypoint_detector.pt
   ```

## ✅ Verification

Check if models are installed correctly:

```bash
# Windows
dir models\*.pt

# Linux/Mac
ls -lh models/*.pt
```

You should see all three `.pt` files.

## 🎓 Training Your Own Models

Want to train custom models? See the training notebooks in `training_notebooks/`:

- `basketball_player_detection_training.ipynb`
- `basketball_ball_training.ipynb`
- `basketball_court_keypoint_training.ipynb`

**Note:** Training requires:
- Roboflow API key
- GPU (recommended)
- Custom dataset (or use provided Roboflow datasets)

See [training_notebooks/README.md](../training_notebooks/README.md) for details.

## 📊 Model Performance

### Player Detection Model
- **Architecture:** YOLOv11
- **Input Size:** 640x640
- **mAP@0.5:** ~95%
- **Inference Speed:** ~30 FPS (GPU)

### Ball Detection Model
- **Architecture:** YOLOv5
- **Input Size:** 640x640
- **mAP@0.5:** ~90%
- **Special Features:** Motion blur augmentation
- **Inference Speed:** ~45 FPS (GPU)

### Court Keypoint Detection Model
- **Architecture:** YOLOv8
- **Input Size:** 640x640
- **Keypoints:** 14 court landmarks
- **Inference Speed:** ~40 FPS (GPU)

## 🔧 Model Configuration

Models are configured in `configs/configs.py`:

```python
PLAYER_DETECTOR_PATH = 'models/basketball_player_model.pt'
BALL_DETECTOR_PATH = 'models/basketball_ball_detection.pt'
COURT_KEYPOINT_DETECTOR_PATH = 'models/court_keypoint_detector.pt'
```

## 🐛 Troubleshooting

### "Model file not found"
- Ensure models are downloaded and placed in this directory
- Check file names match exactly (case-sensitive)
- Verify files are `.pt` format, not `.zip` or other

### "Model loading error"
- Ensure you have the correct PyTorch version installed
- Try re-downloading the model file
- Check if the file is corrupted (compare file size)

### "Out of memory"
- Models require ~2GB GPU memory
- Reduce batch size in processing
- Use CPU inference (slower but works)

## 📝 License

These pre-trained models are provided for research and educational purposes. 

If you use these models in your work, please cite:
```
Basketball Video Analysis with AI
https://github.com/MuhammadAhmad174/basketball-Analysis
```

## 🤝 Contributing

Trained better models? Share them!
1. Upload to Google Drive or similar
2. Create a pull request with updated links
3. Include performance metrics
4. Document training process

## 📧 Support

Issues with models?
- Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
- Open an issue on GitHub
- Verify file integrity and paths
