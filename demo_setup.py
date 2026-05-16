"""
Demo setup script for Fish Behavior Tracking System
This script creates synthetic tracking data for testing the pipeline
without requiring the actual fish video dataset.
"""

import os
import numpy as np
import cv2
from pathlib import Path


def create_demo_structure():
    """Create directory structure for demo"""
    demo_dir = Path("demo_data")
    sequence_dir = demo_dir / "sequences" / "test_sequence"
    
    # Create directories
    sequence_dir.mkdir(parents=True, exist_ok=True)
    (sequence_dir / "img1").mkdir(exist_ok=True)
    
    return sequence_dir


def generate_synthetic_frames(sequence_dir, num_frames=50):
    """Generate synthetic video frames with moving objects"""
    img_dir = sequence_dir / "img1"
    frame_height, frame_width = 480, 640
    
    print(f"Generating {num_frames} synthetic frames...")
    
    for frame_id in range(1, num_frames + 1):
        # Create a frame
        frame = np.ones((frame_height, frame_width, 3), dtype=np.uint8) * 200
        
        # Add some moving "fish-like" objects (rectangles)
        for obj_id in range(3):
            # Calculate position based on frame and object
            x = 100 + (obj_id * 150) + (frame_id * 2) % 100
            y = 150 + (obj_id * 50) + (frame_id * 1.5) % 100
            
            # Draw rectangle (represents a fish)
            cv2.rectangle(frame, (int(x), int(y)), (int(x + 80), int(y + 40)), 
                         (50, 100, 200), -1)
            
            # Add some visual texture
            cv2.putText(frame, f"Fish {obj_id}", (int(x + 10), int(y + 25)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Save frame
        filename = img_dir / f"{frame_id:06d}.png"
        cv2.imwrite(str(filename), frame)
        
        if frame_id % 10 == 0:
            print(f"  Generated frame {frame_id}")
    
    print(f"✓ Generated {num_frames} frames in {img_dir}")


def generate_synthetic_detections(sequence_dir, num_frames=50):
    """Generate synthetic detections in MOTChallenge format"""
    
    # Format: <frame_id>, <id>, <x>, <y>, <width>, <height>, <conf>, <class_id>, <visibility>
    detections = []
    
    print(f"Generating synthetic detections for {num_frames} frames...")
    
    for frame_id in range(1, num_frames + 1):
        for obj_id in range(3):
            # Calculate position
            x = 100 + (obj_id * 150) + (frame_id * 2) % 100
            y = 150 + (obj_id * 50) + (frame_id * 1.5) % 100
            width = 80
            height = 40
            conf = 0.9 + np.random.rand() * 0.1  # Confidence between 0.9-1.0
            
            detections.append([
                frame_id, obj_id, x, y, width, height, conf, 1, 1
            ])
    
    # Save detections
    detections_array = np.array(detections)
    detections_file = sequence_dir.parent / "detections.npy"
    np.save(str(detections_file), detections_array)
    
    print(f"✓ Generated detections file: {detections_file}")
    print(f"  Total detections: {len(detections)}")
    
    return detections_file


def generate_fish_health_metadata(sequence_dir, num_frames=50):
    """Generate synthetic fish health and disease metadata"""
    
    print(f"Generating fish health and disease metadata...")
    
    # Fish metadata: obj_id -> {health_status, disease_status, disease_type}
    fish_metadata = {
        0: {"health": "good", "disease": "none", "confidence": 0.95},
        1: {"health": "lying", "disease": "moderate", "confidence": 0.82},  # Affected fish
        2: {"health": "good", "disease": "none", "confidence": 0.93}
    }
    
    # Create metadata file
    metadata_file = sequence_dir.parent / "fish_metadata.txt"
    with open(metadata_file, 'w') as f:
        f.write("# Fish Health and Disease Metadata\n")
        f.write("# Format: fish_id,health_status,disease_status,disease_confidence\n")
        f.write("# Health: good=normal, lying=abnormal behavior, dead=immobile\n")
        f.write("# Disease: none, mild, moderate, severe\n\n")
        
        for fish_id, metadata in fish_metadata.items():
            f.write(f"{fish_id},{metadata['health']},{metadata['disease']},{metadata['confidence']}\n")
    
    print(f"✓ Generated fish metadata file: {metadata_file}")
    
    # Save as numpy for easy access
    metadata_file_npy = sequence_dir.parent / "fish_metadata.npy"
    np.save(str(metadata_file_npy), fish_metadata, allow_pickle=True)
    
    return fish_metadata, metadata_file


def create_seqinfo(sequence_dir, num_frames=50):
    """Create seqinfo.ini file"""
    seqinfo_content = f"""[Sequence]
name=test_sequence
imdir=img1
frameRate=30
seqLength={num_frames}
imWidth=640
imHeight=480
imExt=.png
"""
    
    seqinfo_file = sequence_dir / "seqinfo.ini"
    with open(seqinfo_file, 'w') as f:
        f.write(seqinfo_content)
    
    print(f"✓ Created seqinfo.ini")
    return seqinfo_file


def main():
    print("=" * 60)
    print("Fish Behavior Tracking - Demo Setup")
    print("=" * 60)
    
    # Create directory structure
    sequence_dir = create_demo_structure()
    
    # Generate synthetic data
    num_frames = 50
    generate_synthetic_frames(sequence_dir, num_frames)
    generate_synthetic_detections(sequence_dir, num_frames)
    generate_fish_health_metadata(sequence_dir, num_frames)
    create_seqinfo(sequence_dir, num_frames)
    
    print("\n" + "=" * 60)
    print("✓ Demo setup complete!")
    print("=" * 60)
    print(f"\nDemo data location: {sequence_dir.parent}")
    print("\nTo run the tracker on demo data, use:")
    print(f"  python deep_sort_app.py \\")
    print(f"    --sequence_dir demo_data/sequences/test_sequence \\")
    print(f"    --detection_file demo_data/sequences/detections.npy \\")
    print(f"    --output_file demo_output.txt \\")
    print(f"    --display True")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
