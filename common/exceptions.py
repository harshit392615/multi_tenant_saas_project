from rest_framework.exceptions import APIException

class PermissionDenied(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"

class ValidationError(APIException):
    status_code = 403
    default_detail = "your request is invalid"
    default_code = "invalid request"