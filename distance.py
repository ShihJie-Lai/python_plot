from scipy.spatial import distance
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import re
import os

def callback():
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	print(csvfile)
	b=re.search('/(\w+)\.',csvfile).group(1)
	rows = pd.read_csv(csvfile)
	df = rows.set_index('gene_id')
	
	A=[[0]*len(df.columns) for i in range(len(df.columns))]
	for i in range(len(df.columns)):
		for j in range(len(df.columns)):
			B1=distance.cosine(df[df.columns[i]], df[df.columns[j]])
			A[i][j]=B1
			A[j][i]=B1
	df2=pd.DataFrame(A,index=df.columns,columns=df.columns)
	sns.set(font_scale=0.6)
	cmap = sns.light_palette('red', as_cmap=True)
	if YN.get()==1 :
		g=sns.clustermap(df2, metric="correlation", cmap=cmap, method="single",z_score=None, xticklabels=True, yticklabels=True, col_cluster=False, row_cluster=False,annot=True)
	else :
		g=sns.clustermap(df2, metric="correlation", cmap=cmap, method="single",z_score=None, xticklabels=True, yticklabels=True, col_cluster=True, row_cluster=True,annot=True)
	c=SaveDirectory+'\\'+b+'_distance.png'
	print(c)
	plt.savefig(c, dpi=1000)
	plt.show()

root = Tk()
root.title('Distance plot')
path = StringVar()
YN = DoubleVar()
YN.set(0)
Label(root, text='cluster: ').grid(row = 0, column = 0)
Checkbutton(root, text='Yes', variable=YN, onvalue=0, offvalue=1).grid(row = 0, column = 1)

Label(root,text = "目標路徑:").grid(row = 1, column = 0)
Entry(root, textvariable = path).grid(row = 1, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 1, column = 2)

#

root.mainloop()