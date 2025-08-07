import os 
import yaml
import shutil
from glob import glob


class ImageLabeler:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.categories = self.config['ml']['labeler']
        self.setup_directories()

    def setup_directories(self):
        for category in self.categories:    
            category_path = os.path.join(f"data/labels/{category}")
            if not os.path.exists(category_path):
                os.makedirs(category_path, exist_ok=True)
    
    def label_images(self, image_path, category):
        print("Image Labeler")
        print("==" * 30)

        image_file = glob("data/images/*.jpg")
        if not image_file:
            print("No images found in data/images directory.")
            return
    
        print(f"Found {len(image_file)} images in data/images directory.")
        print("\nCategories:")
        for i, category in enumerate(self.categories, start=1):
            print(f"{i}. {category}")
            print("  s - skip" )
            print("  q - quit")

            labeled_count = 0

            for image_file in sorted(image_file):
                print(f"\nProcessing image: {image_file}")

                while True:
                    choice = input(f"Enter category number (1-{len(self.categories)}) or 's' to skip, 'q' to quit: ").strip().lower()
                    if choice == 'q':
                        print("Exiting labeling process.")
                        return
                    elif choice == 's':
                        print("Skipping this image.")
                        break
                    elif choice.isdigit() and 1 <= int(choice) <= len(self.categories):
                        category = self.categories[int(choice) - 1]
                        destination_path = os.path.join(f"data/labels/{category}", os.path.basename(image_file))
                        
                        shutil.move(image_file, destination_path)
                        labeled_count += 1
                        print(f"Image labeled as '{category}' and moved to {destination_path}")
                        break
                    else:
                        print(f"Invalid input. Please enter a number between 1 and {len(self.categories)}, 's' to skip, or 'q' to quit.")
        print(f"\nLabeled {labeled_count} images.")

if __name__ == "__main__":
    labeler = ImageLabeler()
    labeler.label_images()
    print("Image labeling complete.")
    