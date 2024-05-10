import subprocess
import time
import pywinauto
import pandas as pd
import pyautogui

import numpy as np

devices = ['Device 2']

applications = [
    {'name': "C:\\Users\\Moham\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", 'version': '15.0'},

    {'name': "C:\\Program Files\\Windows NT\\Accessories\\wordpad.exe", 'version': ''},

    {'name': "C:\\Windows\\system32\\SnippingTool.exe", 'version': ''},

    {'name': "C:\\Windows\\system32\\notepad.exe", 'version': ''},

    {'name': "C:\\Windows\\system32\\mspaint.exe", 'version': ''}

    ]

num_runs = 10
arr_img = ["vscode.png", "wordpad.png", "snippingtool.png", "notepad.png", "paint.png"]


def measure_app_load_time(device_name, app_name, app_version, index):
    start_time = time.time()
    app = pywinauto.Application(backend='uia').start(f'{app_name}')

    while True:
        start_time2 = time.time()
        x = pyautogui.locateOnScreen(arr_img[index], confidence=0.76)
        end_time2 = time.time()
        if x:
            app.kill()
            break

        else:
            time.sleep(1)

    extra_time = end_time2 - start_time2
    end_time = time.time()
    return end_time - start_time - extra_time


results = []
index = 0
for i, device_name in enumerate(devices):
    for j, app in enumerate(applications):
        load_times = []
        for k in range(num_runs):
            load_time = measure_app_load_time(device_name, app['name'], app['version'], index)
            load_times.append(load_time)
            print(f"{device_name} - {app['name']} - Run {k + 1} - Load Time: {load_time:.2f} seconds")
        index = index + 1
        print("----------------------------------------------------------------------------------------------------")
        avg_load_time = sum(load_times) / len(load_times)
        results.append({'Device Number': i + 1,
                        'Application Number': j + 1,
                        'Average Load Time': avg_load_time})

df_results = pd.DataFrame(results)
df_summary = df_results.groupby('Application Number')['Average Load Time'].mean().reset_index()
df_summary['    Percentile'] = df_summary['Average Load Time'].rank(pct=True)
print(df_summary)
