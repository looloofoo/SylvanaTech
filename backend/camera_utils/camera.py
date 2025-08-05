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
            cap.release()
            raise RuntimeError("Could not open camera source: {}".format(self.camera_source))

        try:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

            # Warm up the camera
            for _ in range(5):
                cap.read()

            ret, frame = cap.read()
            if not ret or frame is None:
                raise RuntimeError("Failed to capture image from camera.")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"plant_image_{timestamp}.jpg"
            image_path = os.path.join(self.data_directory, image_filename)

            if not cv2.imwrite(image_path, frame):
                raise IOError(f"Failed to write image to {image_path}")

            return image_path
        finally:
            cap.release()
    
if __name__ == "__main__":
    camera = PlantCamera()
    try:
        image_path = camera.capture_image()
        print(f"Image captured and saved at: {image_path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()