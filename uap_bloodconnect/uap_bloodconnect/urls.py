from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('donors/', include('donors.urls')),
    path('requests/', include('bloodrequests.urls')),
]
