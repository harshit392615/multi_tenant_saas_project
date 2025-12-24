from django.urls import path
from .views import OrgActivityList , EntityActivityList

urlpatterns = [
    path('activities/', OrgActivityList.as_view() , name = 'org_activities' ),
    path('entities/<uuid:entity_id>/activities/', EntityActivityList.as_view() , name = 'entity_activities'),
]