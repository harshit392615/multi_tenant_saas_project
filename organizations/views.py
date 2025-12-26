from rest_framework.views import APIView
from common.exceptions import PermissionDenied

# Create your views here

class TenantAPIviews(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
    
        if not request.membership:
            return PermissionDenied("you cannot access this organization")