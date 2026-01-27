from django.urls import path
from .views import notification_sse_view , notification_seen_API

urlpatterns = [
    path("notification/" , notification_sse_view , name='notification'),
    path("notification/update/", notification_seen_API.as_view() )
]