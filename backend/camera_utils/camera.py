import cv2 
import numpy as np
import os
import json 
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from contextlib import contextmanager


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class PlantMetadata:
    plant_id: str
    species: str
    date_planted: str
    growth_stage: str
    expected_harvest_days: str

@dataclass
class CaptureSession: 
    timestamp: str
    environmental_data: Optional[Dict] = None
    image_path: str = ""
    plant_metadata: List[PlantMetadata] = None
    individual_images: Dict[str, str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        if self.plant_metadata is None:
            self.plant_metadata = []
        if self.individual_images is None:
            self.individual_images = {}

class EnhancedCameraManager:
    def __init__(self, camera_id=0, resolution=(1920, 1080)):
        self.camera_id = camera_id
        self.resolution = resolution
        self.camera = None
        self.base_dir = "plant_data"
        self.setup_directories()

    def setup_directories(self):
        directories = [
            f"{self.base_dir}/images/daily",
            f"{self.base_dir}/images/timelapse",
            f"{self.base_dir}/images/individual",
            f"{self.base_dir}/metadata",
            f"{self.base_dir}/environmental_data",
            f"{self.base_dir}/notes"
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"Created/verified directory: {directory}")
            except OSError as e:
                logger.error(f"Failed to create directory {directory}: {e}")
                raise

    @contextmanager
    def camera_context(self):
        """Context manager for proper camera resource handling"""
        try:
            if self.camera is None:
                self.camera = cv2.VideoCapture(self.camera_id)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                
                if not self.camera.isOpened():
                    raise RuntimeError(f"Failed to open camera {self.camera_id}")
                    
                logger.info(f"Camera {self.camera_id} initialized with resolution {self.resolution}")
            
            yield self.camera
            
        except Exception as e:
            logger.error(f"Camera error: {e}")
            raise
        finally:
            if self.camera is not None:
                self.camera.release()
                self.camera = None
                logger.info("Camera released")

    #====================================================================================================
    ################
    # Core functions 
    ################
    def capture_frame(self):
        """Capture a single frame from the camera"""
        with self.camera_context() as camera:
            ret, frame = camera.read()
            if not ret:
                raise RuntimeError("Failed to capture frame from camera")
            return frame
    
    def save_image(self, frame, timestamp, image_type): 
        """Save image to appropriate directory"""
        try:
            filename = f"{image_type}_{timestamp}.jpg"
            filepath = os.path.join(self.base_dir, "images", image_type, filename)
            
            success = cv2.imwrite(filepath, frame)
            if not success:
                raise RuntimeError(f"Failed to save image to {filepath}")
                
            logger.info(f"Image saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            raise

    def save_session_metadata(self, metadata: CaptureSession):
        """Save capture session metadata to JSON file"""
        try:
            metadata_path = os.path.join(self.base_dir, "metadata", f"{metadata.timestamp}.json")
            
            # Convert dataclass to dict for JSON serialization
            metadata_dict = asdict(metadata)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata_dict, f, indent=4, default=str)
                
            logger.info(f"Metadata saved: {metadata_path}")
            
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            raise
    

    #====================================================================================================
    #######################
    # Daily Capture Session 
    #######################
    def capture_daily_session(self, plants: List[PlantMetadata], 
                              environmental_data: Dict = None, 
                              notes: str = None) -> CaptureSession:
        """Capture daily session with main image and individual plant photos"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"Starting daily capture session: {timestamp}")

        try:
            # Capture main frame
            frame = self.capture_frame()
            image_path = self.save_daily_image(frame, timestamp)

            # Capture individual plant images
            individual_images = self.capture_individual_plants(plants, timestamp)

            # Create session metadata
            metadata = CaptureSession(
                timestamp=timestamp,
                environmental_data=environmental_data,
                image_path=image_path,
                plant_metadata=plants,
                individual_images=individual_images,
                notes=notes
            )

            self.save_session_metadata(metadata)
            logger.info(f"Daily capture session completed: {timestamp}")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error in daily capture session: {e}")
            raise
    
    def save_daily_image(self, frame, timestamp):
        """Save daily image with timestamp overlay"""
        try:
            filename = f"daily_{timestamp}.jpg"
            filepath = os.path.join(self.base_dir, "images", "daily", filename)

            annotated_frame = self.add_timestamp_overlay(frame, timestamp)

            success = cv2.imwrite(filepath, annotated_frame)
            if not success:
                raise RuntimeError(f"Failed to save daily image to {filepath}")
                
            logger.info(f"Daily image saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving daily image: {e}")
            raise
    
    def add_timestamp_overlay(self, frame, timestamp):
        """Add timestamp overlay to frame"""
        # Work on a copy to avoid modifying the original
        annotated = frame.copy()

        # Convert timestamp to readable format
        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        text = dt.strftime("%Y-%m-%d %H:%M:%S")
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Add white text with black border for better visibility
        cv2.putText(annotated, text, (10, 30), font, 1, (0, 0, 0), 3, cv2.LINE_AA)  # Black border
        cv2.putText(annotated, text, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)  # White text
        
        return annotated
    
    def capture_individual_plants(self, plants: List[PlantMetadata], timestamp: str) -> Dict[str, str]:
        """Capture individual photos for each plant"""
        individual_images = {}
        
        try:
            for plant in plants:
                logger.info(f"Capturing individual image for plant: {plant.plant_id}")
                
                frame = self.capture_frame()
                filename = f"{plant.plant_id}_{timestamp}.jpg"
                image_path = os.path.join(self.base_dir, "images", "individual", filename)

                success = cv2.imwrite(image_path, frame)
                if not success:
                    logger.warning(f"Failed to save image for plant {plant.plant_id}")
                    continue
                    
                individual_images[plant.plant_id] = image_path
                logger.info(f"Individual plant image saved: {image_path}")

            return individual_images
            
        except Exception as e:
            logger.error(f"Error capturing individual plants: {e}")
            raise

    def cleanup(self):
        """Cleanup resources"""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            logger.info("Camera resources cleaned up")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        self.cleanup()