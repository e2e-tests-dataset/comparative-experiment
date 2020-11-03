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
        self.tcs = dict()
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

                try:
                    # ADD BBOX
                    with open(join(self.project['test_path'], suit_name.replace('.', '/')+".java"), "r+") as code_file:
                        self.bbox += code_file.read().replace("\n", " ").replace("\r", " ") + '\n'
                     # ADD TIME
                    self.times += root.get('time')+'\n'
                    # SAVE TO GET FAULT MATRIX
                    self.tcs[suit_name] = {
                        'id': self.n,
                        'name': suit_name
                    }
                    self.n = self.n+1
                except IOError as err:
                    # Except when exist a class in another class, i.e. SpecializeModuleTest$SpecializeModuleSpecializationStateTest.java
                    print("> Can't include %s TC" % suit_name)
                    continue

    def getMetrics(self):
        print("> Running test for get metrics")
        for tc in sorted(self.tcs.values(), key=lambda k: k['id']):
            self.pm.call("pkill java")
            self.pm.call(self.project['one_test'] % tc['name'])

            text = ""

            if self.project['metrics_path'].endswith(".xml"):
                root = xml.etree.ElementTree.parse(self.project['metrics_path']).getroot()
                text = root.find('system-out').text
            else:
                with open(self.project['metrics_path'], "r") as f:
                    text = f.read()

            m = re.search("AVG Mem: (.+)\nAVG CPU: (.+)\nAVG time: (.+)", text)
            cpu = -1
            mem = -1
            time = -1
            if m is not None and m.group(1) and m.group(2) and m.group(3):
                mem = m.group(1)
                cpu = m.group(2)
                time = str( float(m.group(3)) / 1000 )
            self.cpu += cpu + '\n'
            self.mem += mem + '\n'
            self.times_avg += time + '\n'
            print("      \033[90m> %s \033[0m" % tc['name'])
    
    def fix(self, tc_class):
        if(self.project['name'] == "Math"):
            return tc_class.replace("math.","math3.")
        else:
            return tc_class

    def save(self):
        self.safeClose()
        with open( join(self.folder_name,"times_avg.txt"), "w" ) as tma:
            tma.write(self.times_avg)
        with open( join(self.folder_name,"cpu.txt"), "w" ) as cpu:
            cpu.write(self.cpu)
        with open( join(self.folder_name,"mem.txt"), "w" ) as mem:
            mem.write(self.mem)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Use: python extractTimesDefect4J.py <config_file>")
        exit()
    config = json.load(open(sys.argv[1]))

    em = ExtractorManager(config)
    em.runTestForMapClasses()
    em.getMetrics()
    em.save()
