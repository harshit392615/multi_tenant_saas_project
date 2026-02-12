from rest_framework.throttling import SimpleRateThrottle

class OrganizationThrottling(SimpleRateThrottle):
    scope = 'free'

    def get_cache_key(self, request, view):
        if not hasattr(request, 'organization') or not request.organization:
            return None

        subscription = request.subscription 

        if not subscription:
            return self.cache_format % {
            'scope': 'free',
            'ident':request.organization.id
        }
        if subscription.is_active:
            scope = subscription.title
        else:
            scope = "free"

        return self.cache_format % {
            'scope': scope,
            'ident':request.organization.id
        }