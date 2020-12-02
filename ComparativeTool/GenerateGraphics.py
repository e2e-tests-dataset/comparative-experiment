#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib
import tikzplotlib


# In[2]:


dfs = []
for path in glob.glob('./results/**/**/results.csv'):
    dfs.append(pd.read_csv(path, index_col=0))
df = pd.concat(dfs, sort=False)


# In[3]:


dfg = df.groupby(['app','name'])


# In[4]:


# Get Median of times and Mean of avgCpu and maxMem
pd.concat([
    dfg.median()[['totalTime']],
    dfg.median()[['testTime']],
    dfg.mean()[['avgCpu', 'maxMem']]]
, axis=1, join='inner')


# In[5]:


def getDataset(app):
    if app in ["Chart", "Lang", "Math", "Closure", "Time"]: return "D4J" 
    if app in ["Eslint", "Express", "Pencilblue	", "Shields", "Bower"]: return "BJS"
    if app in ["WebApp-1", "WebApp-2", "WebApp-3"]: return "E2E"
    return "NO_APP"


# In[6]:


def cleanName(name):
    if name == "CLIEngine executeOnText": return "executedOnText"
    if name == "Resolver .getSource should return the resolver source": return "getSource"
    if name == "app .request should extend the request prototype": return "appRequest"
    return name


# In[7]:


def generateBoxPlot(df, column_name):
    plot = df.boxplot(column=[column_name], by='chartName', figsize=(12,4))
    plt.xticks(rotation=15)
    plt.title("")
    plt.suptitle('')
    plot.set_xlabel("")
    tikzplotlib.save('%s.tex'%column_name, axis_width="12cm", axis_height="5cm")


# In[8]:


only_9 = pd.concat([
    # DEFECTS4J
    dfs[0], dfs[5], dfs[7],
    # BUGSJS
    dfs[1], dfs[2], dfs[3], 
    # E2EDATASET
    dfs[6],dfs[8], dfs[9]
], sort=False)
only_9 = only_9.reset_index()
only_9['chartName'] = only_9.apply (lambda row: getDataset(row['app']) + "-" + cleanName(row['name']), axis=1) 


# In[9]:


for column in ['testTime', 'totalTime', 'maxMem', 'avgCpu']:
    generateBoxPlot(only_9, column)

