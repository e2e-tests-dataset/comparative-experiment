import json
import pandas as pd
import re
import statistics 
from os import listdir
from os.path import isfile, isdir, join

def cleanKey(key):
    return key.replace('.', '_').replace("-", "_")

def extractTestCaseData(data, app):

    # All executions have only 1 Test Suite with 1 Test Case
    ts = data['tJobExec']['testSuites'][0]

    row = {
        'app':  app,
        'name': ts['testCases'][0]['name'],
        'totalTime': data['tJobExec']['duration'],
        'testTime' : ts["timeElapsed"],
        'avgCpu': 0,
        'maxMem': 0,
        'testCases': [],
    }

    for tc in ts['testCases']:

        tc_dict = {
            "name": tc['name'],
            "time": tc['time'],
            "avgCpu": [],
            "maxMem": []
        }

        instants = {}

        metrics = []
        if 'metrics' in tc:
            metrics = tc['metrics']
        else:
            metrics = data['metrics']

        for item in metrics:

            # MEMORY USAGE

            if "_dockbeat-memory.maxUsage" in item['name']:
                match = re.search("(.*)-et_dockbeat-memory.maxUsage", item['name'])
                component_key = match.group(1)

                for metric in item['traces'][cleanKey(item['name'])]:

                    instant_key = metric["timestamp"][0:-5]
                    
                    if instant_key not in instants:
                        instants[instant_key] = {}

                    if component_key not in instants[instant_key]:
                        instants[instant_key][component_key] = { 'mem': [], 'cpu': [] }

                    memInMb = (metric['value'] / 1024) / 1024
                    instants[instant_key][component_key]['mem'].append(memInMb)

            # CPU USAGE

            if "_dockbeat-cpu.totalUsage" in item['name']:
                match = re.search("(.*)-et_dockbeat-cpu.totalUsage", item['name'])
                component = match.group(1)

                for metric in item['traces'][cleanKey(item['name'])]:

                    instant_key = metric["timestamp"][0:-5]
                    
                    if instant_key not in instants:
                        instants[instant_key] = {}

                    if component_key not in instants[instant_key]:
                        instants[instant_key][component_key] = { 'mem': [], 'cpu': [] }

                    cpuUsage= metric['value']
                    instants[instant_key][component_key]['cpu'].append(cpuUsage)

        memMetrics = []
        cpuMetrics = []

        for components in instants.values():
            sumCpu = 0
            sumMemory = 0
            # ONLY WHEN ALL COMPONENTS
            #if len(components.values()) < 4: continue
            for component in components.values():
                sumCpu += max(component['cpu']) if len(component['cpu']) > 0 else 0.0
                print(sumCpu)
                sumMemory += max(component['mem'], default=0)
            memMetrics.append(sumMemory)
            cpuMetrics.append(sumCpu)

        row['testCases'].append(tc_dict)
        tc_dict['maxMem'] = max(memMetrics, default=0)
        tc_dict['avgCpu'] = statistics.mean(cpuMetrics) if len(cpuMetrics) > 0 else 0.0

    row['maxMem'] = max(map(lambda x: x["maxMem"], row['testCases']))
    row['avgCpu'] = max(map(lambda x: x["avgCpu"], row['testCases']))
    del row['testCases']

    return row


if __name__ == "__main__":

    MAIN_PATH = "./results/"

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
                    attemps.append(extractTestCaseData(data, app))
                #break # TO DELETE

            if len(attemps) > 0:
                df = pd.DataFrame.from_dict(attemps)
                df.to_csv(join(test_results_path,'results.csv'), index=False)
                print(df)
            #break # TO DELETE
        #break # TO DELETE
