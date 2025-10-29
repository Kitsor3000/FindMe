from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import MissingPerson
from .serializers import MissingPersonSerializer
from django.contrib import messages
from comments.models import Comment
from django.contrib.auth.decorators import login_required



class MissingPersonViewSet(viewsets.ModelViewSet):
    queryset = MissingPerson.objects.all().order_by('-created_at')
    serializer_class = MissingPersonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region', 'city', 'status']
    search_fields = ['full_name', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



from django.shortcuts import render, get_object_or_404, redirect

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
    comments = person.comments.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        if text.strip():
            Comment.objects.create(user=request.user, person=person, text=text)

    return render(request, 'missing_detail.html', {'person': person, 'comments': comments})


@login_required

def my_posts(request):
    persons = MissingPerson.objects.filter(user=request.user)
    return render(request, 'my_posts.html', {'persons': persons})

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


@login_required
def edit_missing_person(request, pk):
    person = get_object_or_404(MissingPerson, pk=pk)
    if request.user != person.user and not request.user.is_superuser:
        messages.error(request, "Ви не можете редагувати це оголошення.")
        return redirect('home')

    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, "Оголошення оновлено.")
            return redirect('missing_detail', pk=pk)
    else:
        form = MissingPersonForm(instance=person)
    return render(request, 'add_missing.html', {'form': form, 'edit': True})


@login_required
def delete_missing_person(request, pk):
    person = get_object_or_404(MissingPerson, pk=pk)
    if request.user == person.user or request.user.is_superuser:
        person.delete()
        messages.success(request, "Оголошення видалено.")
    else:
        messages.error(request, "Ви не можете видалити це оголошення.")
    return redirect('home')