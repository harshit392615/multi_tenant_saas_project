from django.shortcuts import render
from organizations.views import TenantAPIviews
from core.throttles import OrganizationThrottling
from .selectors import get_notes
from .serializers import notes_Serializer , notes_Create_Serializer
from rest_framework import status
from rest_framework.response import Response
from .services import create_note , Delete_Note

# Create your views here.

class Notes_List_create(TenantAPIviews):
   throttle_classes = [OrganizationThrottling]
   def get(self , request , workspace_slug):
      notes = get_notes(workspace_slug , request.membership , request.organization)
      serializer = notes_Serializer(notes , many = True)
      return Response(serializer.data , status = status.HTTP_202_ACCEPTED)

   def post(self , request , workspace_slug):
      serializer = notes_Create_Serializer(data = request.data)
      if serializer.is_valid():
         note = create_note(workspace_slug , request.membership , request.organization , serializer.validated_data)
         serializer = notes_Serializer(note)
         return Response(serializer.data , status=status.HTTP_201_CREATED)


class Note_Delete_API(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def delete(self , request , board_id):
        try:
            Delete_Note(id=board_id , actor=request.membership)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error' : str(e)},status=status.HTTP_400_BAD_REQUEST)