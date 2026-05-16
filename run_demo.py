#!/usr/bin/env python
"""
Fish Behavior Tracking System - Complete Demo Runner

Automates the entire demo pipeline:
1. Verify all dependencies
2. Generate synthetic demo data
3. Run DeepSORT tracker
4. Display results with health, disease, and speed analysis
"""

import subprocess
import os
import sys
import numpy as np
from pathlib import Path
from collections import defaultdict


def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_command(cmd, step_name):
    """Execute a command and handle errors"""
    print(f"\n[{step_name}] Running: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {step_name} failed with exit code {e.returncode}")
        return False


def load_fish_health_metadata():
    """Load fish health and disease metadata"""
    metadata_file = Path("demo_data/sequences/fish_metadata.txt")
    fish_metadata = {}
    
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            for line in f:
                if line.startswith("#") or line.strip() == "":
                    continue
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    fish_id = int(parts[0])
                    fish_metadata[fish_id] = {
                        'health': parts[1],
                        'disease': parts[2],
                        'confidence': float(parts[3])
                    }
    
    return fish_metadata


def calculate_fish_speed(tracking_data):
    """Calculate speed for each fish based on tracking data"""
    # Group by track_id
    fish_positions = defaultdict(list)
    
    for line in tracking_data:
        parts = line.strip().split(',')
        if len(parts) >= 6:
            frame_id = int(parts[0])
            track_id = int(parts[1])
            x = float(parts[2])
            y = float(parts[3])
            
            fish_positions[track_id].append({
                'frame': frame_id,
                'x': x,
                'y': y
            })
    
    # Calculate speed (pixels per frame)
    fish_speeds = {}
    for track_id, positions in fish_positions.items():
        if len(positions) > 1:
            # Calculate distances between consecutive frames
            distances = []
            for i in range(1, len(positions)):
                dx = positions[i]['x'] - positions[i-1]['x']
                dy = positions[i]['y'] - positions[i-1]['y']
                distance = (dx**2 + dy**2)**0.5
                distances.append(distance)
            
            # Average speed
            avg_speed = sum(distances) / len(distances) if distances else 0
            fish_speeds[track_id] = {
                'avg_speed': avg_speed,
                'min_speed': min(distances) if distances else 0,
                'max_speed': max(distances) if distances else 0,
                'frames': len(positions)
            }
    
    return fish_speeds


def main():
    print_header("Fish Behavior Tracking System - Complete Demo")
    
    project_dir = Path.cwd()
    python_exe = "c:/Users/kowne/AppData/Local/Python/pythoncore-3.14-64/python.exe"
    
    # Step 1: Verify Dependencies
    if not run_command(
        [python_exe, "test_dependencies.py"],
        "STEP 1/3: Verify Dependencies"
    ):
        return 1
    
    # Step 2: Generate Demo Data
    if not run_command(
        [python_exe, "demo_setup.py"],
        "STEP 2/3: Generate Demo Data"
    ):
        return 1
    
    # Step 3: Run Tracker
    if not run_command(
        [
            python_exe, "deep_sort_app.py",
            "--sequence_dir", "demo_data/sequences/test_sequence",
            "--detection_file", "demo_data/sequences/detections.npy",
            "--output_file", "demo_output.txt",
            "--display", "False"
        ],
        "STEP 3/3: Run DeepSORT Tracker"
    ):
        return 1
    
    # Display Results with Health, Disease, and Speed Analysis
    print_header("Tracking Results with Fish Health Analysis")
    
    output_file = Path("demo_output.txt")
    if not output_file.exists():
        print("✗ Output file not found!")
        return 1
    
    with open(output_file, 'r') as f:
        lines = f.readlines()
    
    # Load fish metadata
    fish_metadata = load_fish_health_metadata()
    
    # Calculate speeds
    fish_speeds = calculate_fish_speed(lines)
    
    # Display first 10 results
    print("\nFirst 10 tracking results:")
    print("-" * 100)
    print(f"{'#':>2} | {'Frame':>5} | {'Track':>5} | {'X':>7} | {'Y':>7} | {'Health':>8} | {'Disease':>10} | {'Confidence':>10} | {'Speed (px/f)':>12}")
    print("-" * 100)
    
    for i, line in enumerate(lines[:10], 1):
        parts = line.strip().split(',')
        if len(parts) >= 6:
            frame_id = int(parts[0])
            track_id = int(parts[1])
            x = float(parts[2])
            y = float(parts[3])
            
            # Get health info
            health = fish_metadata.get(track_id, {}).get('health', 'unknown')
            disease = fish_metadata.get(track_id, {}).get('disease', 'unknown')
            confidence = fish_metadata.get(track_id, {}).get('confidence', 0.0)
            
            # Get speed info
            speed_info = fish_speeds.get(track_id, {})
            speed = speed_info.get('avg_speed', 0.0)
            
            # Color code health status
            health_display = f"[{health.upper()}]"
            
            print(f"{i:2d} | {frame_id:5d} | {track_id:5d} | {x:7.1f} | {y:7.1f} | {health_display:>8} | {disease:>10} | {confidence:>10.2f} | {speed:>12.2f}")
    
    # Display Fish Summary
    print("\n" + "-" * 100)
    print_header("Fish Health & Disease Summary")
    
    print("\nFish Status Overview:")
    print("-" * 60)
    print(f"{'Fish ID':>8} | {'Health Status':>15} | {'Disease Status':>15} | {'Avg Speed (px/f)':>18} | {'Tracked Frames':>15}")
    print("-" * 60)
    
    for track_id in sorted(fish_speeds.keys()):
        health = fish_metadata.get(track_id, {}).get('health', 'unknown')
        disease = fish_metadata.get(track_id, {}).get('disease', 'unknown')
        speed_info = fish_speeds.get(track_id, {})
        avg_speed = speed_info.get('avg_speed', 0.0)
        frames = speed_info.get('frames', 0)
        
        # Disease impact indicator
        disease_indicator = "✗" if disease != "none" else "✓"
        
        print(f"{track_id:8d} | {health:>15} | {disease:>15} | {avg_speed:>18.2f} | {frames:>15d}")
    
    # Detailed Analysis
    print("\n" + "-" * 100)
    print_header("Disease Detection Analysis")
    
    affected_fish = {tid: meta for tid, meta in fish_metadata.items() if meta['disease'] != 'none'}
    healthy_fish = {tid: meta for tid, meta in fish_metadata.items() if meta['disease'] == 'none'}
    
    print(f"\nHealthy Fish: {len(healthy_fish)}")
    for fish_id, meta in healthy_fish.items():
        speed_info = fish_speeds.get(fish_id, {})
        avg_speed = speed_info.get('avg_speed', 0.0)
        print(f"  • Fish {fish_id}: GOOD (Normal movement, avg speed: {avg_speed:.2f} px/frame)")
    
    print(f"\nAffected Fish (Disease Detected): {len(affected_fish)}")
    for fish_id, meta in affected_fish.items():
        speed_info = fish_speeds.get(fish_id, {})
        avg_speed = speed_info.get('avg_speed', 0.0)
        print(f"  • Fish {fish_id}: {meta['health'].upper()} - Disease: {meta['disease'].upper()}")
        print(f"    └─ Confidence: {meta['confidence']:.2%} | Avg Speed: {avg_speed:.2f} px/frame")
    
    # Statistics
    print("\n" + "=" * 100)
    print("STATISTICS")
    print("=" * 100)
    print(f"Total tracked detections: {len(lines)}")
    print(f"Unique fish tracked: {len(fish_speeds)}")
    print(f"Output file size: {output_file.stat().st_size:,} bytes")
    
    # Calculate average speed across all fish
    all_speeds = [info['avg_speed'] for info in fish_speeds.values()]
    if all_speeds:
        print(f"Average speed (all fish): {sum(all_speeds)/len(all_speeds):.2f} px/frame")
        print(f"Speed range: {min(all_speeds):.2f} - {max(all_speeds):.2f} px/frame")
    
    # Summary
    print_header("Summary")
    print("""
✓ Demo run completed successfully!

Disease Detection Results:
  ✓ All fish tracked and analyzed
  ✓ Health status: Good/Lying/Dead
  ✓ Disease detection with confidence scores
  ✓ Movement speed analysis complete
  
Next Steps:
  1. Review detailed results above
  
  2. Request real fish video dataset:
     https://docs.google.com/forms/d/e/1FAIpQLScHzbEzj97v6YZn3EdU8Pt4aMXj5cGPe4qJ05mQrM6df54tJg/viewform
  
  3. Place video sequences in: demo_data/sequences/
  
  4. Run tracker on real data with health analysis:
     python deep_sort_app.py \\
       --sequence_dir demo_data/sequences/fish_video_1 \\
       --detection_file detections.npy \\
       --output_file results.txt

System Features:
  • Multi-object tracking with DeepSORT
  • Health status monitoring (good/lying/dead)
  • Disease detection and classification
  • Movement speed analysis
  • Appearance-based identity maintenance
  • Kalman filter motion prediction
  • MOTChallenge-format output
  
For more information, see: SETUP_COMPLETE.md
""")
    print("=" * 100 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
