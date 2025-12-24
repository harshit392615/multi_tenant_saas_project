from .models import Organization , Membership
from django.http import HttpResponseForbidden

class TenantMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        org_slug = request.headers.get("X-ORG-SLUG")

        if not org_slug:
            request.organization = None
            return self.get_response(request)

        try: 
            organization = Organization.objects.get(slug = org_slug , is_active = True)
        except Organization.DoesNotExist:
            return HttpResponseForbidden('organization does not exist')
        
        request.organization = organization

        if request.user.is_authenticated:
            try:
                request.membership = Membership.objects.get(user = request.user , organization = organization)
            except Membership.DoesNotExist:
                return HttpResponseForbidden('No access to this organization')
        else:
            request.membership = None

        return self.get_response(request)

