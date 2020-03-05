#!/usr/bin/env python
# coding: utf-8

# # Wage Function with Interaction

# In[3]:


import numpy as np
import pandas as pd
import pylab
import os
cwd = os.getcwd()
cwd
os.chdir("/Users/lcald_000/Desktop")


import scipy.stats as stats
import sklearn
file = 'W.xls'
xl = pd.ExcelFile(file)
print(xl)
df1 = xl.parse('WAGE1')


# In[4]:


print(df1)


# In[8]:


from sklearn.linear_model import LinearRegression

X = df1.drop('wage', axis=1)
lm = LinearRegression()
lm.fit(X, df1.wage)
LinearRegression(copy_X=True, fit_intercept=True, normalize=False)


# In[9]:


print('Estimate intercept coefficient:', lm.intercept_)


# In[10]:


print('Number of coefficients:'), len(lm.coef_)


# In[11]:


print('Coefficients: \n', lm.coef_)
