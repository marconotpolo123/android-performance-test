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
        self.list_mem_usage = [('Current Time', 'PSS(KB)')]

    def get_memo_info(self):
        cmd = 'adb shell dumpsys meminfo | findstr ' + self.package
        self.content = os.popen(cmd)
        time.sleep(5)
        mem_usage = '0'
        for line in self.content.readlines():
            mem_usage = line.split(": ")[0]
            if 'K' in mem_usage:
                mem_usage = mem_usage[:-1].lstrip().replace(',', '')
            elif 'M' in mem_usage:
                mem_usage = str(float(mem_usage[:-1].lstrip().replace(',', '')) * 1024)
            else:
                mem_usage = str(float(mem_usage[:-1].lstrip().replace(',', '')) * 1024 * 1024)    
            break
        return mem_usage

    @staticmethod
    def get_current_time():
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    def count_of_execution(self, times):
        while times > 0:
            currTime = self.get_current_time()
            mem_usage = self.get_memo_info()
            self.list_mem_usage.append((currTime, mem_usage))
            time.sleep(1)
            times -= 1
        
        print(self.list_mem_usage)
        return self.list_mem_usage

    def save_to_csv(self, tupled_list):
        with open("memory.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tupled_list)
            f.close()

    @staticmethod
    def plotGraph():
        data = pd.read_csv('memory.csv')
        current_time = data['Current Time']
        mem_pss = data['PSS(KB)']
        plt.xlabel("Current Time")
        plt.ylabel("PSS(KB)")
        plt.plot_date(current_time, mem_pss, linestyle='solid')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()


test = Test(sys.argv[1], sys.argv[2])
list_mem_usage = test.count_of_execution(int(sys.argv[3]))
test.save_to_csv(list_mem_usage)
test.plotGraph()

## 'com.touchboarder.android.api.demos', 'com.touchboarder.androidapidemos.MainActivity'
## 20
