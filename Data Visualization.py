import pandas as pd
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6, 7]
y = [1, 3, 5, 6, 14, 2, 2]
# If you want a second curve on the same graph, just put it right after
# the other
plt.plot(x, y)
plt.title("Luis food intake")
plt.xlabel("Day of Week")
plt.ylabel("Amount of Toast")
plt.xticks([1, 2, 3, 4, 5, 6, 7], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
# The legend function takes the arguments in order from how they were
# coded
plt.legend(["Amount of Toast"])
plt.show()


# In[16]:


data = pd.read_csv("")
data
type(data)

# to retrieve columns and dtype:int64 and it's a series
data.column_c

# To retrieve specific values. Here iloc[0] retrieves the first entry
data.column_c.iloc[0]

plt.plot(data.column_a, data.column_b, 'v')
plt.plot(data.column_a, data.column_c)
plt.show()

# You can use single quotes or double quotes to assess a string python
data2 = pd.read_csv('countries.csv')
data2

# if you just write data2.country == 'United States' it generates a true
# and false table
US = data2[data2.country == 'United States']
US
China = data2[data2.country == 'China']
China

plt.plot(US.year, US.population / 10**6)
plt.plot(China.year, China.population / 10**6)
plt.legend(['United States', 'China'])
plt.xlabel('year')
plt.ylabel('population')
plt.show()
US.population

Normalized = US.population / US.population.iloc[0]
NC = China.population / China.population.iloc[0]
Normalized


# In[45]:


plt.plot(US.year, Normalized)
plt.plot(China.year, NC)
plt.legend(['United States', 'China'])
plt.xlabel('year')
plt.ylabel('population growth compared to first year')
plt.show()
