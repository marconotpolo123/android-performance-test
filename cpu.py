import os
import sys
import time
import csv
import pandas as pd
from matplotlib import pyplot as plt

class Test:

    def __init__(self, package, activity):
        self.package = package
        self.activity = activity
        self.content = ''
        self.list_cpu_percent = [('CurrentTime', 'CPU(%)')]

    def get_cpu_info(self):
        cmd = 'adb shell dumpsys cpuinfo | findstr ' + self.package
        self.content = os.popen(cmd)
        time.sleep(5)
        cpu_percent = 0
        for line in self.content.readlines():
            if self.package in line:
                cpu_percent = line.split("%")[0].rstrip("\n").lstrip()
                #print(cpu_percent)
                break
        return cpu_percent

    @staticmethod
    def get_current_time():
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    def count_of_execution(self, times):
        while times > 0:
            currTime = self.get_current_time()
            cpu_percent = self.get_cpu_info()
            self.list_cpu_percent.append((currTime, cpu_percent))
            time.sleep(60)
            times -= 1
        
        print(self.list_cpu_percent)
        return self.list_cpu_percent

    def save_to_csv(self, tupled_list):
        with open("cpu.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tupled_list)
            f.close()

    @staticmethod
    def plotGraph():
        data = pd.read_csv('cpu.csv')
        current_time = data['CurrentTime']
        cpu_percent = data['CPU(%)']
        plt.xlabel("Current Time")
        plt.ylabel("CPU Usage(%)")
        plt.plot_date(current_time, cpu_percent, linestyle='solid')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()


test = Test(sys.argv[1], sys.argv[2])
list_launchTimes = test.count_of_execution(int(sys.argv[3]))
test.save_to_csv(list_launchTimes)
test.plotGraph()

## 'com.touchboarder.android.api.demos', 'com.touchboarder.androidapidemos.MainActivity'
## 10
