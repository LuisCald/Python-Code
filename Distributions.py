#!/usr/bin/env python
# coding: utf-8

# ## Figure B.1

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (8, 5)

plt.xticks([-1, 0, 1, 2, 3], ['$-1$', '$0$', '$1$', '$2$', '$3$'])
plt.yticks([0, .5], ['$0$', '$.5$'])
plt.xlabel("x")
plt.ylabel("f(x)")
plt.axvline(x=0, ymin=0, ymax=.22)
plt.axvline(x=1, ymin=0, ymax=.44)
plt.axvline(x=2, ymin=0, ymax=.36)
plt.text(0, .23, '.22')
plt.text(1, .45, '.44')
plt.text(2, .37, '.36')
plt.title('Figure B.1')
plt.show()


# ## Making Probability Distribution Curves

# In[4]:


import statsmodels.api as sm
import scipy.stats as stats

prob_under_minus1 = stats.norm.cdf(x=-1, loc=0, scale=1)
prob_over_1 = 1 - stats.norm.cdf(x=1, loc=0, scale=1)
between_prob = 1 - (prob_under_minus1 + prob_over_1)

print(prob_under_minus1, prob_over_1, between_prob)

plt.rcParams["figure.figsize"] = (9, 9)

plt.fill_between(x=np.arange(-4, -1, .01),
                 y1=stats.norm.pdf(np.arange(-4, -1, .01)) ,
                 facecolor='red',
                 alpha=0.35)

plt.fill_between(x=np.arange(1, 4, 0.01),
                 y1=stats.norm.pdf(np.arange(1, 4, 0.01)) ,
                 facecolor='red',
                 alpha=0.35)

plt.fill_between(x=np.arange(-1, 1, 0.01),
                 y1=stats.norm.pdf(np.arange(-1, 1, 0.01)) ,
                 facecolor='blue',
                 alpha=0.35)

plt.text(x=-1.8, y=0.03, s=round(prob_under_minus1, 3))
plt.text(x=-0.2, y=0.1, s=round(between_prob, 3))
plt.text(x=1.4, y=0.03, s=round(prob_over_1, 3))
print(stats.norm.ppf(.95))


plt.rcParams["figure.figsize"] = (9, 9)

plt.fill_between(x=np.arange(-1, 1, 0.01),
                 y1=stats.norm.pdf(np.arange(-1, 1, 0.01)) ,
                 facecolor='black',
                 alpha=0.35)

plt.fill_between(x=np.arange(1, 2, 0.01),
                 y1=stats.norm.pdf(np.arange(1, 2, 0.01)) ,
                 facecolor='red',
                 alpha=0.35)

plt.fill_between(x=np.arange(2, 4, 0.01),
                 y1=stats.norm.pdf(np.arange(2, 4, 0.01)) ,
                 facecolor='black',
                 alpha=0.35)
plt.xticks([-1, 0, 1, 2, 3, 4], ['-1', '0', 'a', 'b', '3', '4'])
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title('Figure B.2 The probability that X lies between the points a and b')

bball = 1
make = .8
mp = make / bball
twice = mp * mp
print(round(twice, 3))


# # Other

# In[18]:


plt.rcParams["figure.figsize"] = (9, 9)

plt.fill_between(x=np.arange(-4, 4, 0.01),
                 y1=stats.norm.pdf(np.arange(-4, 4, 0.01)),
                 facecolor='orange',
                 alpha=0.35)


plt.xticks(
    [-4, -3, -2, -1, 0, 1, 2, 3, 4],
    ['$-4$', '$-3$', '$-2$', '$-1$', '$0$', '$1$', '$2$', '$3$', '$4$']
)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title('Normal Distribution')


# The above distribution is symmetric, indicating the mean and median are equivalent.

# In[2]:


import numpy as np
# When making sets, python reads them up top-bottom. The 5.333 represents the mean of [3,4,6].

A = [3, 4, 6]
B = [4, 6, 8]
C = [9, 1, 5]
Set = np.array([A, B, C])  # Creates a Matrix from top to bottom
Mean = np.mean(Set, axis=0)  # When axis =0, average of column
Mean1 = np.mean(Set, axis=1)  # When axis =1, average of row
print(Mean, Mean1)


# In[29]:


Standard_deviation = np.std(Set, axis=0)
print(Standard_deviation)


# In[35]:


# In the new python there is a new statistics package. For now, we use numpy
variance = np.var(A)
print(variance)
covariance = np.cov(A)
print(covariance)

correlation_coefficient = np.corrcoef(A, B)[0, 0]

print(correlation_coefficient)

# Kurtosis and Skewness were discussed in the section. Kurtosis describes the tails of the distribution and hints at its
# peak. The greater the kurtosis, the greater the potential for outliers. Skewness just describes the data's asymmetry.
import numpy as np
import pylab
import matplotlib.pyplot as plt
x = np.linspace(0, 24)
plt.rcParams['figure.figsize'] = (8, 5)

plt.xticks([4, 8, 12, 16, 20, 24], ['4', '8', '12', '16', '20'])
plt.yticks([0, 1], ['0', '1'])
plt.xlabel("EDUC")
plt.ylabel("E(WAGE|EDUC)")

plt.axvline(x=4, ymin=0, ymax=.22)
plt.axvline(x=8, ymin=0, ymax=.30)
plt.axvline(x=12, ymin=0, ymax=.36)
plt.axvline(x=16, ymin=0, ymax=.55)
plt.axvline(x=20, ymin=0, ymax=.80)

plt.title('Figure B.5')
plt.show()


# In[46]:


x = np.arange(0, 20, .1)
y = 10 / x
plt.rcParams['figure.figsize'] = (11, 4)

plt.xticks([1, 5, 10], ['$1$', '$5$', '$10$'])
plt.xlabel("x")
plt.ylabel("E(Y|x)")

plt.plot(x, y, '-b', label=r'$housing= 164 + .27income$')
plt.legend(loc='best')
plt.annotate(
    'E(Y|X) = 10/x', xy=(1.5, 7), xytext=(3, 15),
    arrowprops=dict(facecolor='black', shrink=5)
)
plt.title('Figure B.6 Graph of E(Y|X)=10/x')
plt.show()


# In[55]:


x = np.arange(0, 20, .1)
y = x
plt.rcParams['figure.figsize'] = (11, 4)

# plt.xticks([1, 5, 10],
# ['$1$', '$5$', '$10$'])
# plt.xlabel("x")
# plt.ylabel("E(Y|x)")

plt.plot(x, y, '-w')  # w for white
# plt.plot(x, y, '-w', label=r'$housing= 164 + .27income$')
plt.legend(loc='best')
plt.annotate(
    'FD', xy=(2, 10), xytext=(.1, 10),
    arrowprops=dict(facecolor='black', shrink=1)
)
plt.annotate('FD', xy=(2, 7), xytext=(.1, 10),
             arrowprops=dict(facecolor='black', shrink=1)
             )
plt.annotate('efficicient markets & cheaper services', xy=(11, 10), xytext=(2, 10), arrowprops=dict(facecolor='black', shrink=4))
plt.annotate('Financial Firms', xy=(11, 10), xytext=(2, 13), arrowprops=dict(facecolor='black', shrink=4))
plt.annotate('S', xy=(.1, 10), xytext=(.1, 5), arrowprops=dict(facecolor='black', shrink=4))
plt.annotate('S', xy=(2, 7), xytext=(.1, 5), arrowprops=dict(facecolor='black', shrink=4))

plt.annotate('Institutional day', xy=(11, 10), xytext=(2, 7))
plt.annotate('gains', xy=(11.2, 10), xytext=(11.2, 10))
plt.plot(11.2, 9.5, 'o')
plt.plot(2, 6.3, 'o')
plt.annotate('gains', xy=(15, 13), xytext=(11.2, 10), arrowprops=dict(facecolor='black', shrink=4))
plt.annotate('gains', xy=(15, 10), xytext=(11.2, 10), arrowprops=dict(facecolor='black', shrink=4))
plt.annotate('Wealth Returns', xy=(15, 10), xytext=(15, 10))
plt.annotate('Renumeration', xy=(15, 10), xytext=(15, 13))

plt.title('Something I was Trying')
plt.axis('off')
plt.plot('off')
plt.show()


# In[64]:


data = np.random.randn(1000)
values, base = np.histogram(data, bins=100)

cumulative = np.cumsum(values)

plt.plot(base[:-1], cumulative, c='b')
plt.yticks([0, 1000], ['0', '1'])
plt.show()


# In[141]:


import scipy.stats
q = stats.norm(0, .1).pdf(4)  # Tells me the likelihood that this x will be in that sample. But really it is just the derivative of the cdf.
print(q)
# information on the probabilty density function
# For continuous random variable, the probability that it takes on
# a paritcular value is ZERO
# We have to find the probability that it falls under some interval
# A probability density function is created from a sample.
# If for example, you get 100 burgers, you want to see the
# spectrum of its weight possibly. You find the mean and see
# how each burger differs from the mean. This creates a histogram which
# displays relative frequency. Relative frequency depends on the weight of the burger. For example, the quarter pounder burger weighed .27 lets say. Theres 4 that weighed that much. But what about .274?
# The point is that this is a continuous variable so eventually the bars that make your histogram of relative frequencies become a curve. This curve is the probability density function.
# This tells me the probability that x is close to a single number.


# In[153]:


mu = 0
sigma = 1
x = np.arange(-5, 5, 0.1)
y = stats.norm.pdf(x, 0, 1)
z = stats.norm.pdf(x, 0, 2)
zz = stats.norm.pdf(x, 0, 5)

# If you have a legend in mind, just write label and do the following
plt.plot(x, zz, label='5')
plt.plot(x, y, label='1')
plt.plot(x, z, label='2')
plt.legend(loc='best')
plt.show


# Shows how the change in variance changes the distribution.

# Finding the probability of a continous random variable.

# In[154]:


x = np.linspace(0, 5, 1000)
fig, ax = plt.subplots(1, 1)

linestyles = [':', '--', '-.', '-']
deg_of_freedom = [1, 2, 4, 8]
for df, ls in zip(deg_of_freedom, linestyles):
    ax.plot(x, stats.chi2.pdf(x, df), linestyle=ls, label=r'$df=%i$' % df)

plt.xlim(0, 5)
plt.ylim(0, .5)

plt.xlabel(r'$\chi^2$')
plt.ylabel(r'$f(\chi^2)$')
plt.title(r'$\chi^2 Distribution$')

plt.legend()
plt.show()


# In[155]:


# To solve chi-squared and p value. It reads it like standard deviation
from scipy.stats import chisquare
chisquare([A, B, C])


# In[156]:


from scipy.stats import f as fisher_f
mu = 0
d1 = [1, 5, 2, 10]
d2 = [1, 2, 5, 50]
ls = ['-', '--', ':', '-.']
x = np.linspace(0, 5, 1001)[1:]


for (d1, d2, ls) in zip(d1, d2, ls):
    dist = fisher_f(d1, d2, mu)

    plt.plot(x, dist.pdf(x), ls=ls, c='black',
             label=r'$d_1=%i,\ d_2=%i$' % (d1, d2))

plt.xlim(0, 4)
plt.ylim(0.0, 1.0)

plt.xlabel('x')
plt.ylabel('p(x|d_1, d_2)')
plt.title("Fisher's Distribution")

plt.legend()
plt.show()

# Tells me if two population variances are equal, but in multivariate models - it tells me how strong my model is.
# If I made it better. The larger the F value, the higher the chance for outliers (between group/in-group) and
# statistical significance.


# In[159]:


from scipy.stats import t as student_t
mu = 0
# I use 1E10 to describe infinity.

k = [1E10, 2, 1, 0.5]
ls = ['-', '--', ':', '-.']
x = np.linspace(-10, 10, 1000)


for k, ls in zip(k, ls):
    dist = student_t(k, 0)

    if k >= 1E10:
        label = r'$\mathrm{t}(k=\infty)$'
    else:
        label = r'$\mathrm{t}(k=%.1f)$' % k

    plt.plot(x, dist.pdf(x), ls=ls, c='black', label=label)

plt.xlim(-5, 5)
plt.ylim(0.0, 0.45)

plt.xlabel('$x$')
plt.ylabel(r'$p(x|k)$')
plt.title("Student's $t$ Distribution")

plt.legend()
plt.show()
