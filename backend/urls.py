from rest_framework import routers
from django.urls import include, path
from .views import EventViewSet, ParticipantViewSet
from users.views import UserViewSet


router = routers.DefaultRouter()
router.register('events', EventViewSet)
router.register('participants', ParticipantViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]