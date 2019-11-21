#!/usr/bin/env python
# coding: utf-8

# # Appendix C

# # Other Stat stuff

# ## Example C-1

# In[2]:


import plotly.plotly as py
import plotly
plotly.tools.set_credentials_file(username='jrxz12', api_key='uSstQZx74IIp7rf1pqZv')
import plotly.graph_objs as go

index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
outcome = [5.1, 5.4, 6, 7, 8, 2.3, 3.2, 5, 1, 2.4]
trace = go.Table(
    header=dict(values=['City', 'Unemployment Rate']),
    cells=dict(values=[index, outcome]))
data = [trace]
py.iplot(data, filename='basic_table')


# In[9]:


import numpy as np
import statsmodels.api as sm
import scipy.stats as stats
import matplotlib.pyplot as plt

mu = 0
sigma = 1
x = np.arange(-5, 5, 0.1)
y = stats.norm.pdf(x, 0, 1)
z = stats.norm.pdf(x, 1, 1)
plt.plot(x, y)
plt.plot(x, z)
plt.xlabel("W")
plt.ylabel("f(W)")
plt.xticks([0, 1], ['$E(W)$', '$E(W2)$'])
plt.title('Figure C.1 An unbiased estimator, W1, and an estimator with positive bias, W2')
plt.show()

mu = 0
sigma = 1
x = np.arange(-5, 5, 0.1)
y = stats.norm.pdf(x, 0, 1)
z = stats.norm.pdf(x, 0, 2)
plt.plot(x, y)
plt.plot(x, z)
plt.xlabel("W")
plt.ylabel("f(W)")
plt.xticks([0], ['$E(W)$'])
plt.title('Figure C.2 Two unbiased estimators')
plt.show()
