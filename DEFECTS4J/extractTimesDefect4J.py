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
    
    def create_and_test(self, folder, change_version_command):
        print("> Getting version %s" % folder)
        if os.path.exists( folder ):
            print("> Project available: %s" % folder)
            os.chdir(folder)
        else:
            self.pm.call(change_version_command)
            os.chdir(folder)
            self.pm.call(self.project['build'])
            print("> Running test: %s" % folder)
            self.pm.call(self.project['test'])
    
    def safeClose(self):
        self.pm.close()
        os.chdir(self.init_folder)
       

    def runTestForMapClasses(self):

        print("\033[95mProject: %s \033[0m" % self.project['name'])

        self.create_and_test(self.project['base_folder'], self.project['base'])

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

    def getMetrics(self):
        print("> Running test for get metrics")
        for tc in sorted(self.tcs, key=lambda k: k['id']):

            clazz = tc['class']
            clazz_name = tc['class'].split(".")[-1]
            tc = tc['testcase']
            fullName = clazz + "#" + tc

            self.pm.call("mvn clean")       
            self.pm.call(self.project['one_test'] % fullName)

            ouputFolder = join(self.folder_name, clazz_name, tc)

            # COPY OUTPUT

            if not os.path.isdir(join(self.folder_name, clazz_name)):
                os.mkdir(join(self.folder_name, clazz_name))
            os.mkdir(ouputFolder)
            src = self.project['metrics_path']
            dst = join(ouputFolder, "results.csv")
            copyfile(src, dst)

            # text = ""

            # if self.project['metrics_path'].endswith(".xml"):
            #     root = xml.etree.ElementTree.parse(self.project['metrics_path']).getroot()
            #     text = root.find('system-out').text
            # else:
            #     with open(self.project['metrics_path'], "r") as f:
            #         text = f.read()

            # m = re.search("AVG Mem: (.+)\nAVG CPU: (.+)\nAVG time: (.+)", text)
            # cpu = -1
            # mem = -1
            # time = -1
            # if m is not None and m.group(1) and m.group(2) and m.group(3):
            #     mem = m.group(1)
            #     cpu = m.group(2)
            #     time = str( float(m.group(3)) / 1000 )
            # self.cpu += cpu + '\n'
            # self.mem += mem + '\n'
            # self.times_avg += time + '\n'
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
    em.runTestForMapClasses()
    em.getMetrics()
