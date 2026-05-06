# Training Notebook Template

### Method 1: Config File

Create `roboflow_config.py`:
```python
# roboflow_config.py (this file is in .gitignore)
ROBOFLOW_API_KEY = "your_api_key_here"
```

Use in notebook:
```python
from roboflow_config import ROBOFLOW_API_KEY
from roboflow import Roboflow

rf = Roboflow(api_key=ROBOFLOW_API_KEY)
```

### Method 2: Environment Variables

Set environment variable:
```bash
export ROBOFLOW_API_KEY="your_api_key_here"
```

Use in notebook:
```python
import os
from roboflow import Roboflow

api_key = os.getenv('ROBOFLOW_API_KEY')
rf = Roboflow(api_key=api_key)
```

### Method 3: Input Prompt (for Colab)

```python
from getpass import getpass
from roboflow import Roboflow

api_key = getpass('Enter your Roboflow API key: ')
rf = Roboflow(api_key=api_key)
```

## Example Training Notebook Structure

```python
# 1. Install dependencies
!pip install roboflow ultralytics

# 2. Import libraries
from roboflow import Roboflow
from ultralytics import YOLO
from roboflow_config import ROBOFLOW_API_KEY  # Safe import

# 3. Initialize Roboflow
rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace("your-workspace").project("your-project")
dataset = project.version(1).download("yolov8")

# 4. Train model
model = YOLO('yolov8n.pt')
results = model.train(
    data=f"{dataset.location}/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16
)

# 5. Export model
model.export(format='pt')
```

## ⚠️ Before Committing

**Checklist:**
- [ ] Remove all hardcoded API keys
- [ ] Use config file or environment variables
- [ ] Add config file to .gitignore
- [ ] Test notebook works with config import
- [ ] Document any dataset requirements
- [ ] Include training results/metrics


