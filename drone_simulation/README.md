# Drone Simulation

This directory contains the Visual SLAM (V-SLAM) demonstration for PRALAYA-NET.

## Files

- `visual_slam.py`: Main SLAM demo script using OpenCV
- `config.json`: Drone and simulation configuration
- `video_feed.mp4`: Pre-recorded drone footage (placeholder - add your own video file)

## Usage

### Running the SLAM Demo

```bash
cd drone_simulation
python visual_slam.py
```

### Controls

- Press `s` to enable/disable V-SLAM
- Press `q` to quit

### Video Feed

The script will attempt to use:
1. A connected webcam (default)
2. A video file if `video_feed.mp4` exists
3. Simulated mode if neither is available

To use your own video:
- Place a video file named `video_feed.mp4` in this directory
- Or modify `visual_slam.py` to use a different file path

## Features

- Real-time feature detection using ORB
- Map point tracking
- Keyframe extraction
- Visual feedback on camera feed

## Requirements

- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)



