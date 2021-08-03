import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import re
import os
#from bioinfokit import visuz
import math
from adjustText import adjust_text

def volcano(table="dataset_file", lfc="log2FC", pv="p-value", lfc_thr=1, pv_thr=0.05,xmin=-10,xmax=10,line=1,colup="red",coldown="blue",YN=1):
    # load csv data file
    np.random.seed(0)
    d = pd.read_csv(table, sep=",")
    d.loc[(d[lfc] >= lfc_thr) & (d[pv] < pv_thr), 'color'] = colup  # upregulated
    d.loc[(d[lfc] <= -lfc_thr) & (d[pv] < pv_thr), 'color'] = coldown  # downregulated
    d.loc[(d[lfc] > xmax), lfc] = xmax  # upregulated
    d.loc[(d[lfc] < xmin), lfc] = xmin  # downregulated
    d['color'].fillna('black', inplace=True)  # intermediate
    d['logpv'] = -(np.log10(d[pv]))
    # plot
    #plt()
    plt.figure(figsize=(15, 10), dpi=1000)
    plt.title("Volcano Plot", fontsize=15, fontname="sans-serif", fontweight="bold")
    plt.scatter(d[lfc], d['logpv'], c=d['color'], alpha=0.4,s=20)
    plt.xlabel('log2 Fold Change', fontsize=12, fontname="sans-serif", fontweight="bold")
    plt.ylabel('-log10(P-value)', fontsize=12, fontname="sans-serif", fontweight="bold")
    plt.xticks(fontsize=12, fontname="sans-serif")
    plt.yticks(fontsize=12, fontname="sans-serif")
    if line==1:
        plt.axvline(x=-lfc_thr, color='b', linestyle='--')
        plt.axvline(x=lfc_thr, color='b', linestyle='--')
        plt.axhline(y=-(np.log10(pv_thr)), color='b', linestyle='--')
    if YN==1:
        texts=[]
        aa=d.isnull()
        for i, varnames in enumerate(d['GeneNames']):
	        if  (aa['symbol'][i]==False) :#(abs(d[lfc][i]) >= lfc_thr) & (d[pv][i] < pv_thr) & 
                 texts.append(plt.text(d[lfc][i], d['logpv'][i],d['symbol'][i],fontsize=8))
        plt.margins(y=0.125)
        #adjust_text(texts)
    #plt.plot(-1, y , linestyle='--')
    plt.xlim(xmin,xmax)


def callback():
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	b=re.search('/(\w+)\.',csvfile).group(1)
	volcano(table=csvfile, lfc="log2FC", pv="p-value", lfc_thr=lfc_thr.get(), pv_thr=pv_thr.get(),xmin=xmin.get(),xmax=xmax.get(),line=var1.get(),colup=colup.get(),coldown=coldown.get(),YN=var2.get())
	c=SaveDirectory+'\\'+b+'_Volcano.png'
	#plt.set_size_inches(2000, 1600, forward=True)
	plt.savefig(c)
	print(c)	
	#sns.heatmap(df), dpi=2000
	#plt.set_size_inches(2000, 1600, forward=True)
	#plt.show()	

root = Tk()
root.title('volcano')
lfc_thr = DoubleVar()
lfc_thr.set(1)
pv_thr = DoubleVar()
pv_thr.set(0.05)
Label(root, text='Cut Fold Change: ').grid(row = 0, column = 0)#创建一个`label`名为`User name: `置于坐标（50,150）
Label(root, text='Cut P-value: ').grid(row = 1, column = 0)
Entry(root, textvariable = lfc_thr).grid(row = 0, column = 1)
Entry(root, textvariable = pv_thr).grid(row = 1, column = 1)

xmin = DoubleVar()
xmax = DoubleVar()
xmin.set(-10)
xmax.set(10)
Label(root, text='FC(Min-Max): ').grid(row = 2, column = 0)
Entry(root, textvariable = xmin).grid(row = 2, column = 1)
Label(root, text='-').grid(row = 2, column = 2)
Entry(root, textvariable = xmax).grid(row = 2, column = 3)

var1 = IntVar()
var1.set(1)
Label(root, text='虛線 ').grid(row = 3, column = 0)
c1 = Checkbutton(root, text='有', variable=var1, onvalue=1, offvalue=0).grid(row = 3, column = 1)

var2 = IntVar()
var2.set(1)
Label(root, text='文字 ').grid(row = 3, column = 2)
c1 = Checkbutton(root, text='有', variable=var2, onvalue=1, offvalue=0).grid(row = 3, column = 3)



colup = StringVar()
coldown = StringVar()  
colup.set("red") 
coldown.set("blue")
Label(root, text='Up color: ').grid(row = 4, column = 0)
Entry(root, textvariable = colup).grid(row = 4, column = 1)
Label(root, text='Down color:').grid(row = 4, column = 2)
Entry(root, textvariable = coldown).grid(row = 4, column = 3)
Label(root, text='Example: red、blue、green').grid(row = 4, column = 4)

path = StringVar()
Label(root,text = "目標路徑:").grid(row = 5, column = 0)
Entry(root, textvariable = path).grid(row = 5, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 5, column = 2)

root.mainloop()
