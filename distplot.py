import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tkinter import *
from tkinter.filedialog import askopenfilename
import re
import os
import math


def distp(table="dataset_file"):
    d = pd.read_csv(table, sep=",")
    aa = d.columns
    for i, varnames in enumerate(aa):
     sns.distplot(np.log(d[varnames]), hist = False,label = varnames)#, kde = True,kde_kws = {'linewidth': 3}
    plt.legend(prop={'size': 8})
    plt.title('Density Plot')
    plt.xlabel('log(TPM)')
    plt.ylabel('Density')

def callback():
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	b=re.search('/(\w+)\.',csvfile).group(1)
	distp(table=csvfile)
	c=SaveDirectory+'\\'+b+'_distplot.png'
	print(c)
	plt.savefig(c, dpi=500)
	plt.show()	

root = Tk()
root.title('distplot')

path = StringVar()
Label(root,text = "目標路徑:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 0, column = 2)

root.mainloop()