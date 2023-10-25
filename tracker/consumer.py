import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import NetworkSystems, SystemProcesses, ProcessHistory
from asgiref.sync import sync_to_async

class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("connecting")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("incoming")
        data = json.loads(text_data)
        
        await self.update_database(data)
        

    @sync_to_async
    def update_database(self,data):
        # update database

        # this is the users system login name
        # we are considering this as the identity
        system_user = data["username"]
        system_info = data["system_info"]

        # fetching system user and update it to data base,
        # if there is no user we create else we fetch the existed user instance
        # this helps to autoconnect the systems who run the pyton script to fetch the system data
        user,status = NetworkSystems.objects.get_or_create(system_username=system_user,password="123")
        print("user creation status :",status)

        # update system_process table using system_info data
        for process in system_info:

            # only create new process if there is no one
            # it means its a newly installed packages
            system_process,status = SystemProcesses.objects.get_or_create(
                network_system=user, 
                process_name=process["process_name"]
            )

            print("process_creation status", status)
            
            # update the package info history
            process_history= ProcessHistory.objects.create(
                system_package=system_process,
                memory_percent = process["memory_percent"],
                memory_usage = process["memory_usage"]
            )