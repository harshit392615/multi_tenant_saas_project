from rest_framework.throttling import SimpleRateThrottle

class OrganizationThrottling(SimpleRateThrottle):
    scope = 'organization'

    def get_cache_key(self, request, view):
        if not hasattr(request, 'organization') or not request.organization:
            return None
        return f'throttle_org_{request.organization.id}'