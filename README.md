This is a tool to help with app performance testing on Android and generate reports by Matplotlib. It measures following aspects:
1. Launch Time:
2. CPU
3. Memory
4. Frame Stats
5. Network Traffic

Pre-requisites:
1. Install Python
2. Install libraries csv, Pandas, Matplotlib

Explanations:

Launch Time: either "hot start" or "cold start"
1. Command format: _>launch_time.py APP_PACKAGE APP_ACTIVITY EXECUTION_TIMES 
2. Example: _>launch_time.py com.touchboarder.android.api.demos, com.touchboarder.androidapidemos.MainActivity 10

CPU:
1. Command format: _>cpu.py APP_PACKAGE APP_ACTIVITY EXECUTION_TIMES 
2. Example: _>cpu.py com.touchboarder.android.api.demos, com.touchboarder.androidapidemos.MainActivity 10

Memory:
1. Command format: _>memory.py APP_PACKAGE APP_ACTIVITY EXECUTION_TIMES
2. Example: _>memory.py com.touchboarder.android.api.demos, com.touchboarder.androidapidemos.MainActivity 10

Frame Stats:
1. Command format: _>frame_stats.py APP_PACKAGE APP_ACTIVITY EXECUTION_TIMES
2. Example: _>frame_stats.py com.touchboarder.android.api.demos, com.touchboarder.androidapidemos.MainActivity 10

Network Traffic:
1. Command format: _>network_traffic.py APP_PACKAGE APP_ACTIVITY EXECUTION_TIMES
2. Example: _>network_traffic.py com.touchboarder.android.api.demos, com.touchboarder.androidapidemos.MainActivity 10
