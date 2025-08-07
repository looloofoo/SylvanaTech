import schedule
import time     
from datetime import datetime
from camera import PlantCamera
import yaml

class CameraScheduler:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.camera = PlantCamera(config_path)
        self.schedule_interval()

    def schedule_interval(self):
        interval = self.config['schedule']['capture_interval']
        
        for time_str in interval:
            schedule.every().days.at(time_str).do(self.daily_capture)

    def daily_capture(self):
        try:
            print(f"🌱 Daily capture started at {datetime.now()}")
            image_path = self.camera.capture_image()
            print(f"✅ Daily capture complete: {image_path}")
        except Exception as e:
            print(f"❌ Daily capture failed: {e}")

    def run(self):
        print("Plant monitor scheduler started")
        print("Press Ctrl+C to stop")
        
        self.daily_capture()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  
        except KeyboardInterrupt:
            print("Scheduler stopped by user.")


if __name__ == "__main__":
    scheduler = CameraScheduler()
    scheduler.run()