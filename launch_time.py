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
        self.launchTime = ''
        self.list_launchTime = [('CurrentTime', 'LaunchTime(ms)')]

    def launch_app(self):
        cmd = 'adb shell am start -W -n ' + self.package + '/' + self.activity
        self.content = os.popen(cmd)
        time.sleep(5)

    def kill_app(self):
        cmd = 'adb shell am force-stop ' + self.package
        os.popen(cmd)
        time.sleep(5)

    def stop_app(self):
        cmd = 'adb shell input keyevent 3'
        os.popen(cmd)
        time.sleep(5)

    def cold_launch_app(self):
        self.launch_app()
        launch_time = self.get_launch_time()
        self.kill_app()
        return launch_time

    def hot_launch_app(self):
        self.launch_app()
        launch_time = self.get_launch_time()
        self.stop_app()
        return launch_time

    def get_launch_time(self):
        for line in self.content.readlines():
            if "ThisTime: " in line:
                self.launchTime = line.split(": ")[1].rstrip("\n")
                break
        return self.launchTime

    @staticmethod
    def get_current_time():
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    def count_of_execution(self, execution_method, times):
        self.kill_app()
        while times > 0:
            currTime = self.get_current_time()
            
            if execution_method == 'hot start':
                launch_time = self.hot_launch_app()
            else:
                launch_time = self.cold_launch_app()

            self.list_launchTime.append((currTime, launch_time))
            times -= 1
        
        print(self.list_launchTime)
        return self.list_launchTime

    def save_to_csv(self, tupled_list):
        with open("launch_time.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tupled_list)
            f.close()

    @staticmethod
    def plotGraph():
        data = pd.read_csv('launch_time.csv')
        current_time = data['CurrentTime']
        launch_time = data['LaunchTime(ms)']
        plt.xlabel("Current Time")
        plt.ylabel("Launch Time(ms)")
        plt.plot_date(current_time, launch_time, linestyle='solid')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()


test = Test(sys.argv[1], sys.argv[2])
list_launchTimes = test.count_of_execution(sys.argv[4], sys.argv[3])
test.save_to_csv(list_launchTimes)
test.plotGraph()
#print(list_launchTimes[:])


## 'com.touchboarder.android.api.demos', 'com.touchboarder.androidapidemos.MainActivity'
## 20
## 'cold start' or 'hot start'