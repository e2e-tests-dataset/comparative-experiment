import json
import pandas as pd
import re
from os import listdir
from os.path import isfile, isdir, join

def cleanKey(key):
    return key.replace('.', '_').replace("-", "_")

def extractTestCaseData(data):

    # All executions have only 1 Test Suite with 1 Test Case
    ts = data['tJobExec']['testSuites'][0]

    row = {
        'app': data['tJobExec']['tJob']['sut']['name'],
        'name': ts['testCases'][0]['name'],  # ts['name'],
        'time': data['tJobExec']['duration'],
        'testCases': [],
        'maxMem': 0,
        'maxCpu': 0
    }

    for tc in ts['testCases']:
        #print("    - "+tc['name'])

        tc_dict = {
            "name": tc['name'],
            "time": tc['time'],
            "maxMem": [],
            "maxCpu": []
        }

        memMetrics = []
        cpuMetrics = []

        if 'metrics' in tc:

            for item in tc['metrics']:

                # MEMORY USAGE

                if "_dockbeat-memory.maxUsage" in item['name']:
                    match = re.search("(.*)-et_dockbeat-memory.maxUsage", item['name'])
                    component = match.group(1)
                    #print("       Component: %s" % component)
                    for metric in item['traces'][cleanKey(item['name'])]:
                        memInMb = (metric['value'] / 1024) / 1024
                        #print("       -> Memory (MBytes): %d" % memInMb)
                        memMetrics.append((metric['value'] / 1024) / 1024)

                # CPU USAGE

                if "_dockbeat-cpu.totalUsage" in item['name']:
                    match = re.search("(.*)-et_dockbeat-cpu.totalUsage", item['name'])
                    component = match.group(1)
                    #print("       Component: %s" % component)
                    for metric in item['traces'][cleanKey(item['name'])]:
                        cpuUsage= metric['value']
                        #print("       -> CPU (%%): %f" % cpuUsage)
                        cpuMetrics.append(cpuUsage)

        tc_dict['maxMem'] = max(memMetrics, default=0)
        tc_dict['maxCpu'] = max(cpuMetrics, default=0)
        row['testCases'].append(tc_dict)

    row['maxMem'] = max(map(lambda x: x["maxMem"], row['testCases']))
    row['maxCpu'] = max(map(lambda x: x["maxCpu"], row['testCases']))
    del row['testCases']

    return row


if __name__ == "__main__":

    MAIN_PATH = "/home/ubuntu/E2EDataset"

    apps = [f for f in listdir(MAIN_PATH) if isdir(join(MAIN_PATH, f))]

    # ITERATE APPS

    for app in apps:
        app_path = join(MAIN_PATH, app)
        test_folders = [f for f in listdir(app_path) if isdir(join(app_path, f))]

        # ITERATE TEST RESULTS FOLDERS

        for test_folder in test_folders:
            test_results_path = join(app_path, test_folder)
            results = [f for f in listdir(test_results_path) if isfile(join(test_results_path, f)) and f.endswith(".json")]

            # ITERATE TEST RESULTS ATTEMPS

            attemps = []

            for result in results:
                
                with open(join(test_results_path, result)) as json_file:
                    data = json.load(json_file)
                    attemps.append(extractTestCaseData(data))

            if len(attemps) > 0:
                df = pd.DataFrame.from_dict(attemps)
                df.to_csv(join(test_results_path,'results.csv'), index=False)
                means = df.groupby(['app','name']).mean()
                means.to_csv(join(test_results_path, 'mean.csv'), index=False)
                print(df)
