from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import MissingPerson
from .serializers import MissingPersonSerializer

class MissingPersonViewSet(viewsets.ModelViewSet):
    """
    API для роботи з оголошеннями про зниклих людей.
    - Авторизовані користувачі можуть створювати/редагувати.
    - Неавторизовані бачать лише список.
    """
    queryset = MissingPerson.objects.all().order_by('-created_at')
    serializer_class = MissingPersonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Пошук і фільтрація
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region', 'city', 'status']
    search_fields = ['full_name', 'description']

    def perform_create(self, serializer):
        # Автоматично прив’язує користувача, який створює запис
        serializer.save(user=self.request.user)
