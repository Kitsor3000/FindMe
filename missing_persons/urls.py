from rest_framework import routers
from .views import MissingPersonViewSet

router = routers.DefaultRouter()
router.register(r'missing', MissingPersonViewSet)

urlpatterns = router.urls
