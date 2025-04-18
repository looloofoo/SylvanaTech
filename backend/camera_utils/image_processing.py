import cv2 
import numpy as np
import matplotlib.pyplot as plt
import os 
from datetime import datetime
import pandas as pd

class PlantAnalyzer: 
    def __init__(self):
        """
        Initialize the plant analyzer

        This is based only only on basic colors present on the leaves
        """
        self.color_ranges = { 
            'green': (np.array([35, 40, 40]). np.array([85, 255, 255])), 
            'yellow': (np.array([20, 40, 40]). np.array([35, 255, 255])), 
            'brown': (np.array([0, 40, 40]). np.array([20, 255, 255])), 
        }

        self.history = {
            'timestamps': [],
            'green_percent': [],
            'yellow_percent': [],
            'brown_percent': [],
            'plant_area_percent': []
        }

    def detect_colors(self, image):
        