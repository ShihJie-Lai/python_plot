import pandas as pd
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
# def ratio(m,m):
	# for x,y in list(zip(m,n))
		# if 




def callback():
    # Entry 有個get() 方法用來獲取輸入框的值
	#text = entry.get()
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	rows = pd.read_csv(csvfile)
	df = rows.set_index('gene')
	df
	columnsNamesArr = rows.columns.values
	rows["FC1"]=[ "red" if np.log2(x/y)<-1; y elif np.log2(x/y)>1  elif "grey"  for x,y in list(zip(rows[columnsNamesArr[1]],rows[columnsNamesArr[2]]))]
	#"blue" elif np.log2(x/y)<(-1)
	plt.figure(figsize=(7,5))
	plt.style.use("ggplot") 
	plt.xlabel(columnsNamesArr[1], fontweight = "bold")
	plt.ylabel(columnsNamesArr[2], fontweight = "bold")
	plt.title("The difference of miRNA profile",fontsize = 15, fontweight = "bold")
	plt.scatter(np.log10(rows[columnsNamesArr[1]]),                # x軸資料
            np.log10(rows[columnsNamesArr[2]]),     # y軸資料
            c = rows["FC1"],                                  # 點顏色
            s = 50,                                   # 點大小
            alpha = .5,                               # 透明度
            marker = "o")                             # 點樣式
	#plt.savefig("The difference of miRNA profile.jpg")   		
			
	# Prepare a vector of color mapped to the 'cyl' column
	#my_palette = dict(zip(df.cyl.unique(), ["orange","yellow","brown"])), row_colors=row_colors, standard_scale=1
	#row_colors = df.cyl.map(my_palette)
	# plot
	#sns.set(font_scale=0.6)
	#g=sns.clustermap(df, metric="correlation", cmap="RdBu", method="single",z_score=0, xticklabels=True, yticklabels=True, center=1)
	plt.show()
	

root = Tk()
root.title('heatmap')
path = StringVar()

Label(root,text = "目標路徑:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1)
Button(root, text = "路徑選擇", command = callback).grid(row = 0, column = 2)


root.mainloop()