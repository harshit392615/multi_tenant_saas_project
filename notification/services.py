from .models import UserNotification 
from .publisher import publish_notification
from accounts.models import User
from organizations.models import Organization
from firebase_admin import messaging
from accounts.models import Device

def send_push_notification(user, title, body, data_payload=None):
    # 1. Get all devices for this user
    devices = Device.objects.filter(user=user)
    if not devices.exists():
        return # User hasn't registered any devices

    # 2. Extract the tokens into a list
    tokens = [device.registration_id for device in devices]

    # 3. Construct the message
    # 'data_payload' is useful for sending hidden IDs to the frontend (like note_id or workspace_slug)
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=data_payload or {}, 
        tokens=tokens,
    )

    # 4. Send the message
    try:
        response = messaging.send_each_for_multicast(message)
        print(f"Successfully sent {response.success_count} messages.")
        
        # Optional: Clean up dead tokens (e.g., if a user uninstalled the app or cleared cache)
        if response.failure_count > 0:
            responses = response.responses
            failed_tokens = []
            for idx, resp in enumerate(responses):
                if not resp.success:
                    # Common error codes for invalid tokens:
                    if resp.exception.code in ['messaging/invalid-registration-token', 'messaging/registration-token-not-registered']:
                        failed_tokens.append(tokens[idx])
            
            if failed_tokens:
                Device.objects.filter(registration_id__in=failed_tokens).delete()
                print(f"Cleaned up {len(failed_tokens)} invalid tokens.")

    except Exception as e:
        print(f"Error sending FCM message: {e}")

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
        send_push_notification(user=user, title=title, body=description)
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
    send_push_notification(user=user, title=title, body=description)

def update_notification_status(user):
    UserNotification.objects.filter(user = user, seen = False).update(seen = True)
    return {"message": "Updated successfully"}

