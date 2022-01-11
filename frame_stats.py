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
        self.frame_time_list = [('Frame Time(ms)',)]

    # how much time it takes to complete a single frame
    def capture_frame_time(self):
        cmd_framestats = 'adb shell dumpsys gfxinfo ' + self.package + ' framestats'
        self.content = os.popen(cmd_framestats)
        time.sleep(5)
        counter = 0
        for line in self.content.readlines():
            if '---PROFILEDATA---' in line or 'Flags,IntendedVsync,Vsync,OldestInputEvent' in line:
                counter += 1
                continue
            if counter == 2:
                #print(line)
                frame_time = str((int(line.split(",")[13]) - int(line.split(",")[1])) / 1000000)
                self.frame_time_list.append((frame_time,))
            if counter > 2:
                counter = 0
                continue


    def reset_frame(self):
        cmd_framereset = 'adb shell dumpsys gfxinfo ' + self.package + ' reset'
        os.popen(cmd_framereset)

    def count_of_execution(self, times):
        while times > 0:
            self.reset_frame()
            time.sleep(2)
            self.capture_frame_time()
            times -= 1
        
        #print(self.frame_time_list)
        return self.frame_time_list
        
    @staticmethod    
    def save_to_csv(tupled_list):
        with open("frame_stats.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tupled_list)
            f.close()

    @staticmethod
    def plotGraph():
        data = pd.read_csv('frame_stats.csv')
        frame_time = data['Frame Time(ms)'].tolist()
        #print(frame_time)
        bins = [5, 10, 15, 20, 25, 30]
        plt.hist(frame_time, bins=bins, edgecolor='black')
        plt.xlabel("Frame Time(ms)")
        plt.ylabel("Frame Count")
        plt.tight_layout()
        plt.show()


test = Test(sys.argv[1], sys.argv[2])
frame_time_list = test.count_of_execution(int(sys.argv[3]))
test.save_to_csv(frame_time_list)
test.plotGraph()


## 'com.touchboarder.android.api.demos', 'com.touchboarder.androidapidemos.MainActivity'
## 10