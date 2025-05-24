import pandas as pd
from pandas import DataFrame
import os

categorys=['n100','n200','n400']
for category in categorys:
    #category='n100'
    path='./Solutions/'
    name=os.listdir(path+category)
    data=[]
    for txt in name:
        data.append([txt.split(".")[0],int(txt.split(".")[1].split("_")[0]),int(txt.split(".")[1].split("_")[1])])
    pd=DataFrame(data,columns=['Instance','Vehicles','Distance'])
    save_path='./SOTA/'+category+'.xlsx'
    pd.to_excel(save_path,index = False)