# Libraries
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import re
import os
#import random
from scipy.spatial import distance 
from scipy.cluster import hierarchy
from sklearn import datasets
from random import randint

def callback():
    # Entry 有個get() 方法用來獲取輸入框的值
	#text = entry.get()
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	print(csvfile)
	b=re.search('/(\w+)\.',csvfile).group(1)
	#re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(0)
	rows = pd.read_csv(csvfile)
	#df = rows.set_index('Gene')
	df = rows.set_index(rows.columns[0])
	df
	indexNamesArr = df.index.values
	#sns.set(font_scale=1)
	cmap = sns.diverging_palette(133, 10, n=11, sep=20, as_cmap=True, center="dark")
	sys.setrecursionlimit(3000)
	
	#hierarchy.dendrogram(row_linkage,labels=df.index)
	#plt.title('Hierarchical Clustering')
	
	
	if lfc_thr.get()==2:
		a1=None
		p_25=-10
		p_75=10
		for j, varnames2 in enumerate(df.columns):	
			p = np.percentile(df[varnames2], 100)
			q = np.percentile(df[varnames2], 0)
			if p<p_75 :
				p_75=p
			if q>p_25 :
				p_25=q
		#g=sns.clustermap(df, metric="correlation", cmap=cmap, method="single",z_score=a1, xticklabels=col_lab.get(), yticklabels=row_lab.get(), col_cluster=col_cluster.get(), row_cluster=row_cluster.get(),vmin=p_25, vmax=p_75)
		g=sns.clustermap(df, metric="correlation", cmap=cmap, method="single",z_score=a1, xticklabels=col_lab.get(), yticklabels=row_lab.get(), col_cluster=col_cluster.get(), row_cluster=row_cluster.get(),vmin=q, vmax=p)
		#
		#g=sns.heatmap(df, vmin=-10, vmax=10, cmap=cmap,cbar_kws=dict(use_gridspec=False,location="bottom"))#
		#g.xaxis.tick_top() # x axis on top
		#g.xaxis.set_label_position('top')
		#for i, varnames in enumerate(indexNamesArr):
			#for j, varnames2 in enumerate(df.columns):
				#aa=random.random() 
				#print(df[varnames2][varnames])
				#if df[varnames2][varnames]>5:
				#	df[varnames2][varnames]=5+aa
				#elif df[varnames2][varnames]<(-5):
				#	df[varnames2][varnames]=-5-aa
	else:
		a1=lfc_thr.get()
		g=sns.clustermap(df, metric="correlation", cmap=cmap, method="single",z_score=a1, xticklabels=col_lab.get(), yticklabels=row_lab.get(), col_cluster=col_cluster.get(), row_cluster=row_cluster.get())
	c=SaveDirectory+'\\'+b+'_heatmap_'+str(a1)+'.png'
	plt.savefig(c,dpi=500)
	#sns.heatmap(df)
	#plt.set_size_inches(2000, 1600, forward=True)
	plt.show()

    #print(text)
#
# root = Tk()"RdYlGn", center=1
# root.title('heatmap')
# root.geometry('800x800')
# entry = Entry(root)
# entry.pack()
# button = Button(root, text='enter', command=callback)
# button.pack()
# root.mainloop()


root = Tk()
root.title('heatmap')
path = StringVar()

col_cluster = BooleanVar()
row_cluster = BooleanVar()
col_cluster.set(True)
row_cluster.set(True)
Label(root,text = "群集:").grid(row = 0, column = 0)
Checkbutton(root,text = 'col_cluster',variable = col_cluster).grid(row = 0, column = 1)
Checkbutton(root,text = 'row_cluster',variable = row_cluster).grid(row = 0, column = 2)

col_lab = BooleanVar()
row_lab = BooleanVar()
col_lab.set(True)
row_lab.set(True)
Label(root,text = "標籤:").grid(row = 1, column = 0)
Checkbutton(root,text = 'col_label',variable = col_lab).grid(row = 1, column = 1)
Checkbutton(root,text = 'row_label',variable = row_lab).grid(row = 1, column = 2)

lfc_thr = DoubleVar()
lfc_thr.set(0)
Label(root,text = "標準化:").grid(row = 2, column = 0)
Radiobutton(root,text = 'row',variable = lfc_thr,value = 0).grid(row = 3, column = 0)
Radiobutton(root,text = 'column',variable = lfc_thr,value = 1).grid(row = 3, column = 1)
Radiobutton(root,text = 'None',variable = lfc_thr,value = 2).grid(row = 3, column = 2)

Label(root,text = "目標路徑:").grid(row = 4, column = 0)
Entry(root, textvariable = path).grid(row = 4, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 4, column = 2)


root.mainloop()
#csvfile=sys.argv[1]
#filetype=( ("CSV file", "*.csv*"),("HTML files", "*.html;*.htm"))