"""
Camera utils for plant health monitoring
"""


import cv2 
import os 
import time
from datetime import datetime 

class CameraManager:

    def __init__(self, camera_id=0, resolution=(1280, 720)):
        self.camera_id = camera_id
        self.resolution = resolution 
        self.camera = None

    def initialize(self):
        # Starts camera 
        self.camera = cv2.VideoCapture(self.camera_id)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[0])

        if not self.camera.isOpened():
            raise RuntimeError("Failed to open camera. Check if it isn't connected and not in use by another app.")
    
        return RuntimeError("Failed to open camera. Check if it connected or being used by another application")

    def capture_frame(self):

        if self.camera is None or not self.camera.isOpened():
            raise RuntimeError("Camera is not initialized. Call initializer() first.")
        
        ret, frame = self.camera.read()

        if not ret:
            raise RuntimeError("Failed to capture frame from camera.")
        
        return frame
    
    def capture_and_save(self, output_dir, filename=None):
        """
        This function captures a single frame and saves is to a directory

        Note: See if this part can sent to server and not saved locallly
        """

        os.makedirs(output_dir, exist_ok=True)

        frame = self.capture_frame()

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"plant_{timestamp}.jpg"

        image_path = os.path.join(output_dir, filename)
        cv2.imwrite(image_path, frame)

        return image_path, frame 
    
    def start_timelapse(self, output_dir, interval_seconds=3600, max_frames=None, display=True):
        """
        Note: The argument max frame should be set before runnig to assure we have enoght space locally"
        Also: Display argument set to true can be changed to false if running in headless mode.     
        """
        
        os.makedirs(output_dir, exist_ok=True)

        if self.camera is None:
            self.initialize()

        frame_count = 0
        captured_paths = []

        print(f"Starting timelapse. Images will be saved to {output_dir}")
        print(f"Press 'q' to stop caturing")

        try: 
            while True: 
                if max_frames is not None and frame_count >= max_frames:
                    break 
            
            image_path, frame = self.capture_and_save(output_dir)
            captured_paths.append(image_path)
            frame_count += 1

        except KeyboardInterrupt:
            print("Timelapse stopped by user")
        finally:
            if display:
                cv2.destroyAllWindows()

    def release(self):
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()
            self.camera = None

    def list_available_cameras(max_cameras=10):
        """
        Creating this since it could be useful in the future if more cameras are added to the rig.
        """
        available_cameras = {}

        for camera_id in range(max_cameras):
            camera = cv2.VideoCapture(camera_id)
            if camera.isOpened():
                ret, _ = camera.read()
                if ret:
                    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                    heigth = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    available_cameras[camera_id] = (width, heigth)
                camera.release()
        
        return available_cameras         


                    