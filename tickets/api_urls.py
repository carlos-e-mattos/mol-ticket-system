from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import ClienteViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]