import psutil
import schedule
import time
import requests
import json
import subprocess

def collect_system_info():
    installed_packages = subprocess.check_output(["dpkg","--get-selections"]).decode("utf-8").split("\n")
    installed_software = [line.split("\t")[0] for line in installed_packages]
    system_info = {
        "cpu usage": psutil.cpu_percent(interval=1),
        "memmory_usage": psutil.virtual_memory().percent,
        "installed_software": installed_software

    }
    return system_info

while True:
    print(collect_system_info())
    time.sleep(1)

