import psutil
import schedule
import time
import requests
import json
import subprocess
import os


def fetch_process():
    """
    fetching all processes and assosiated information of the system
    return info as list
    """

    # declaring set to avoice duplicate process, in the case of pid we have to avoid this step
    # delaring system_info list to store process info
    rec = set()
    system_info = []

    # this loop iterate throgh the process and fetch the fields mentioned in the attrs
    for process in psutil.process_iter(attrs=["name","status","memory_percent","memory_info"]):
        
        # avoiding duplicate process
        if process.info["name"] not in rec:
            rec.add(process)

            # appending process information to the system_info list
            system_info.append({
                "process_name" : process.info["name"],
                "memory_percent": process.info["memory_percent"],
                "memory_usage": process.info["memory_info"].rss/(1024*1024)
            })
    return system_info

def sed_data():
    """
    collect all the datas to send and make a post request to the server
    """
    username = os.getlogin()
    system_info = fetch_process()
    data = {"username":username, "system_info":system_info}

    # url to send the data
    url = 'http://127.0.0.1:8000/'
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            print("success")
        else:
            print("Failed")
            
    except Exception as e:
        print(e)
        print("somthing went wrong")

    

# scheduled to send the data in every 1 minut
schedule.every(1).minutes.do(fetch_process)

# check the pendings in scheduler in evry one second 
# while True:
#     schedule.run_pending()
#     time.sleep(1)

        
