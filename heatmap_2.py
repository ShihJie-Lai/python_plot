#!/usr/bin/env python
"""
Annotate a group of y-tick labels as such.
"""
import seaborn as sns
import numpy as np
import pandas as pd
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
import cv2
import re
import os
import random
from scipy.spatial import distance 
from scipy.cluster import hierarchy
from sklearn import datasets
import matplotlib.pyplot as plt
from matplotlib.transforms import TransformedBbox

def annotate_yranges(groups, ax=None):
    """
    Annotate a group of consecutive yticklabels with a group name.

    Arguments:
    ----------
    groups : dict
        Mapping from group label to an ordered list of group members.
    ax : matplotlib.axes object (default None)
        The axis instance to annotate.
    """
    if ax is None:
        ax = plt.gca()
    label2obj = {ticklabel.get_text() : ticklabel for ticklabel in g.ax_heatmap.get_yticklabels()}
    print(label2obj)
    for ii, (group, members) in enumerate(groups.items()):
        first = members[0]
        last = members[-1]
        print(label2obj[first])
        bbox0 = _get_text_object_bbox(label2obj[first], ax)
        bbox1 = _get_text_object_bbox(label2obj[last], ax)
        print(bbox0.y0)
        set_yrange_label(group, bbox0.y0 + bbox0.height/2,
                         bbox1.y0 + bbox1.height/2,
                         min(bbox0.x0, bbox1.x0),
                         2,
                         ax=ax)


def set_yrange_label(label, ymin, ymax, x, dx=-0.5, ax=None, *args, **kwargs):
    """
    Annotate a y-range.

    Arguments:
    ----------
    label : string
        The label.
    ymin, ymax : float, float
        The y-range in data coordinates.
    x : float
        The x position of the annotation arrow endpoints in data coordinates.
    dx : float (default -0.5)
        The offset from x at which the label is placed.
    ax : matplotlib.axes object (default None)
        The axis instance to annotate.
    """

    if not ax:
        ax = plt.gca()

    dy = ymax - ymin
    props = dict(connectionstyle='angle, angleA=270, angleB=0, rad=0',
                 arrowstyle='-',
                 shrinkA=10,
                 shrinkB=10,
                 lw=1)
    ax.annotate(label,
                xy=(x+4, ymin),
                xytext=(x+4 + dx, ymin + dy/2),
                annotation_clip=False,
                arrowprops=props,
                *args, **kwargs,
    )
    ax.annotate(label,
                xy=(x+4, ymax),
                xytext=(x+4 + dx, ymin + dy/2),
                annotation_clip=False,
                arrowprops=props,
                *args, **kwargs,
    )


def _get_text_object_bbox(text_obj, ax):
    # https://stackoverflow.com/a/35419796/2912349
    transform = ax.transData.inverted()
    # the figure needs to have been drawn once, otherwise there is no renderer?
    plt.ion(); plt.show(); plt.pause(0.001)
    bb = text_obj.get_window_extent(renderer = ax.get_figure().canvas.renderer)
    # handle canvas resizing
    return TransformedBbox(bb, transform)


#if __name__ == '__main__':

import numpy as np

fig, ax = plt.subplots(1,1)

    # so we have some extra space for the annotations
fig.subplots_adjust(right=0.3)

# data = np.random.rand(10,10)
# ax.imshow(data)

# ticklabels = 'abcdefghij'
# ax.set_yticks(np.arange(len(ticklabels)))
# ax.set_yticklabels(ticklabels)

# groups = {
        # 'abc' : ('a', 'b', 'c'),
        # 'def' : ('d', 'e', 'f'),
        # 'ghij' : ('g', 'h', 'i', 'j')
# }


cmap = sns.diverging_palette(133, 10, n=11, sep=20, as_cmap=True, center="dark")

rows = pd.read_csv("NGS1050240_heatmap_3.csv")
df = rows.set_index(rows.columns[0])
indexNamesArr = df.index.values
g=sns.clustermap(df, metric="correlation", cmap=cmap, method="single",z_score=0, xticklabels=True, yticklabels=True, col_cluster=False, row_cluster=False)
#plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)
ax1 = g.ax_heatmap
ax1.set_ylabel("")


ax.set_yticks(np.arange(len(indexNamesArr)))
ax.set_yticklabels(indexNamesArr)

groups = {
        'A' : (indexNamesArr[0:12].astype(str)),
        'B' : (indexNamesArr[12:26].astype(str))
}

print(groups)
annotate_yranges(groups)

plt.savefig("aa.png",dpi=500)
plt.show()