from rest_framework.views import APIView
from .selectors import get_org_activity , get_entity_activity
from rest_framework.response import Response
from .serializers import ActivitySerializer
from rest_framework.exceptions import ValidationError

# Create your views here.
class OrgActivityList(APIView):
    def get(self , request ):
        try:
            limit = int(request.query_params.get('limit' , 50))
        except (ValueError , TypeError):
            limit = 50

        limit = min(limit , 100)

        activity = get_org_activity(organization=request.organization,limit=limit)

        serializer = ActivitySerializer(activity , many = True)
        return Response(serializer.data)
    
class EntityActivityList(APIView):
    def get(self , request ,entity_id):
        try:
            limit = int(request.query_params.get('limit' , 50))
        except (ValueError , TypeError):
            limit = 50

        limit = min(limit , 100)

        activity = get_entity_activity(organization=request.organization,entity_id=entity_id,limit=limit)
        serializer = ActivitySerializer(activity , many = True)
        return Response(serializer.data)
