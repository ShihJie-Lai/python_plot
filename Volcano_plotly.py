import chart_studio.plotly as py
import plotly.express as go
#import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys
import cv2
import re
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
import math

def volcano(table="dataset_file", lfc="log2FC", pv="p-value", lfc_thr=1, pv_thr=0.05,xmin=-10,xmax=10,line=1,colup="red",coldown="blue",YN=1,Pa="file.html"):
	d = pd.read_csv(table, sep=",")
	d.loc[(d["log2FC"] >= lfc_thr) & (d["p-value"] < pv_thr), 'sign'] = 'Up sign'  # upregulated
	d.loc[(d["log2FC"] <= -lfc_thr) & (d["p-value"] < pv_thr), 'sign'] = 'Down sign'  # downregulated
	d.loc[(d["log2FC"] > xmax), "log2FC"] = xmax  # upregulated
	d.loc[(d["log2FC"] < xmin), "log2FC"] = xmin  # downregulated
	d['sign'].fillna('No sign', inplace=True)  # intermediate
	d['logpv'] = -(np.log10(d["p-value"]))
	d["symbol"] = d["symbol"].fillna(" ")
	print(d)
	if YN!=1:
		trace = go.scatter(d,x="log2FC", y="logpv", color="sign",color_discrete_map={'Up sign': colup,'No sign': 'black','Down sign': coldown},width=1500, height=1000, custom_data=["GeneNames"])
	else :
		trace = go.scatter(d,x="log2FC", y="logpv",text="symbol", color="sign",color_discrete_map={'Up sign': colup,'No sign': 'black','Down sign': coldown},width=2000, height=1000, custom_data=['GeneNames'])
		trace.update_traces(textposition='top center')
	if line==1:
		trace.add_shape(type="line",x0=-lfc_thr, y0=0, x1=-lfc_thr, y1=max(d['logpv']),line=dict(color="RoyalBlue",width=3,dash="dot"))
		trace.add_shape(type="line",x0=lfc_thr, y0=0, x1=lfc_thr, y1=max(d['logpv']),line=dict(color="RoyalBlue",width=3,dash="dot"))
		trace.add_shape(type="line",x0=xmin, y0=-(np.log10(pv_thr)), x1=xmax, y1=-(np.log10(pv_thr)),line=dict(color="RoyalBlue",width=3,dash="dot"))
	trace.update_layout(
		title="Volcano Plot",
		xaxis_title='log2 Fold Change',
		yaxis_title="-log10(P-value)",
		font=dict(
			family="Courier New, monospace",
			size=18,
			color="RebeccaPurple"),
		legend=dict(orientation="h",
			yanchor="bottom",
			y=1.02,
			xanchor="right",
			x=1
		),
		margin=dict(l=20, r=20, t=20, b=30),
		paper_bgcolor="LightSteelBlue",
    )
	trace.update_traces(hovertemplate='log2FC: %{x} <br>-log10(P-value): %{y}<br>gene_id: %{customdata[0]}') #
	trace.show()
	trace.write_html(Pa)

def callback():
	text = askopenfilename(filetype = (("CSV files", "*.csv"),("","")))
	csvfile=text
	SaveDirectory = os.getcwd()
	b=re.search('/(\w+)\.',csvfile).group(1)
	c=SaveDirectory+'\\'+b+'_Volcano.html'
	print(c)	
	volcano(table=csvfile, lfc="log2FC", pv="p-value", lfc_thr=lfc_thr.get(), pv_thr=pv_thr.get(),xmin=xmin.get(),xmax=xmax.get(),line=var1.get(),colup=colup.get(),coldown=coldown.get(),YN=var2.get(),Pa=c)
	
root = Tk()
root.title('volcano')
lfc_thr = DoubleVar()
lfc_thr.set(1)
pv_thr = DoubleVar()
pv_thr.set(0.05)
Label(root, text='Cut log2(Fold Change): ').grid(row = 0, column = 0)#创建一个`label`名为`User name: `置于坐标（50,150）
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