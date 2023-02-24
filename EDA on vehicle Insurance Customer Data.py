#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas
table1 = pandas.read_csv('customer_details.csv')
table2 = pandas.read_csv('customer_policy_details.csv')
print(table1.head())
print(table2.head())


# In[2]:


table1_label = {'0':'customer_id', '1':'gender', '2':'age', '3':'driving_licence_presence',
               '4':'region_code', '5':'previously_insured', '6':'vehicle_age', '7':'vehicle_damage'}

for i in range(table1.shape[1]):
    print(f'number of cells of {table1_label[str(i)]} with null values = {table1[str(i)].isnull().sum()}')
table1.info()
# In[10]:


table1.dropna(subset=['0'],inplace=True)
print(f'number of cells of {table1_label[str(0)]} with null values = {table1[str(0)].isnull().sum()}')


# In[11]:


for i in range(2,6):
    table1[str(i)].fillna(table1[str(i)].mean(),inplace=True)
    print(f'number of cells of {table1_label[str(i)]} with null values = {table1[str(i)].isnull().sum()}')


# In[16]:


for i in range(1,6,7):
    table1[str(i)].fillna(table1[str(i)].mode()[0],inplace=True)
    print(f'number of cells of {table1_label[str(i)]} with null values = {table1[str(i)].isnull().sum()}')


# In[17]:


table2_label = {'0':'customer_id', '1':'annual_premium_INR', '2':'Sales_channel_code', '3':'vintage', '4':'response'}


# In[18]:


for i in range(table2.shape[1]):
    print(f'number of cells of {table2_label[str(i)]} with null values is {table2[str(i)].isnull().sum()}')
table2.info()


# In[19]:


table2.dropna(subset=['0'],inplace = True)
print(f'number of cells of {table1_label[str(0)]} with null values is {table2[str(0)].isnull().sum()}')


# In[20]:


for i in range(1,5):
    table2[str(i)].fillna(table2[str(i)].mean(), inplace=True)
    print(f'number of cells of {table2_label[str(i)]} with null values is {table2[str(i)].isnull().sum()}')


# In[21]:


table1_limits={}
for i in range(2,6):
    computations = table1[str(i)].describe(percentiles=[.25,.75])
    mean = computations.values[1]
    Q1=computations.values[4]
    Q3=computations.values[6]
    IQR=Q3-Q1
    II=Q1-1.5*IQR
    hI=Q3+1.5*IQR
    table1_limits[str(i)]=(II,hI)
table1_limits


# In[23]:


table1_outliers={'2':0,'3':0,'4':0,'5':0,'6':0}

for j in table1.index:
    for i in range(2,6):
        if(table1_limits[str(i)][0]!=table1_limits[str(i)][1]) and (table1.loc[j,str(i)]>table1_limits[str(i)][1] or table1.loc[j,str(i)]<table1_limits[str(i)][0]):
            table1_outliers[str(i)]+=1
table1_outliers


# In[24]:


for j in table1.index:
    for i in range(2,6):
        if table1.loc[j, str(i)]<table1_limits[str(i)][0]:
            table1.loc[j, str(i)]=table1[str(i)].mean()
        if table1.loc[j, str(i)]>table1_limits[str(i)][1]:
            table1.loc[j, str(i)]=table1[str(i)].mean()
                                                    


# In[26]:


table2_limits={}
for i in range(1,5):
    computations = table2[str(i)].describe(percentiles=[.25,.75])
    mean = computations.values[1]
    Q1 = computations.values[4]
    Q3 = computations.values[6]
    IQR = Q3-Q1
    II = Q1-1.5*IQR
    hI = Q3+1.5*IQR
    table2_limits[str(i)] = (II,hI)
table2_limits


# In[28]:


table2_outliers = {'1':0, '2':0, '3':0, '4':0, '5':0}

for j in table2.index:
    for i in range(1,5):
        if(table2_limits[str(i)][0]!=table2_limits[str(i)][1]) and (table2.loc[j, str(i)]>table2_limits[str(i)][1] or table2.loc[j, str(i)]<table2_limits[str(i)][0]):
            table2_outliers[str(i)]+=1
table2_outliers          


# In[29]:


for j in table2.index:
    for i in range(1,5):
        if table2.loc[j, str(i)]<table2_limits[str(i)][0]:
            table2.loc[j, str(i)]=table2[str(i)].mean()
        if table2.loc[j, str(i)]>table2_limits[str(i)][1]:
            table2.loc[j,str(i)]=table2[str(i)].mean()


# In[31]:


table1.apply(lambda x:x.str.strip() if x.dtype=='object' else x)


# In[32]:


table2.apply(lambda x:x.str.strip() if x.dtype=='object' else x)


# In[33]:


table1.apply(lambda x:x.str.lower() if x.dtype=='object' else x)


# In[34]:


table2.apply(lambda x:x.str.lower() if x.dtype=='object' else x)


# In[35]:


table1.drop_duplicates(inplace=True)


# In[36]:


table2.drop_duplicates(inplace=True)


# In[37]:


data = pandas.merge(table1, table2, on='0')
label = {'0':'customer_id', '1_x':'gender', '2_x':'age', '3_x':'driving_license_presence', '4_x':'region_code', '5':'previously_insured', '6':'vehicle_age', '7':'vahicle_damage', '1_y':'annual_premium_INR', '2_y':'sales_channel_code', '3_y':'vintage', '4_y':'responce'}
data.rename(columns=label,inplace=True)
data


# In[38]:


result4_1 = data.groupby('gender')['annual_premium_INR'].mean()
import matplotlib.pyplot as pyplot
result4_1.plot()
pyplot.show()


# In[39]:


result4_2 = data.groupby('age')['annual_premium_INR'].mean()
import matplotlib.pyplot as pyplot
result4_2.plot()
pyplot.show()


# In[41]:


print(f"male to female ration is {round(data['gender'].value_counts()[0]/data['gender'].value_counts()[1],2)}")
print(f'generally, the standard is: \n balanced data ratio: {50/50}\n slightly balanced data ratio:{round(55/45,2)}-{60/40} \n imbalanced data ratio:{80/20}-{90/10}')


# In[43]:


result4_4 = data.groupby('vehicle_age')['annual_premium_INR'].mean()
import matplotlib.pyplot as pyplot
result4_4.plot()
pyplot.show()


# In[44]:


n = data['age'].corr(data['annual_premium_INR'])
if n<-0.5:
    print('trong negative relationship')
if n>0.5:
    print('strong positive relationship')
if n>-0.5 and n<0.5:
    print('There is no relationship!')


# In[ ]:




