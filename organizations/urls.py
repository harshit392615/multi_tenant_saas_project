from django.urls import path
from .views import Organization_Create_API , Organization_List_API , Organization_Update_API , Organization_Delete_API , Organization_Archive_API , Organization_Membership_API , Organization_Membership_Update_API ,Organization_Add_Subscription , Organization_Verify_Subscription

urlpatterns = [
    path('create/', Organization_Create_API.as_view() , name = 'create'),
    path('list/',Organization_List_API.as_view() , name='list'),
    path('update',Organization_Update_API.as_view() , name='update'),
    path('delete/<uuid:org_id>',Organization_Delete_API.as_view() , name='delete'),
    path('archive',Organization_Archive_API.as_view() , name='archive'),
    path('membership/', Organization_Membership_API.as_view() , name='memberhsip' ),
    path('membership/update/' , Organization_Membership_Update_API.as_view() , name='membership_update'),
    path('subscription/' , Organization_Add_Subscription.as_view() , name='subscription_add'),
    path('subscription/verify/' , Organization_Verify_Subscription.as_view() , name='subscription_verify'),

]
