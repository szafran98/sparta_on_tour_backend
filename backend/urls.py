from rest_framework import routers
from django.urls import include, path
from .views import EventViewSet, ParticipantViewSet


router = routers.DefaultRouter()
router.register('events', EventViewSet)
router.register('participant', ParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]