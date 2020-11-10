import pandas as pd
import glob


for path in glob.glob('results/**'):
    cpu  = pd.read_csv('%s/cpu.txt' % path, names=['maxCpu'])
    mem  = pd.read_csv('%s/mem.txt' % path, names=['maxMem'])
    time = pd.read_csv('%s/times_avg.txt' % path, names=['time'])
    df = pd.concat([cpu, mem, time], axis=1)
    print(df)





#print(a)

#pd.concat([df1['c'], df2['c']], axis=1, keys=['df1', 'df2'])
