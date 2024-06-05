from django.contrib import admin
from django.urls import path
from django.urls import path, include
urlpatterns = [
    path('', admin.site.urls),
    path('api/',include('api_service.urls')),
]
