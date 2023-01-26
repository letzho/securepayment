# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 01:39:36 2023

@author: MINGKE
"""
# =============================================================================
# Import Libraries
# =============================================================================
import os.path
import datetime
import pickle

import tkinter as tk
from tkinter.ttk import Label
import cv2
from PIL import Image,ImageTk
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from scipy.spatial.distance import cosine,euclidean
import util
from data_analysis import data_process
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title(" Secure Payment Terminal ")
        self.main_window.geometry("1200x620+350+100")
        self.main_window.iconbitmap('./folder.ico')
        

        self.identify_button_main_window = util.get_button(self.main_window, 'Verify', 'orange', self.verify)
        self.identify_button_main_window.place(x=750, y=120)
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=10, width=700, height=600)
        self.add_webcam(self.webcam_label)
        
        self.spending_label=Label(self.main_window, text = "Spending $")
        self.spending_label.place(x=750, y=20)
        self.spending_box = util.get_spending(self.main_window)
        self.spending_box.place(x=750, y=40)
        
        self.maxallow_label=Label(self.main_window, text = "Max Limit (fr Past Transaction)")
        self.maxallow_label.place(x=950, y=20)
        self.maxallow_box=util.get_max(self.main_window)
        self.maxallow_box.place(x=950, y=40)
        
        self.result_label=Label(self.main_window, text = "Result of Verification")
        self.result_label.place(x=750, y=240)
        self.output_box=util.get_console(self.main_window)
        self.output_box.place(x=750, y=270)
        
        self.time_label=Label(self.main_window, text = "Elapsed time (s)")
        self.time_label.place(x=750, y=340)
        self.time_box=util.get_console(self.main_window)
        self.time_box.place(x=750, y=370)

        
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

       
        self.rImg=frame    
        imagelast= cv2.cvtColor(self.rImg, cv2.COLOR_BGR2RGB)
        
        self.image_new = Image.fromarray(imagelast)
        imgtk = ImageTk.PhotoImage(image=self.image_new)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(10, self.process_webcam)
        
    def start(self):
        self.main_window.mainloop()

    def verify(self):
        self.output_box.delete('1.0',tk.END)
        self.maxallow_box.delete('1.0',tk.END)
        self.time_box.delete('1.0',tk.END)
        pathfolder='./image_db'
        starttime=datetime.now()
        output=util.recognize(pathfolder)
        no_user=len(output)
        
        cosine_list=[]
        for i in range(no_user):
            img2=os.path.join(pathfolder,output[i])
            cosine=util.verification(self.rImg,img2)
            cosine_list.append(cosine)
        
        min_cosine=min(cosine_list)
        index_min=cosine_list.index(min_cosine)
        verified_user=output[index_min]
        username=verified_user.split('.')[0]       
        if min_cosine<0.4:
            result=f'{username} is verified'           
            flag=True
        else:
            result='User is NOT verified'
            util.msg_box('Fail!', 'Failed Authentication!')
            flag=False
            
        timeelapsed=datetime.now()-starttime
        elapsed_time=timeelapsed.total_seconds() 
        self.output_box.insert('1.0', result)
        self.time_box.insert('1.0', round(elapsed_time,1))
        
        #Check transacted amount
        spend_amount=self.spending_box.get("1.0", "end-1c")
        expenditure=float(spend_amount)
        spending_folder='./spending_db'
        allow_transact,max_allow=data_process(spending_folder,username,expenditure)
        self.maxallow_box.insert('1.0', round(max_allow,2))
        if flag==True:
            if allow_transact:
                
                util.msg_box('Success!', 'Transaction is successful !')
            else:
                
                util.msg_box('Fail!', 'Failed Transaction (Exceed allowable limit)!')
           
    
        
if __name__ == "__main__":
    app = App().start()
    
