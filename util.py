# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 02:07:19 2023

@author: MINGKE
"""

import os
import pickle
from deepface import DeepFace
import tkinter as tk
from tkinter import messagebox


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def msg_box(title, description):
    messagebox.showinfo(title, description)

def recognize(pathfolder):
    for dirpath,dirnames,imagename in os.walk(pathfolder):
        continue

    return imagename
        
def verification(img1, img2):
    face_verified = DeepFace.verify(img1,
                            img2,
                            detector_backend="ssd",
                            model_name="VGG-Face",
                            distance_metric="cosine")
    
    
    cosine_value = face_verified['distance']
    
    return cosine_value

def get_spending(window):
    inputtxt = tk.Text(window, height = 1,
                width = 12,
                bg = "white",
                font=("Arial", 20))   
    
    return inputtxt

def get_console(window):
    outputtxt = tk.Text(window, height = 2,
                width = 33,
                bg = "light blue",
                font=("Calibri", 15))   
    
    return outputtxt

def get_max(window):
    outputtxt = tk.Text(window, height = 1.6,
                width = 18,
                bg = "pink",
                font=("Arial", 9))   
    
    return outputtxt
    
    