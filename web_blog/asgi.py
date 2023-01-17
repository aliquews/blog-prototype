import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import blog_chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_blog.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            blog_chat.routing.websocket_urlpatterns,
        ),
    ),
})