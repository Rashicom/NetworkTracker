import psutil
import schedule
import time
import requests
import json
import os
import asyncio
import websockets


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
        
        memory_usage = process.info["memory_info"].rss/(1024*1024)
        
        # avoiding duplicate process
        if process.info["name"] not in rec and memory_usage > 0.0:
            rec.add(process)

            # appending process information to the system_info list
            system_info.append({
                "process_name" : process.info["name"],
                "memory_percent": process.info["memory_percent"],
                "memory_usage": process.info["memory_info"].rss/(1024*1024)
            })
    return system_info

async def send_data():
    """
    collect all the datas to send and make a post request to the server
    """
    username = os.getlogin()
    system_info = fetch_process()
    data = {"username":username, "system_info":system_info}

    # url to send the data
    url = 'ws://127.0.0.1:8000/ws/add/'
    async with websockets.connect(url) as websocket:
        while True:
            
            # collect data in a perticular time period
            system_info = fetch_process()
            data = {"username":username, "system_info":system_info}
            print(data)
            await websocket.send(json.dumps(data))
            print("waining 30 second")
            await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(send_data())
