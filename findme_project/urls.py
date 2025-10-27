from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.views.generic import TemplateView
from missing_persons import views as mp_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Головна сторінка
    path('', mp_views.home_page, name='home'),

    # Перегляд деталей
    path('person/<int:pk>/', mp_views.missing_detail, name='missing_detail'),

    # Додавання нового оголошення
    path('add/', mp_views.add_missing_person, name='add_missing'),

    # JWT + API маршрути
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('users.urls')),
    path('api/', include('missing_persons.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('messages.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


