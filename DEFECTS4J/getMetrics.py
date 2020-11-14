import subprocess
import os
from os import listdir
from os.path import isfile, join, isdir
import sys
import xml.etree.ElementTree
import json
import re
import pandas as pd

def cmd(command):
    output = ""
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    finally:
        return output

def cmdWithMetrics(command, outfile):
    with open(outfile, 'w') as fd:
        subprocess.call('/usr/bin/time -f  time=%e,cpu=%P,mem=%M '+command, shell=True, stderr=fd, stdout=fd)
    rawMetrics = cmd("tail -n 1 %s"%outfile).decode().strip()
    rawMetrics += ',' # Add a comma for the regex
    findall = re.findall(r'(?P<var>.*?)=(?P<out>.*?),', rawMetrics) # Note the additional comma
    metrics = {k.strip(): v.strip() for k,v in findall}
    return metrics
    
REPEATS = 10

class ExtractorManager:

    def __init__(self, project):
        
        self.project = project
        self.folder_name = "/home/ubuntu/defects4j/results/"+self.project['name']
        self.init_folder = os.getcwd()
        
        if os.path.exists(self.folder_name):
            print("Results for project %s already exist" %self.project['name'])
            exit(0)
        os.mkdir(self.folder_name)
        
        self.bbox = ""
        self.times= ""
        self.times_avg= ""
        self.cpu=""
        self.mem=""
        self.n = 1
        self.fault_matrix = dict()
        self.tcs = []
    
    def generateProject(self):
        folder = self.project['base_folder']
        print("\033[95mProject: %s \033[0m" % self.project['name'])
        print("> Getting version %s" % folder)
        if os.path.exists( folder ):
            print("> Project available: %s" % folder)
            os.chdir(folder)
        else:
            cmd(self.project['base'])
            os.chdir(folder)   
            cmd(self.project['build'])   

    def runOneTestAndGetMetrics(self, clazz, testCase):

        df = pd.DataFrame(columns=["app","name","time","avgCpu","maxMem"])

        fullName = clazz + "#" + testCase
        clazz_name = clazz.split(".")[-1]
        
        # CREATE RESULT FOLDER

        outputFolder = join(self.folder_name, clazz_name, testCase)

        if not os.path.isdir(join(self.folder_name, clazz_name)):
            os.mkdir(join(self.folder_name, clazz_name))
        os.mkdir(outputFolder)
        
        # CLEAN AND RUN TEST (X TIMES)

        for i in range(REPEATS):
        
            cmd(self.project['clean'])    
            metrics = cmdWithMetrics(self.project['one_test'], join(outputFolder,"iteration_%d.log"%i))
            
            # COLLECT RESULTS

            df = df.append({
                "app": self.project['name'],
                "name": testCase,
                "time": metrics['time'],
                "avgCpu": metrics['cpu'][0:-1],
                "maxMem": float(metrics['mem']) / 1024
            }, ignore_index=True)

        # GENERATE OUTPUT FILE

        df.to_csv(join(outputFolder,'results.csv'), index=False)

        print("      \033[90m> %s \033[0m" % fullName)
    
    def fix(self, tc_class):
        if(self.project['name'] == "Math"):
            return tc_class.replace("math.","math3.")
        else:
            return tc_class

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Use: python3 extractTimesDefect4J.py <config_file>")
        exit()
    config = json.load(open(sys.argv[1]))

    em = ExtractorManager(config)
    em.generateProject()
    # em.runTestForMapClasses()
    # em.runTestForGetMetrics()
    em.runOneTestAndGetMetrics(config["sample_class"],config["sample_test_case"])
