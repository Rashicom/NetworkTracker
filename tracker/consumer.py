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

        user,status = NetworkSystems.objects.get_or_create(system_username=system_user,password="123")
        
