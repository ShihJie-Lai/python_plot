import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import re
import os
from adjustText import adjust_text
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cmc


def callback():
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	b=re.search('/(\w+)\.',csvfile).group(1)
	#re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(0)
	rows = pd.read_csv(csvfile)
	scaler = StandardScaler()
	scaler.fit(rows)
	rows1=scaler.transform(rows)    
	pca = PCA()
	x_new = pca.fit_transform(rows1)
	la =pca.explained_variance_ratio_
	res = format(la[0], '.2%')
	res1 = format(la[1], '.2%')
	aa=rows.columns
	def myplot(score,coeff,labels=None):
		xs = coeff[:,0]
		ys = coeff[:,1]
		n = coeff.shape[0]
		plt.scatter(coeff[:,0],coeff[:,1], c='r')
		if labels is None:
			texts = [plt.text(coeff[i,0], coeff[i,1], "Var"+str(i+1), color = 'b') for i in range(n)]
			adjust_text(texts)
		else:
			texts = [plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i].replace('_count','').replace('_FPKM',''), color = 'b', ha = 'center', va = 'center') for i in range(n)]
			adjust_text(texts)
		plt.xlim(xs.min()-.25,xs.max()+.25)
		plt.ylim(ys.min()-.25,ys.max()+.25)
		plt.xlabel("PC{}".format(str(1)+'('+res+')'))
		plt.ylabel("PC{}".format(str(2)+'('+res1+')'))
		plt.grid()
	myplot(x_new[:,0:2],np.transpose(pca.components_[0:2, :]),aa)
	c=SaveDirectory+'\\'+b+'_pca.png'
	print(c)
	plt.savefig(c, dpi=500)
	#sns.heatmap(df)
	#plt.set_size_inches(2000, 1600, forward=True)
	plt.show()
	
	



#Call the function. Use only the 2 PCs.



root = Tk()
root.title('PCA')
path = StringVar()

Label(root,text = "目標路徑:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 0, column = 2)


root.mainloop()
#csvfile=sys.argv[1]
#filetype=( ("CSV file", "*.csv*"),("HTML files", "*.html;*.htm"))
