# Installation & Setup Guide

## Current Status
✓ Python 3.14.2 is installed  
⏳ Installing core dependencies (OpenCV, NumPy, SciPy, Scikit-learn, Imutils)

## Installation Progress
The pip installer is currently downloading OpenCV (40.2 MB file, ~2 min remaining)

### What's being installed:
- **NumPy** ✓ (already installed)
- **SciPy** ✓ (already installed) 
- **Scikit-learn** ✓ (already installed)
- **OpenCV 4.13.0** ⏳ (downloading - ~40 MB)
- **Imutils** ⏳ (building from source)

## Next Steps (Once Installation Completes)

### 1. Verify Installation
```bash
python test_dependencies.py
```

### 2. Create Demo Data
```bash
python demo_setup.py
```
This generates synthetic frames and detections to test the tracking system without real fish data.

### 3. Run the Tracker on Demo Data
```bash
python deep_sort_app.py ^
  --sequence_dir demo_data/sequences/test_sequence ^
  --detection_file demo_data/sequences/detections.npy ^
  --output_file demo_output.txt ^
  --display False
```

### 4. Visualize Results
```bash
python show_results.py ^
  --sequence_dir demo_data/sequences/test_sequence ^
  --result_file demo_output.txt ^
  --video_filename demo_output.avi
```

## Optional: Install Heavy Dependencies

For full functionality with fish segmentation, you'll need:
```bash
# PyTorch (choose one based on your setup)
pip install torch torchvision torchaudio

# Detectron2 (requires PyTorch first)
pip install git+https://github.com/facebookresearch/detectron2.git

# TensorFlow (for feature extraction)
pip install tensorflow==2.13.0

# Django (for web interface - optional)
pip install Django==3.2.8 djangorestframework==3.12.4
```

## Troubleshooting

### ModuleNotFoundError: No module named 'cv2'
- Installation is still in progress. Wait for pip to finish.
- Run: `python test_dependencies.py` to check status

### ImportError: No module named 'detectron2'
- Not required for demo. Only needed when using real fish segmentation models.
- To install: `pip install git+https://github.com/facebookresearch/detectron2.git`

## Files Created for Setup

- **requirements.txt** - All dependencies listed
- **demo_setup.py** - Script to generate synthetic demo data
- **test_dependencies.py** - Verify all packages are installed
- **demo_data/** - Generated demo dataset (created after running demo_setup.py)

## Project Files

- **deep_sort_app.py** - Main tracking application
- **show_results.py** - Visualization tool
- **generate_videos.py** - Video generation tool
- **deep_sort/** - DeepSORT tracking implementation
- **application_util/** - Utilities for preprocessing and visualization
- **centroid_tracker/** - Alternative simple tracking method

---

For questions, refer to README.md
