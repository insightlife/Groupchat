from django.urls import re_path
from django.urls import path
from .consumer import MySync, MyAsync

websocket_urlpatterns = [
    path('wa/sc/<str:grpname>',MySync.as_asgi()),
    path('wa/ac/<str:grpname>',MyAsync.as_asgi())
]