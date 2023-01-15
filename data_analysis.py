# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 18:07:55 2023

@author: MINGKE
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime

def data_process(pathfolder,username,spend):
    
    file_ext=username+'_rec.csv'
    db_filename=os.path.join(pathfolder,file_ext)
    df=pd.read_csv(db_filename)
    
    
    
    def change_to_hour(x):
        timestamp=x
        timeextract=timestamp.split(" ")[1]
        hourextract=timeextract.split(":")[0]
        return int(hourextract)
    
    df['Timestamp (UTC)']=df['Timestamp (UTC)'].map(lambda x:change_to_hour(x))
    df['Amount']=df['Amount'].map(lambda x:abs(x))
    df1=df[(df['Timestamp (UTC)']<11) & (df['Timestamp (UTC)']>=1)]
    df2=df[(df['Timestamp (UTC)']<15) & (df['Timestamp (UTC)']>=11)]
    df3=df[(df['Timestamp (UTC)']<23) & (df['Timestamp (UTC)']>=15)]
    
    #Construct table for statistical mean and std deviation
    stdf=[]
    meanf=[]
    
    for dataf in [df1,df2,df3]:
        std_df=dataf['Amount'].std()
        mean_df=dataf['Amount'].mean()
        stdf.append(std_df)
        meanf.append(mean_df)
    
    outputdf_dict={'Mean':meanf,
                   'std dev':stdf}
    outputdf_df=pd.DataFrame(outputdf_dict,index=['1am-11am','11am-3pm','3pm-12am'])
        
        
    time_current=datetime.now()
    extract_current_time=str(time_current).split(" ")[1]
    extract_hour=extract_current_time.split(":")[0]
    if 1<=int(extract_hour)<11:
        mean=meanf[0]
        std=stdf[0]
        result=spendcheck(spend,mean,std)
     
    elif 11<=int(extract_hour)<15:
        mean=meanf[1]
        std=stdf[1]
        result=spendcheck(spend,mean,std)
    
    elif 15<=int(extract_hour)<24:
        mean=meanf[2]
        std=stdf[2]
        result=spendcheck(spend,mean,std)
    
    return result
    
def spendcheck(spend,mean,std):
    if spend<mean+2*std:
        result_flag=True
    else:
        result_flag=False
    return result_flag
    
    

    