from rest_framework.throttling import SimpleRateThrottle

class OrganizationThrottling(SimpleRateThrottle):
    scope = 'organization'

    def get_cache_key(self, request, view):
        if not request.membership:
            return None
        
        return f'throllle_org_{request.organization.id}'