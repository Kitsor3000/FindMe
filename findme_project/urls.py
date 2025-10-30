from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from users import views as user_views
from user_messages import views as msg_view
from users import views_auth


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.views.generic import TemplateView
from missing_persons import views as mp_views

def logout_view(request):
    logout(request)
    return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('', mp_views.home_page, name='home'),

   
    path('person/<int:pk>/', mp_views.missing_detail, name='missing_detail'),

  
    path('add/', mp_views.add_missing_person, name='add_missing'),

    path('login/', views_auth.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('my-posts/', mp_views.my_posts, name='my_posts'),

     path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),

     path('register/', user_views.register_view, name='register'),
    path('person/<int:pk>/edit/', mp_views.edit_missing_person, name='edit_missing'),
path('person/<int:pk>/delete/', mp_views.delete_missing_person, name='delete_missing'),

    # JWT + API маршрути
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('', include('users.urls')),
    path('api/', include('missing_persons.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('user_messages.urls')),

      path('chat/', include('user_messages.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


