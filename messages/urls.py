from rest_framework import routers
from .views import MessageViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = router.urls
