from django.urls import re_path , path
from .consumer import NotesUpdateConsumer

websocket_urlpatterns = [re_path(
    r"^ws/notes/$",
    NotesUpdateConsumer.as_asgi()
)]