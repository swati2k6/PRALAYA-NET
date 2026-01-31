"""
Visual SLAM Demo - Demonstrates GPS-denied navigation
Uses laptop camera or video feed for SLAM simulation
"""

import cv2
import numpy as np
import json
from pathlib import Path

class VisualSLAMDemo:
    """
    Visual SLAM demonstration using OpenCV
    Simulates feature detection and mapping for GPS-denied navigation
    """
    
    def __init__(self, config_path="config.json"):
        self.config = self._load_config(config_path)
        self.cap = None
        self.slam_enabled = False
        self.map_points = []
        self.keyframes = []
        
    def _load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_path} not found, using defaults")
            return {
                "drone": {"max_altitude": 120},
                "simulation": {"update_interval_ms": 2000}
            }
    
    def initialize_camera(self, source=0):
        """
        Initialize camera or video source
        
        Args:
            source: Camera index (0 for default) or video file path
        """
        if isinstance(source, str) and Path(source).exists():
            self.cap = cv2.VideoCapture(source)
        else:
            self.cap = cv2.VideoCapture(source)
        
        if not self.cap.isOpened():
            print("Error: Could not open camera/video source")
            return False
        
        print("Camera initialized successfully")
        return True
    
    def enable_slam(self):
        """Enable Visual SLAM"""
        self.slam_enabled = True
        self.map_points = []
        self.keyframes = []
        print("V-SLAM enabled - GPS-denied navigation active")
    
    def disable_slam(self):
        """Disable Visual SLAM"""
        self.slam_enabled = False
        print("V-SLAM disabled - GPS navigation active")
    
    def detect_features(self, frame):
        """
        Detect features in frame using ORB detector
        
        Args:
            frame: Input image frame
        
        Returns:
            Keypoints and descriptors
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # ORB feature detector
        orb = cv2.ORB_create(nfeatures=500)
        keypoints, descriptors = orb.detectAndCompute(gray, None)
        
        return keypoints, descriptors
    
    def process_frame(self, frame):
        """
        Process a frame for SLAM
        
        Args:
            frame: Input image frame
        
        Returns:
            Processed frame with features visualized
        """
        if not self.slam_enabled:
            return frame
        
        # Detect features
        keypoints, descriptors = self.detect_features(frame)
        
        # Add to map if significant features found
        if len(keypoints) > 50:
            self.map_points.append({
                "keypoints": len(keypoints),
                "timestamp": cv2.getTickCount()
            })
            
            # Store keyframe
            if len(self.keyframes) == 0 or len(keypoints) > self.keyframes[-1]["keypoints"]:
                self.keyframes.append({
                    "keypoints": len(keypoints),
                    "frame_id": len(self.keyframes)
                })
        
        # Draw keypoints on frame
        frame_with_features = cv2.drawKeypoints(
            frame, keypoints, None, color=(0, 255, 0), flags=0
        )
        
        # Add SLAM status overlay
        cv2.putText(
            frame_with_features,
            f"V-SLAM: ACTIVE | Map Points: {len(self.map_points)} | Keyframes: {len(self.keyframes)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        return frame_with_features
    
    def run_demo(self):
        """Run the SLAM demo"""
        print("Starting Visual SLAM Demo")
        print("Press 's' to enable/disable SLAM")
        print("Press 'q' to quit")
        
        if not self.initialize_camera():
            print("Failed to initialize camera. Using simulated mode...")
            # Simulate with a test pattern
            self._simulate_slam()
            return
        
        slam_enabled = False
        
        while True:
            ret, frame = self.cap.read()
            
            if not ret:
                print("End of video or camera error")
                break
            
            # Process frame
            if slam_enabled:
                frame = self.process_frame(frame)
            else:
                cv2.putText(
                    frame,
                    "V-SLAM: INACTIVE (Press 's' to enable)",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )
            
            # Display frame
            cv2.imshow("PRALAYA-NET V-SLAM Demo", frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                slam_enabled = not slam_enabled
                if slam_enabled:
                    self.enable_slam()
                else:
                    self.disable_slam()
        
        self.cap.release()
        cv2.destroyAllWindows()
        print(f"Demo ended. Total map points: {len(self.map_points)}")
    
    def _simulate_slam(self):
        """Simulate SLAM without camera"""
        print("Running simulated SLAM mode...")
        self.enable_slam()
        
        # Simulate feature detection
        for i in range(10):
            self.map_points.append({
                "keypoints": np.random.randint(50, 200),
                "timestamp": i * 1000
            })
            print(f"Frame {i+1}: Detected {self.map_points[-1]['keypoints']} features")
        
        print(f"Simulation complete. Total map points: {len(self.map_points)}")

if __name__ == "__main__":
    demo = VisualSLAMDemo()
    demo.run_demo()
