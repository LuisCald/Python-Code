a = ["a", "b", "c"]

# To iterate. This says: "For each element in a, print" element can be any word actually
for element in a:
    print(element)


# In[18]:


b = [20, 5, 4]
total = 0
# So here for all elements "e" in the set B, we add. So, initial total is 0
# Once we add the first element to it, we have a new total, 20. Then we add
# the subsequent e to it
for e in b:
    total = total + e
total
# You can also do this neat trick. instead of rewriting total, you can do:
for e in b:
    total += e  # The plus equals sign will add itself
total
# It shows 58 since i ran the command twice

# creates a range from 1 -5, not including 5
range(1, 5)
# To make a list out of it
c = list(range(1, 5))
c

for i in c:
    print(i + 6)

# So here I want to add only the numbers divisible by 3. This requires the
# modular which is the remainder function.
print(4 % 3)  # this will print only the remainder of 4/3 or 1.
range(1, 8)
total3 = 0
for i in range(1, 8):
    if i % 3 == 0:
        total3 += i
total3  # 3+6 since they are the only numbers divisble by 9


# In[8]:


d = list(range(1, 100))
total4 = 0
for i in d:
    if i % 4 and i % 5 == 0:
        total4 += i
total4
# d does not include 100


# While Loops and the Break Statement
total = 0
for i in range(1, 5):
    total += i
total
total2 = 0
# in the for loop, we did not have to specify i or element
# in the while loop, we have to specify, so we do it before
j = 1
while j < 5:
    total2 += j
    j += 1
total2
# The process: ok j =1 so it is less than 5, so we total2 + j = 0+1
# Then we add 1 to J so J is now 2
# Then we do the process again. total2 = 1+2 = 3 and so forth for all j<5


# So for loops and while loop lead to the same result, but the idea with while loop is that we do not know which elements will be under the condition. Meaning, in for loops, I already give a range. In while loops, it goes through all elements that satisfy a condition, rather than looking at a range. Meaning, we assume there are elements that do not satisfy the condition. This is necessary for the while loop to stop. For example, if we removed the negative numbers from the list, we have to add another condition in the while loop. This is shown 1 row below

# In[27]:


x = [5, 4, 3, 3, 2, -1, -2, -5]
total3 = 0
i = 0
# In the while function, when we have a list, we use the [] to indicate every
# element.
while x[i] > 0:
    total3 += x[i]
    i += 1
total3


# In[11]:


y = [5, 4, 3, 3, 2]
total5 = 0
i = 0
while i < len(y) and y[i] > 0:
    total5 += y[i]
    i += 1
print(total5)
print(len(y))
print(y[0])


# In[44]:


v = [3, 4, 5, 6, 7, -1, -2, -3]
total5 = 0
for element in v:
    if element <= 0:
        break
    total5 += element
print(total5)
# It immediately stops when it reaches a negative number


# In[45]:


v = [3, 4, 5, 6, 7, -1, -2, -3]
total5 = 0
i = 0
while True:
    total5 += v[i]
    i += 1
    if v[i] <= 0:
        break
print(total5)

# More on Loops
# More neat tricks in the for loop process
# lets create a list
a = [1, 2, 3, 4, 5, 6]
# i can obviously just put for i in 'a', print 'a' , but this method has
# implications
for i in range(len(a)):
    print(a[i])
# Weird command
for i in range(len(a)):
    for j in range(i + 1):
        print(a[i])


# In[53]:


d = range(100)
tot = 0
for i in d:
    if i % 5 == 0:
        tot += i
    elif i % 3 == 0:
        tot += i

print(tot)

# or command
d = range(100)
tot = 0
for i in d:
    if i % 5 == 0 or i % 3 == 0:
        tot += i
print(tot)
# This is a mistake. Running this while loop will make it stop at 0,
# hence it only works if the numbers are in descending order
n = [3, -3, -4, -5, 0, -6]
T = 0
j = len(n) - 1
while n[j] < 0:
    T += n[j]
    j -= 1
print(T)
# To convert to any order, we can do ascending
import numpy as np
w = n.sort()
print(n)

# or descending
n.sort(reverse=True)
print(n)

# Then we can take the sum using a while loop, since it is already organized.

T = 0
# This is our starting point. We start at the end, since all
# the negative numbers are there
i = len(n) - 1
while n[i] < 0:
    T += n[i]  # Summing only the negative numbers
    i -= 1  # Since we started at the end, we go backwards
print(T)

# Summing all numbers
T = 0
for i in n:
    T += i
    i += 1
print(T)


# In[104]:


f = [2, 3, -5, 6]
TT = 0
# Think of i as 'the element'
for i in f:
    if i > 0:
        TT += i
print(TT)


# Dictionaries
# To create a dictionary, just:
d = {}

# now to input values
d["George"] = 20
d["Michel"] = 21
d["Ade"] = 22
d["Ludicrous"] = 'silly or unbelieveable'
# This will show all values in our dictionary and you can print indvidually
print(d)


# In[6]:


# To iterate over key valued pairs and messing around with if and else
for key, value in d.items():
    if key != 'Ludicrous':
        print("Name")
    else:
        print("Word")
    print(key)
    print("")
    if key != 'Ludicrous':
        print("Age")
    else:
        print("Definition")

    print(value)
    print("")


# Class and Objects

# In[147]:


# We create classes to apply functions to each object of our class.
# Here, we create a class called friends where each object is 1 friend
# and whenever we run the function on an object like r1.introduce_self,
# it will print "My name is" +self.name where self = r1

# I later added the __init__ to simplify
class Friends:
    def __init__(self, name, color, weight):  # Called a constructor
        self.name = name
        self.color = color
        self.weight = weight

    def introduce_self(self):
        print("My name is " + self.name)
        print("My favorite color is " + self.color)


# In[156]:


# r1 here is an object. It goes within the class. By the way, to block out
# code, do control + /

# r1 = Friends()
# r1.name = "Tom"
# r1.color = "Blue"
# r1.weight = 40

# r2 = Friends()
# r2.name = "Squi"
# r2.color = "purple"
# r2.weight = 90

# Now we are going to try to use the __init_. This simplifies the coding process
r1 = Friends("Tom", "Blue", 40)
r2 = Friends("Squi", "Purple", 90)


# In[158]:


r1.introduce_self()
r2.introduce_self()


# In[159]:


class Person:
    def __init__(self, n, p, i):
        self.name = n
        self.personality = p
        self.is_sitting = i

    def sit_down(self):
        self.is_sitting = True

    def stand_up(self):
        self.is_sitting = False


p1 = Person("Alice", "Aggresive", False)
p2 = Person("Becky", "Talkative", True)
p1.robot_owned = r2
p2.robot_owned = r1
p1.robot_owned.introduce_self()


# List Comprehensions
a = [1, 2, 4, 6, 7, 12]
c = []
for x in a:
    c.append(x * 2)  # adding each element doubled in a to c
print(c)


# In[166]:


d = [x * 2 for x in a]
print(d)


# In[167]:


# So you create an empty list. Then fill it with a function
w = []
for element in d:
    w.append(element / 2)
print(w)

# Creating a range
range(6, 0, -1)  # Starts at 6, does not include 0, and goes down by 1
f1 = []
for x in range(6, 0, -1):
    f1.append(x ** 2)
print(f1)

f2 = [x ** 3 for x in range(13, 2, -2)]
print(f2)


# # Set
# A python set rejects duplicate sets
a = set()
print(a)

a.add(1)
print(a)

a.add(2)
print(a)


# So for lists, we have append. BUT for sets we have ADD
b = []
for x in a:
    b.append(np.log(x))

print(b)

# The fact that python rejects duplicates in a set is fascinating
q = [1, 2, 3, 3, 4, 4, 1]
new_set = set()
for x in q:
    new_set.add(x)
print(new_set)

t = 0
for x in new_set:
    t += x
print(t)
