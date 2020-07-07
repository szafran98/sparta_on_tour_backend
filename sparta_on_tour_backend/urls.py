from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),
    path('auth/', CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
