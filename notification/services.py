from .models import UserNotification 
from .publisher import publish_notification
from accounts.models import User
from organizations.models import Organization
from asgiref.sync import async_to_sync


def Create_Org_Notifications(title , description , organization_id):
    organization = Organization.objects.get(id = organization_id)
    users = User.objects.filter(membership__organization = organization)
    notifications = []
    for user in users:
        notifications.append(
        UserNotification(
            title = title,
            description = description , 
            user = user 
        ))
        publish_notification(user.id , title , description )
    UserNotification.objects.bulk_create(notifications)

    
def Create_user_Notifications(title , description , user_id):
    user = User.objects.get(
        id = user_id
    )
    notification = UserNotification.objects.create(
        title = title,
        description = description , 
        user = user
    )

def update_notification_status(user):
    UserNotification.objects.filter(user = user, seen = False).update(seen = True)
    return {"message": "Updated successfully"}
