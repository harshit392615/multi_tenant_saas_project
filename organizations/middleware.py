from .models import Organization , Membership
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class TenantMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        org_slug = request.headers.get("X-ORG-SLUG")

        if not org_slug:
            request.organization = None
            request.membership = None
            return None

        try: 
            organization = Organization.objects.get(slug = org_slug , is_active = True)
        except Organization.DoesNotExist:
            return HttpResponseForbidden('organization does not exist')
        
        request.organization = organization

        if hasattr(request,'user') and request.user.is_authenticated:
            try:
                request.membership = Membership.objects.get(user = request.user , organization = organization)
            except Membership.DoesNotExist:
                return HttpResponseForbidden('No access to this organization')
        else:
            request.membership = None
        return None

