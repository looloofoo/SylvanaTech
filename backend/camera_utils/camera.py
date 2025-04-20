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
        """
        Initialize camera
        """ 
        self.camera = cv2.VideoCapture(self.camera_id)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        if not self.camera.isOpened():
            raise RuntimeError("Failed to open camera. Check if it isn't connected and not in use by another app.")
 
        return self.camera.isOpened():

    def capture_frame(self):
        """
        Capture a single frame from the cameras
        """
        if self.camera is None or not self.camera.isOpened():
            self.initialize()

        ret, frame = self.camera.read()
        
        if not ret:
            raise RuntimeError("Failed to capture frame from camera.")
        
        return frame
    
    def save_frame(self, frame, output_dir, filename=None):
        """
        Save a frame to the specific directory
        """
        os.makedirs(output_dir, exist_ok=True)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"

        if not filename.lower().endswith(('.jpg','.jpeg')):
            filename += '.jpg'


        file_path = os.path.join(output_dir, filename)
        success = cv2.imwrite(file_path, frame)

        if not success: 
            raise RuntimeError(f"Failed to save image to {file_path}")

        return file_path

    def capture_and_save(self, output_dir, filename=None):
        """
        This function captures a single frame and saves is to a directory

        Note: See if this part can sent to server and not saved locallly
        """
        
        frame = self.capture_frame()
        return self.save_frame(frame, output_dir, filename)

    def release(self):
        """
        Release the camera resources
        """
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

