from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
