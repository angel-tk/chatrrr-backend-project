from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, getRoutes

router = DefaultRouter()
router.register('rooms', RoomViewSet, basename='rooms')

urlpatterns = [
    path('', getRoutes, name='get-routes'),
    path('', include(router.urls)),
]
