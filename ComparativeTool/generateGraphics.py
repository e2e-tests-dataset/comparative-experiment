#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib
import tikzplotlib


dfs = []
for path in glob.glob('./results/**/**/results.csv'):
    dfs.append(pd.read_csv(path, index_col=0))
df = pd.concat(dfs, sort=False)


def getDataset(app):
    if app in ["Chart", "Lang", "Math", "Closure", "Time"]: return "D4J" 
    if app in ["Eslint", "Express", "Pencilblue", "Shields", "Bower"]: return "BJS"
    if app in ["WebApp-1", "WebApp-2", "WebApp-3"]: return "E2E"
    return "NO_APP"


def cleanName(name):
    if name == "CLIEngine executeOnText": return "testExecutedOnText"
    if name == "Resolver .getSource should return the resolver source": return "testGetSource"
    if name == "app .request should extend the request prototype": return "testAppRequest"
    if name == "Resolver .getTarget should return the resolver target": return "testGetTarget"
    if name == "Resolver .hasNew should resolve to true by default": return "testHasNew"
    if name == "IgnoredPaths initialization should load .eslintignore from cwd when explicitly passed": return "testIgnorePaths"
    if name == "rules when given an invalid rules directory should log an error and exit": return "testRules"
    if name == "app .response should extend the response prototype": return "testAppResponse"
    if name == "app .use": return "testAppUse"
    if name == "BaseMediaRenderer BaseMediaRenderer.getEmbedUrl should not modify media id": return "testGetEmbedUrl"
    if name == "BaseObjectService BaseObjectService.getIdWhere should throw when passed null as the parameter": return "testGetIdWhere"
    if name == "RequestHandler RequestHandler.getBodyParsers should return the default list of body parsers": return "testGetBodyParsers"
    if name == "The LRU cache should support being called without new": return "testLRUCache"
    if name == "The text measurer should produce the same length as before": return "testTextMesurer"
    if name == "nodeifySync Should return the result via the callback": return "testNodeifySync"
    return name


def generateBoxPlot(df, column_name):
    plot = df.boxplot(column=[column_name], by='chartName', figsize=(12,4))
    plt.xticks(rotation=25)
    plt.title("")
    plt.suptitle('')
    plot.set_xlabel("")
    tikzplotlib.save('outputImages/%s.tex'%column_name, axis_width="12cm", axis_height="5cm")

only_9 = pd.concat([
    # BUGSJS
    dfs[10], dfs[7], dfs[4],
    # DEFECTS4J
    dfs[15], dfs[2], dfs[20], 
    # E2EDATASET
    dfs[23],dfs[22], dfs[18]
], sort=False)
only_9 = only_9.reset_index()
only_9['chartName'] = only_9.apply (lambda row: getDataset(row['app']) + "-" + cleanName(row['name']), axis=1) 


for column in ['testTime', 'totalTime', 'maxMem', 'avgCpu']:
    generateBoxPlot(only_9, column)


# GENERATE SUMMARY TABLE

dfg = df.groupby(['app','name'])

# Get Median of times and Mean of avgCpu and maxMem
table = pd.concat([
    dfg.median()[['totalTime']],
    dfg.median()[['testTime']],
    dfg.mean()[['avgCpu', 'maxMem']]]
, axis=1, join='inner')
table = table.reset_index()
table['app']  = table.apply (lambda row: getDataset(row['app']) + "-" + row['app'], axis=1) 
table['name'] = table.apply (lambda row: cleanName(row['name']), axis=1) 
table = table.sort_values(by=['app'])
table.round(decimals=3).to_csv('./results/resume.csv', index=False)

