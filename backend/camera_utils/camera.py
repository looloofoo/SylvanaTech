import cv2
import os 
from datetime import datetime
import yaml

class PlantCamera: 
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.camera_source = self.config['camera']['source']
        self.resolution = self.config['camera']['resolution']
        self.data_directory = "data/images"

        os.makedirs(self.data_directory, exist_ok=True)
    
    def capture_image(self):
        cap = cv2.VideoCapture(self.camera_source)  
        if not cap.isOpened():
            raise Exception("Could not open camera")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        for _ in range(5):
            cap.read()  # Allow camera to warm up

        ret, frame = cap.read()
        if not ret:
            raise Exception("Failed to capture image")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(self.data_directory, f"plant_image_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)

        return image_path
    
