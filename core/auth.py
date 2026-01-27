# auth/bearer.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


jwt_auth = JWTAuthentication()

def authenticate_bearer(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise AuthenticationFailed("Authorization header missing")

    try:
        scheme, token = auth_header.split()
    except ValueError:
        raise AuthenticationFailed("Invalid Authorization header format")

    validated_token = jwt_auth.get_validated_token(token)
    user = jwt_auth.get_user(validated_token)

    return user

def authenticate_bearer_by_token(token):
    validated_token = jwt_auth.get_validated_token(token)
    user = jwt_auth.get_user(validated_token)

    return user