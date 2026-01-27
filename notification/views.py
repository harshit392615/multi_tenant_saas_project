from django.http import StreamingHttpResponse , HttpResponseForbidden , JsonResponse
from .selectors import notification_stream , get_unseen_notifications
from core.auth import authenticate_bearer_by_token
from .services import Create_user_Notifications  , update_notification_status , Create_Org_Notifications
from .publisher import publish_notification
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework.views import APIView





def add_user_notification(title , description , user_id):
    Create_user_Notifications(title , description , user_id)
    publish_notification(user_id , title , description )

def add_Org_notification(title , description , organization_id):
    Create_Org_Notifications(title , description , organization_id)

def notification_sse_view(request):
    token = request.GET.get('token')
    try:
        user = authenticate_bearer_by_token(token)
    except Exception:
        return HttpResponseForbidden("Unauthorized")
    
    notifications = get_unseen_notifications(user.id)

    response = StreamingHttpResponse(
        notification_stream(notifications , user),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["Connection"] = "keep-alive"
    response["X-Accel-Buffering"] = "no"
    return response

@method_decorator(csrf_exempt, name='dispatch')
class notification_seen_API(APIView):
    def post(self , request):
        data = update_notification_status(request.user)

        return JsonResponse(data , status=201)
