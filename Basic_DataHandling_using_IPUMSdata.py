# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 22:05:32 2019

@author: Jrxz12
"""
# Preliminaries
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Packages for Stats
import statsmodels.api as sm
import scipy.stats as stats
import seaborn as sns

# Importing Data
input_base_path = r"C:\Users\Jrxz12\Desktop"

file1= r"Stata\Datasets\PersonA1-afteralldescriptivestats19756.dta"
file2=  r"Stata\Datasets\PersonB1-afterallvariableadditions14782.dta"
Aimee_df1= pd.read_stata(os.path.join(input_base_path, file1))
Aimee_df2= pd.read_stata(os.path.join(input_base_path, file2))

# Merge Data
lefton_condition= Aimee_df1.columns.tolist()
final_df= Aimee_df1.merge(Aimee_df2, 
                             how = "outer",
                             left_on = lefton_condition,
                             right_on = lefton_condition,
                             )

# Data Management
# Creating variables. Mostly Boolean
final_df= final_df.drop(["EngA","SENW", "SEW", "SEVW", "SNE"], axis=1)
final_df["EngA"]= np.nan
final_df["SEVW"]= np.nan
final_df["SEW"]= np.nan
final_df["SENW"]= np.nan
final_df["SNE"]= np.nan
# Another way to add them would be: 


condition= [
        (final_df["eng"]==4), 
        (final_df["eng"]==3), 
        (final_df["eng"]==2), 
        (final_df["eng"]==1)
        ]

choices= ['0','1','2','3']
final_df["EngA"]= (np.select(condition, choices, default=np.nan)).astype(float)

condition2= [
        (final_df["EngA"]==3),
        (final_df["EngA"]==2) | (final_df["EngA"]==1) | (final_df["EngA"]==0)
        ]
choices2= [1, 0]
final_df["SEVW"]= np.select(condition2, choices2, default=np.nan)

condition3= [
        (final_df["EngA"]==2),
        (final_df["EngA"]==3) | (final_df["EngA"]==1) | (final_df["EngA"]==0)
        ]
choices3= [1, 0]
final_df["SEW"]= np.select(condition3, choices3, default=np.nan)

condition4= [
        (final_df["EngA"]==1),
        (final_df["EngA"]==3) | (final_df["EngA"]==2) | (final_df["EngA"]==0)
        ]
choices4= [1, 0]
final_df["SENW"]= np.select(condition4, choices4, default=np.nan)

condition5= [
        (final_df["EngA"]==0),
        (final_df["EngA"]==3) | (final_df["EngA"]==2) | (final_df["EngA"]==1)
        ]
choices5= [1, 0]
final_df["SNE"]= np.select(condition5, choices5, default=np.nan)


# Using groupby
# Typically used to group observations that have a similar characteristic
Example1= final_df.groupby('EngA')
Example2= final_df.groupby(['EngA','EducationalAttainment'])

# Extracting a small piece from final_df
df_example= final_df[['EngA','EducationalAttainment']] 

# Generating mean for all columns by EngA. In this case, all columns= 1 column
Example3= df_example.groupby('EngA').mean()

# This just snags all rows corresponding to EngA==1 
# and the following for EngA==2
Example4= df_example.groupby('EngA').get_group(1)
Example5= df_example.groupby('EngA').get_group(2)


# Concatenate. This links two dataframes as would an outer merge
df_example2= pd.concat([Example4, Example5])

# Let's try append. The result here is the same. 
df_example3= Example4.append(Example5)

# You can also use extend instead of append. Extend is used in the cases where 
# there are multiple elements to add. 

# To sort, as you would expect, we use the .sort_values function
# To sort a list, we can use just .sort
df_example4= df_example3.sort_values(['EngA', 'EducationalAttainment'])


# Stats, using Chapter 5 of Wes Mckinney's book on Pandas
# A method like skipna, mostly found in stat functions
df_example4['EngA'].mean(skipna=False) # the default is the mean over the col.
                                        # dropna, fillna are useful 


# Correlation for Series and df, covariance
correlation= df_example4.EngA.corr(df_example4.EducationalAttainment)
df_example4.corr()
covariance= df_example4.EngA.cov(df_example4.EducationalAttainment)


# Other 
columns = [
        "lnEarnings",
        "EducationalAttainment"
        ]
for column in columns:
    sns.kdeplot(final_df[column], shade=True)

jp= sns.jointplot("EducationalAttainment", "lnEarnings", 
                  data=final_df, kind='reg').set_axis_labels(
                          "Educational Attainment", "Log Earnings")

fig= jp.fig
fig.subplots_adjust(top=0.93)
fig.suptitle(
        'Correlation and Distribution of Educational Attainment on Earnings', 
        fontsize=14, 
        fontweight='bold'
        )

#Weighted Regression
IV_columns= [
        "AYNE", 
        "DAoA", 
        "NES", 
        "agep", 
        "White", 
        "Black", 
        "Asian", 
        "Hisp", 
        "sex"
        ]
IV = final_df[IV_columns]
DV = final_df["lnWage"]
IV = sm.add_constant(IV)
weight = final_df["pwgtp2"]
sd= 'HC0'
regression1 = sm.WLS(DV, IV, weights=weight, missing='drop').fit(cov_type= sd)
IVhat = regression1.predict(IV)
regression1.summary()
final_df = final_df.dropna(subset=['lnEarnings'])


def _variable_finder_(variable_name):
    """Referencing the 2017 PUMS data dictionary, the function will
       search the datasets for the variable needed"""   
    if variable_name in Aimee_df1.columns.tolist():
        print("Yes, {} is here".format(variable_name))
    else:
        print("{} is on the loose.".format(variable_name))
        
    
