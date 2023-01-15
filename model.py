# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 13:12:46 2023

@author: LEOWSH
"""
# Import libaries
import os
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from scipy.spatial.distance import cosine,euclidean
from deepface import DeepFace


def verification(img1, img2):
    face_verified = DeepFace.verify(img1,
                            img2,
                            detector_backend="opencv",
                            model_name="VGG-Face",
                            distance_metric="cosine")
    
    
    cosine_value = face_verified['distance']

    
    
    print((f"Cosine similarity:{cosine_value:.3f}"))
    
    if(cosine_value< 0.4):
        print("Identity Authenticated")
    else:
        print("Wrong Identity")