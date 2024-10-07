from django.contrib import admin
from django.urls import include, path

API_VERSION = 'v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]
