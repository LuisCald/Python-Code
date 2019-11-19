# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 23:29:36 2019

@author: Jrxz12
"""

""" An introductory session to graphics.
    
"""

import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import numpy as np
import os

# Graphics package
import seaborn as sns

# Importing dataset
input_base_path = r"C:\Users\Jrxz12\Desktop\Code\Stata\Datasets"
df = pd.read_stata(os.path.join(input_base_path, "September20.dta"))

# Scatter PLots
df_random = np.random.randn(100,2) # Generating df
x = df_random[:,0] # x-axis variable
y = df_random[:,1] # y-axis variable
plt.scatter(x,y) # scatter x, y

plt.scatter(x, y, s=5) # "s" alters "size" of point
plt.scatter(x,y, s=5, c='r') # "c" is color

# Details on labeling is in "Functions and Graphs.ipynb"

# Bar Graphs
y = np.random.randn(10)
x = np.arange(10) # spits list of consecutive numbers less than 10
plt.bar(x,y) # creates bar graph
plt.bar(x,y, width= 0.5) # "width" changes bar width
plt.barh(x,y) # "barh" for horizontal bar graphs

# sns is known for its color palettes
colors = sns.color_palette('colorblind')
plt.bar(x,y, width= 2, color= colors) # Takes same arguments as above

# Pie charts
y = abs(np.random.randn(5)) # to get 5 positive numbers
plt.pie(y, autopct='%.2f') # a format has been applied

# Pie chart with percent and number
values = [3, 12, 5, 8]
labels = ['a', 'b', 'c', 'd']

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

plt.pie(values, labels=labels, autopct=make_autopct(values))
plt.show()
