import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import re
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def ma(table="dataset_file", lfc="logFC", ct_count="value1", st_count="value2", lfc_thr=1,dd=""):
    # load csv data file
    d = pd.read_csv(table, sep=",")
    d.loc[(d[lfc] >= lfc_thr), 'color'] = "green" # upregulated
    d.loc[(d[lfc] <= -lfc_thr), 'color'] = "red"  # downregulated
    d['color'].fillna('grey', inplace=True)  # intermediate
    d['A'] = np.log2((d[ct_count] + d[st_count]) / 2)
    # plot
    plt.scatter(d['A'], d[lfc], c=d['color'])
    # draw a central line at M=0
    plt.axhline(y=0, color='b', linestyle='--')
    plt.xlabel('A', fontsize=15, fontname="sans-serif", fontweight="bold")
    plt.ylabel('M', fontsize=15, fontname="sans-serif", fontweight="bold")
    plt.xticks(fontsize=12, fontname="sans-serif")
    plt.yticks(fontsize=12, fontname="sans-serif")
    plt.savefig(dd, format='png', bbox_inches='tight', dpi=800)





def MA_P(xlsx="csvfile",os_s="SaveDirectory",n_1="b1",lfc_thr=1):
	wd=pd.read_excel( xlsx, index_col=None, header=None)
	wd=wd.drop([0,1], axis=0)
	wd=wd.drop([1,2,3,4,5,6,9,11,12,13], axis=1)
	d=os_s+'\\'+n_1+".csv"
	d1=os_s+'\\'+n_1+"_MAplot.png"
	wd.to_csv(d,index=False)
	ma(table=d, lfc="10", ct_count="7", st_count="8", lfc_thr=1,dd=d1)
	print(wd.head())
	



def callback():
	text = askopenfilename(filetype = (("xlsx files", "*.xlsx"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	
	b1=re.search('/(\w+)\.',csvfile).group(1)
	MA_P(xlsx=csvfile,os_s=SaveDirectory,n_1=b1)


root = Tk()
root.title('MA diagram')
path = StringVar()
Label(root,text = "目標路徑:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 0, column = 2)

root.mainloop()