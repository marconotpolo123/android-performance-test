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
        self.list_network_traffic = [('Current Time', 'Network Traffic(Bytes)')]

    def get_network_traffic(self):
        # find the process id
        cmd_fetch_pid = 'adb shell ps | findstr ' + self.package
        content = os.popen(cmd_fetch_pid)
        time.sleep(3)
        network_traffic = 0
        for line in content.readlines():
            line = " ".join(line.split())
            # network traffic is calculated by the sum of received + transmitted bytes
            cmd_fetch_network_traffic = 'adb shell cat /proc/' + line.split(' ')[1] + '/net/dev'
            content = os.popen(cmd_fetch_network_traffic)
            for line in content.readlines():
                line = line.rstrip("\n")
                line = " ".join(line.split())
                if "Inter-" not in line and "face" not in line:
                    row = line.split(' ')
                    bytes_of_received_packets = row[1]
                    bytes_of_transmitted_packets = row[9]
                    network_traffic = network_traffic + int(bytes_of_received_packets) + int(bytes_of_transmitted_packets)


        #print(sum)
        return network_traffic

    @staticmethod
    def get_current_time():
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    def count_of_execution(self, times):
        while times > 0:
            currTime = self.get_current_time()
            network_traffic = self.get_network_traffic()
            self.list_network_traffic.append((currTime, network_traffic))
            time.sleep(5)
            times -= 1
        
        #print(self.list_network_traffic)
        return self.list_network_traffic

    def save_to_csv(self, tupled_list):
        with open("network_traffic.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tupled_list)
            f.close()

    @staticmethod
    def plotGraph():
        data = pd.read_csv('network_traffic.csv')
        current_time = data['Current Time']
        network_traffic = data['Network Traffic(Bytes)']
        plt.xlabel("Current Time")
        plt.ylabel("Network Traffic(Bytes)")
        plt.plot_date(current_time, network_traffic, linestyle='solid')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()


test = Test(sys.argv[1], sys.argv[2])
list_network_traffic = test.count_of_execution(sys.argv[3])
test.save_to_csv(list_network_traffic)
test.plotGraph()

## 'com.touchboarder.android.api.demos', 'com.touchboarder.androidapidemos.MainActivity'
## 20