a = 1
b = 2
# If clause. MAke sure the indent is consistent through the lines
if a < b:
    print("Iguanas")
    print("Fly over the moon")


# In[1]:


# The single equal sign is an assignment. The double equal sign is like math.
c = 5
d = 4
if c < d:
    print("positive")
elif c == d:
    print("Hmmmm")
else:
    print("negative")


# In[4]:


g = 8
h = 8

if g < h:
    print("g is less than h")
else:
    if g == h:
        print("g is equal to h")
    else:
        print("g is greater than h")


# In[15]:


name = "james"
height = 2
weight = 190
bmi = weight / (height**2)
print("bmi: ")
print(bmi)

if bmi < 25:
    print(name)
    print("is not overweight")
else:
    print(name)
    print("is overweight")
