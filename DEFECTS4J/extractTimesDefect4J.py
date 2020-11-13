import subprocess
import os
from os import listdir
from os.path import isfile, join, isdir
import sys
import xml.etree.ElementTree
import pprint
import re 
import pickle
import shutil
from operator import attrgetter
import json
from shutil import copyfile

class ProcessManager:

    def __init__(self, output):
        self.outfile = output

    def call(self, params, output=None):
        if output is None:
            output=self.outfile
        return subprocess.call(params, shell=True, stdout=output, stderr=self.outfile)

    def runAndGetOutput(self, command):
        text=""
        with open('run', 'w') as out:
            self.call(command, output=out)
        with open('run', 'r') as out:
            text = out.read()
        self.call("rm run")
        return text
    
    def close(self):
        self.outfile.close()

class ExtractorManager:

    def __init__(self, project):
        
        self.project = project
        self.folder_name = "/home/ubuntu/defects4j/results/"+self.project['name']
        self.init_folder = os.getcwd()
        
        if os.path.exists(self.folder_name):
            print("Results for project %s already exist" %
                  self.project['name'])
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
        self.pm = ProcessManager(open(join(self.folder_name, 'outputs.log'), 'w+'))
        self.project['n_bugs'] = int(self.pm.runAndGetOutput("defects4j info -p %s | grep 'Number of bugs:' | cut -d':' -f2" % project['name']))
    
    def generateProject(self):
        folder = self.project['base_folder']
        change_version_command = self.project['base']
        print("\033[95mProject: %s \033[0m" % self.project['name'])
        print("> Getting version %s" % folder)
        if os.path.exists( folder ):
            print("> Project available: %s" % folder)
            os.chdir(folder)
        else:
            self.pm.call(change_version_command)
            os.chdir(folder)
            self.pm.call(self.project['build'])
    
    def safeClose(self):
        self.pm.close()
        os.chdir(self.init_folder)
       

    def runTestForMapClasses(self):

        print("> Running test for map: %s" % self.project['base_folder'])
        self.pm.call(self.project['test'])
        reports = listdir(self.project['reports_path'])
        reports.sort()
        for report in reports:
            if report.endswith('.xml'):
                root = xml.etree.ElementTree.parse(
                    join(self.project['reports_path'], report)).getroot()
                suit_name = root.get('name')
                # FILTER
                excluded = False
                if 'exclude' in self.project:
                    for ex in self.project['exclude']:
                        m = re.search(ex, suit_name)
                        if m is not None and m.group(0):
                            excluded = True
                if excluded:
                    continue

                className = join(self.project['test_path'], suit_name.replace('.', '/')+".java")
                if os.path.isfile(className):

                    for tc in root.findall("testcase"):
                        self.tcs.append({
                            'id': self.n,
                            'class': tc.get("classname"),
                            'testcase': tc.get("name")
                        })
                        self.n = self.n+1

                else:
                    # Except when exist a class in another class, i.e. SpecializeModuleTest$SpecializeModuleSpecializationStateTest.java
                    print("> Can't include %s TC" % suit_name)
                    continue

    def runTestForGetMetrics(self):
        print("> Running all test for get metrics")
        for tc in sorted(self.tcs, key=lambda k: k['id']):
            self.runOneTestAndGetMetrics(tc['class'], tc['testcase'])

    def runOneTestAndGetMetrics(self, clazz, testCase):
        fullName = clazz + "#" + testCase
        clazz_name = clazz.split(".")[-1]
        self.pm.call("mvn clean")       
        self.pm.call(self.project['one_test'] % fullName)

        ouputFolder = join(self.folder_name, clazz_name, testCase)

        # COPY OUTPUT

        if not os.path.isdir(join(self.folder_name, clazz_name)):
            os.mkdir(join(self.folder_name, clazz_name))
        os.mkdir(ouputFolder)
        src = self.project['metrics_path']
        dst = join(ouputFolder, "results.csv")
        copyfile(src, dst)
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
