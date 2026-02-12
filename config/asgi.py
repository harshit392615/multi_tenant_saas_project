"""
ASGI config for multi_tenant_saas_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter , URLRouter
import notes.routing 
from channels.auth import AuthMiddlewareStack
from core.middleware import JWTAuthenticationMiddleware , OrganizationMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    'websocket':AuthMiddlewareStack(JWTAuthenticationMiddleware(OrganizationMiddleware(URLRouter(notes.routing.websocket_urlpatterns))))
})
