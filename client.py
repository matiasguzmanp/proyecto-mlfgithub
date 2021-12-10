import os
import sys
import requests
import time
import cv2
import numpy as np


class ClientWrapper:

    def __init__(self, url='localhost'):
        self.url = url

    def get_single_frame(self):
        response = requests.get('http://'+self.url+':5000/single_frame', stream=True).raw
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)