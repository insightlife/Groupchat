from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import group,chat

class MySync(SyncConsumer):
    def websocket_connect(self,event):
        self.gpn = self.scope['url_route']['kwargs']['grpname']
        print("websocket connected for group ",self.gpn,self.scope["user"])
        print("channel layer ",self.channel_layer)
        print("channel name ",self.channel_name)
        async_to_sync(self.channel_layer.group_add)(self.gpn,self.channel_name)
        self.send({'type':'websocket.accept'})

    def websocket_receive(self,event):
        print("client msg received")
        print("event is ",event)
        ddata=json.loads(event['text'])
        print("final data...",ddata)
        groupp = group.objects.get(name=self.gpn)
        print("chat is going to ave for group",groupp)
        chatt = chat(content=ddata['msg'],group=groupp,person=self.scope['user'])
        chatt.save()
        async_to_sync(self.channel_layer.group_send)(self.gpn,{'type':'chat.message','message':event['text']})

    def chat_message(self,event):
        print('event..chat_message_handler',event)
        print('event..chat_message_handler',event['message'])
        print(self.scope["user"])
        self.send({'type':'websocket.send','text':event['message'],'user':self.scope['user']})

    def websocket_disconnect(self,event):
        print("websocket disconnected")
        print("channel layer",self.channel_layer,self.channel_name)
        raise StopConsumer()

class MyAsync(AsyncConsumer):
    async def websocket_connect(self,event):
        self.gpn = self.scope['url_route']['kwargs']['grpname']
        print("websocket connected",self.gpn)
        print("channel layer",self.channel_layer,self.channel_name)
        async_to_sync(self.channel_layer.group_add)(self.gpn,self.channel_name)
        await self.send({'type':'websocket.accept'})

    async def websocket_receive(self,event):
        print("client msg received")
        print(event)
        async_to_sync(self.channel_layer.group_send)(self.gpn,{'type':'chat.message','message':event['text']})

    async def chat_message(self,event):
        print('event..chat_message_handler',event)
        print('event..chat_message_handler',event['message'])
        await self.send({'type':'websocket.send','text':event['message']})

    async def websocket_disconnect(self,event):
        print("websocket disconnected")
        print("channel layer",self.channel_layer,self.channel_name)
        raise StopConsumer()
