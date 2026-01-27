from celery import shared_task
from .publisher import publish_notification
from .views import add_user_notification , add_Org_notification
@shared_task(bind = True , autoretry_for={Exception,} , retry_kwargs = {'max_retries' : 3} )
def send_notification(self,*,user_id,title , description):
    publish_notification(user_id , title , description )

@shared_task(bind = True , autoretry_for={Exception,} , retry_kwargs = {'max_retries' : 3} )
def send_user_notification(self , title , description , user_id):
    add_user_notification(title,description,user_id)

@shared_task(bind = True , autoretry_for={Exception,} , retry_kwargs = {'max_retries' : 3} )
def send_Org_notification(self , title , description , organization_id):
    add_Org_notification(title,description,organization_id)