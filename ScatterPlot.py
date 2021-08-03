#import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import re
import os
#from matplotlib.axes import xscale, yscale
from adjustText import adjust_text

import random
def co():
	r = lambda: random.randint(0,255)
	cc='#%02X%02X%02X' % (r(),r(),r())
	return cc

def callback( YN=1 ):
	
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	b=re.search('/(\w+)\.',csvfile).group(1)
	rows = pd.read_csv(csvfile)
	df = rows.set_index('gene_id')
	aa=df.isnull()
	df.loc[aa['symbol']!=False, 'color']="black"
	df.loc[aa['symbol']==False, 'color']="red"

	naml=list(df.columns)
	
	for i in range(1,len(naml)-2):
		for j in range(i+1,len(naml)-1):
			na1=naml[i]+"_vs_"+naml[j]+"_Scatter_Plot"
			plt.title(na1, fontsize=15, fontname="sans-serif", fontweight="bold")
			
			data=pd.DataFrame()
			mask = df["symbol"].isnull()
			df.symbol[mask]="A0"
			indexNamesArr=pd.unique(df.symbol)
			indexNamesArr=sorted(indexNamesArr)

			mm=df[naml[i]]<=0.1
			df[naml[i]][mm]=0.1
			mm1=df[naml[j]]<=0.1
			df[naml[j]][mm1]=0.1
			
			if YN==xmin.get():
				print(indexNamesArr)
				for k, varnames in enumerate(indexNamesArr):
					mask = df["symbol"] == varnames
					aass=df[mask]
					aass['color']=co()
					if varnames=="A0":
						aass['color']="gray"
						plt.scatter(aass[naml[i]], aass[naml[j]], alpha=0.3,s=5,marker="o",c=aass['color'],label="no annotation")
					else :
						plt.scatter(aass[naml[i]], aass[naml[j]], alpha=1,s=20,marker="*",c=aass['color'],label=varnames)
				plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.,fontsize=4)
			else :
				plt.scatter(df[naml[i]], df[naml[j]], alpha=1,s=5,marker="p",c="black")
			plt.xscale("log")
			plt.yscale("log")
			plt.xlabel(naml[i], fontsize=12, fontname="sans-serif", fontweight="bold")
			plt.ylabel(naml[j], fontsize=12, fontname="sans-serif", fontweight="bold")
			#plt.xlim(10**(-1),10**5)
			#plt.ylim(10**(-1),10**5)
			#
			c=SaveDirectory+'\\'+na1+'.png'
			print(c)
			plt.savefig(c, dpi=200)
			plt.clf()

root = Tk()
root.title('ScatterPlot')
path = StringVar()

xmin = DoubleVar()
xmin.set(1)
Label(root, text='Color: ').grid(row = 0, column = 0)
Checkbutton(root,text='有',variable=xmin, onvalue=1, offvalue=0).grid(row = 0, column = 1)

Label(root,text = "目標路徑:").grid(row = 1, column = 0)
Entry(root, textvariable = path).grid(row = 1, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 1, column = 2)

root.mainloop()