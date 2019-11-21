# Functions are a collection of code that takes zero to x arguments. We have to call this function
def function1():
    print("a")
    print("b")


print("This is outside the function")
function1()
# It can also be a mapping. "WE are going to define a function which is
# going to take the input and return


def function2(x):
    return 2 * x


a = function2(3)
a


def function3(x, y):
    return x + y


e = function3(1, 2)
e


# BMI Calc
name1 = "Luis"
weight1 = 90
height1 = 2

name2 = "Squi"
weight2 = 90
height2 = 2

name3 = "moose"
weight3 = 90
height3 = 2


def bmi_calculator(name, height, weight):
    bmi = weight / (height**2)
    print("bmi: ")
    print(bmi)
    if bmi < 25:
        return name + " is not overweight"
    else:
        return name + " overweight"


# In[9]:


result1 = bmi_calculator(name1, height1, weight1)
print(result1)
