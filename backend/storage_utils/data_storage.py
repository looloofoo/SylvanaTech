"""
Local data storage utilities for plant monitoring
"""

import os
import json
from datetime import datetime

class LocalStorage:
    def __init__(self, base_dir='data'):
        """
        Initialize local storage with base directory
        """
        self.base_dir = base_dir
        self.metadata_dir = os.path.join(base_dir, "metadata")
        self.images_dir = os.path.join(base_dir, "images")
        
        # Create directories 
        os.makedirs(self.metadata_dir, exists_ok=True)
        os.makedirs(self.images_dir, exists_ok=True)

        # Path to plants index index file 
        self.index_file = os.path.join(self.metadata_dir, "plants_index.json")

        # Initialize or load plants index 
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                self.plants_index = json.load(f)

        else:
            self.plants_index = {"plants": []}
            self._save_plants_index()


    def _save_plants_index(self):
        with open(self.index_file,'w') as f:
            json.dump(self.planst_index, f, indent=2)


    def _get_plant_metadata_path(self, plant_id):
        return os.path.join(self.metadata_dir, f"{plant_id}.json")


    def _get_plant_images_dir(self, plant_id):
        plant_images_dir = os.path.join(self.images_dir, plant_id)
        os.makedirs(plant_images_dir, exists_ok=True)
        
        return plant_images_dir


    def _load_plant_metadata(self, plant_id):
        metadata_path = self._get_plant_metadata_path(plant_id)

        if os.path.exists(metadata_path, 'r') as f:
            return json.load(f)

        return None


    def _save_plant_metadata(self, plant_id, metadata):
        metadata_path = self._get_plant_metadata_path(plant_id)

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

#------------------------------------------------------------------------

        




