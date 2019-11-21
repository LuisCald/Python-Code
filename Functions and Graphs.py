#!/usr/bin/env python
# coding: utf-8

# # Linear Housing Expenditure Function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
x = np.linspace(0, 5000)
y = .27 * x + 164

plt.rcParams['figure.figsize'] = (11, 4)

plt.xticks([0, 5000], ['$0$', '$5000$'])
plt.xlabel("Income")
plt.ylabel("Housing")
plt.axhline(0, color='black')
plt.plot(x, y, '-b', label='housing= 164 + .27income')
plt.legend(loc='best')
plt.title('Figure A.1 Graph of Housing')
plt.show()


# # Demand for Compact Discs
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 5, 10, 15)
P = (120 / 9.8) - x
plt.rcParams['figure.figsize'] = (11, 4)

plt.xticks([0, .50, 2], ['$0$', '$.5$', '$2$'])
plt.xlabel("Quantity")
plt.ylabel("Price")
plt.axhline(0, color='black')
plt.plot(x, y, '-b', label=r'$Demand for CDs')
plt.legend(loc='best')
plt.title('Figure A.2 Graph')
plt.show()


# # Quadratic Function
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 10, 20)
y = 8 * x - 2 * x ** 2 + 6

plt.rcParams['figure.figsize'] = (11, 4)

plt.xticks([0, 10, 20], ['$0$', '$10$', '$20$'])
plt.axhline(14, color='black', linestyle='dashed')
plt.axvline(2, color='black', linestyle='dashed')
plt.plot(x, y, '-b', label=r'$y= 6+ 8x - 2x^2$')
plt.legend(loc='best')
plt.title('Figure A.3 Graph')
plt.show()


# In[14]:


math = np.math
x = np.linspace(-45, 45, 1000)

plt.rcParams['figure.figsize'] = (11, 4)

plt.xticks([-40, -20, 0, 20, 40], ['$-40$', '$-20$', '$0$', '$20$', '$40$'])
plt.yticks([-20000, 0, 20000])

plt.axvline(0, color='black')
plt.axhline(0, color='black')
plt.plot(x, np.log10(np.abs(x)), label=r'$f(x)= log_{10} x$')
plt.legend(loc='best')
plt.title('Logarithmic Function')
plt.show()


# In[15]:
import numpy as np
import pylab
import matplotlib.pyplot as plt
x = np.linspace(0, 1000, 2000)
y = .48 * x - .008 * x**2
plt.rcParams['figure.figsize'] = (11, 4)

plt.xticks([0, 1000, 2000], ['$0$', '$1000$', '$2000$'])
pylab.xlabel("Price")
pylab.ylabel("Quantity")

plt.plot(x, y + 5.25, '-b', label=r'$wage= 5.25 + .48exper - .008exper^2$')
plt.legend(loc='best')
plt.title('Ex. A.4 Graph')
plt.show()


# # Constant Elasticity Demand Function

# In[15]:


import math
x = np.linspace(0, 10, 20)
y = np.log10(x) * -1.25
plt.rcParams['figure.figsize'] = (11, 4)

plt.xticks([0, 5, 10], ['$0$', '$5$', '$10$'])
pylab.xlabel("Price Elasticity of Demand")
pylab.ylabel("Quantity Demanded")
plt.plot(x, y + 4.7, '-b', label=r'$log(q) = 4.7 - 1.25log(p)$')
plt.legend(loc='best')
plt.title('Ex A.5 Graph')
plt.show()
