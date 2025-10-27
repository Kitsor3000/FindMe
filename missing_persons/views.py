from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import MissingPerson
from .serializers import MissingPersonSerializer

# --- REST API ---
class MissingPersonViewSet(viewsets.ModelViewSet):
    queryset = MissingPerson.objects.all().order_by('-created_at')
    serializer_class = MissingPersonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region', 'city', 'status']
    search_fields = ['full_name', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- HTML В’юхи ---
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import MissingPersonForm

def home_page(request):
    query = request.GET.get('q')
    if query:
        persons = MissingPerson.objects.filter(full_name__icontains=query)
    else:
        persons = MissingPerson.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'persons': persons})

def missing_detail(request, pk):
    person = get_object_or_404(MissingPerson, pk=pk)
    return render(request, 'missing_detail.html', {'person': person})

@login_required
def add_missing_person(request):
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            missing = form.save(commit=False)
            missing.user = request.user
            missing.save()
            return redirect('home')
    else:
        form = MissingPersonForm()
    return render(request, 'add_missing.html', {'form': form})
