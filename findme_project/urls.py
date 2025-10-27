from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('users.urls')),
    path('api/', include('missing_persons.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('user_messages.urls')),
]


