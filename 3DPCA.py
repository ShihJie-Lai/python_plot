import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

def pcaplot(x="x", y="y", z="z", labels="d_cols", var1="var1", var2="var2", var3="var3",name="c",YN="YN"):
    

	
	cc=["red","red","blue","blue","y","y","green","green","pink","pink","k","k"]
	
	for i, varnames in enumerate(labels):
		plt.scatter(x[i], y[i], label=varnames.replace('_count','').replace('_FPKM',''),c=cc[i])
		if YN==1:
			plt.text(x[i], y[i], varnames.replace('_count','').replace('_FPKM',''), fontsize=5)

	plt.xlabel("PC1 ({}%)".format(var1), fontsize=12, fontname="sans-serif")
	plt.ylabel("PC2 ({}%)".format(var2), fontsize=12, fontname="sans-serif")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=5)
	plt.tight_layout()
	plt.savefig(name+'pcaplot_2d.png', format='png', bbox_inches='tight', dpi=800)
	plt.close()
#
    # for 3d plot
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for i, varnames in enumerate(labels):
		ax.scatter(x[i], y[i], z[i],label=varnames.replace('_count','').replace('_FPKM',''),c=cc[i])
		if YN==1:
			texts = ax.text(x[i], y[i], z[i], varnames.replace('_count','').replace('_FPKM',''), fontsize=5)

	ax.set_xlabel("PC1 ({}%)".format(var1), fontsize=12, fontname="sans-serif")
	ax.set_ylabel("PC2 ({}%)".format(var2), fontsize=12, fontname="sans-serif")
	ax.set_zlabel("PC3 ({}%)".format(var3), fontsize=12, fontname="sans-serif")
	ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=5)
	plt.tight_layout()
	plt.savefig(name+'pcaplot_3d.png', format='png', bbox_inches='tight',  dpi=800)
    #plt.close()

def callback():
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	b=re.search('/(\w+)\.',csvfile).group(1)
	#re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(0)
	rows = pd.read_csv(csvfile)
	#x=StandardScaler().fit_transform(rows)
	
	
	pca_out = PCA()
	pca_out.fit(rows)
	pca_out.transform(rows)
	prop_var = pca_out.explained_variance_ratio_
	rotation = pca_out.components_
	
	# rows = pd.read_csv(csvfile)
	# scaler = StandardScaler()
	# scaler1 = scaler.fit(rows)
	# print(scaler1)
	# X_train_std=scaler1.transform(rows)
	# print(X_train_std)
	# pca = PCA(n_components=3)
	# pca_std = pca.fit(X_train_std)
	# x_new=pca_std.fit_transform(X_train_std)    
	# print(x_new)
	
	# la =pca.explained_variance_ratio_
	res = format(prop_var[0], '.2%')
	res1 = format(prop_var[1], '.2%')
	res2 = format(prop_var[2], '.2%')
	aa=rows.columns
	c=SaveDirectory+'\\'+b
	pcaplot(x=rotation[0], y=rotation[1], z=rotation[2], labels=aa, var1=res, var2=res1, var3=res2,name=c,YN=YN.get())
	
	#print(c)
	#plt.savefig(c, dpi=500)
	#sns.heatmap(df)
	#plt.set_size_inches(2000, 1600, forward=True)
	plt.show()

root = Tk()
root.title('PCA3D')
YN = DoubleVar()
path = StringVar()

Label(root, text='plot text on maps: ').grid(row = 0, column = 0)
Checkbutton(root, text='Yes', variable=YN, onvalue=1, offvalue=0).grid(row = 0, column = 1)
Label(root,text = "目標路徑:").grid(row = 1, column = 0)
Entry(root, textvariable = path).grid(row = 1, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 1, column = 2)

root.mainloop()
