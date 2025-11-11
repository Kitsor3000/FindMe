from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import MissingPerson
from .serializers import MissingPersonSerializer
from django.contrib import messages
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now, timedelta
import json
from datetime import date
from django.db.models.functions import TruncWeek, TruncMonth, TruncYear
from django.http import JsonResponse
from django.core.paginator import Paginator
from volunteers.models import Volunteer, VolunteerParticipation
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import MissingPerson





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
    query = request.GET.get('q', '').strip()
    city = request.GET.get('city', '').strip()
    date = request.GET.get('date', '').strip()
    sort = request.GET.get("sort", "").strip()

    persons = MissingPerson.objects.all().order_by('-created_at')

    if query:
        persons = persons.filter(full_name__icontains=query)
    if city:
        persons = persons.filter(city__icontains=city)
    if date:
        persons = persons.filter(missing_date=date)

    #  Сортування
    if sort == "name_asc":
        persons = persons.order_by("full_name")
    elif sort == "name_desc":
        persons = persons.order_by("-full_name")
    elif sort == "date_oldest":
        persons = persons.order_by("missing_date")
    elif sort == "date_latest":
        persons = persons.order_by("-missing_date")
    elif sort == "city":
        persons = persons.order_by("city")
    else:
        persons = persons.order_by("-created_at")

    # Пагінація — по 9 елементів
    paginator = Paginator(persons, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'persons': page_obj.object_list,  
        'query': query,
        'city': city,
        'date': date,
        'sort': sort,
    }
    return render(request, 'home.html', context)

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


@staff_member_required
def admin_dashboard(request):
    """Основна сторінка аналітики (рендер шаблону)."""
    today = now().date()
    last_week = today - timedelta(days=6)

    #  Дані про статуси зниклих
    status_data = dict(
        MissingPerson.objects.values_list("status").annotate(total=Count("status"))
    )

    #  Топ 7 регіонів
    region_data_qs = (
        MissingPerson.objects.values("region")
        .annotate(total=Count("region"))
        .order_by("-total")[:7]
    )
    region_data = {r["region"]: r["total"] for r in region_data_qs}

    #  Нові за останній тиждень
    daily_counts = (
        MissingPerson.objects.filter(created_at__date__gte=last_week)
        .extra({"day": "date(created_at)"})
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )
    weekly_data = {
        (d["day"].strftime("%d.%m") if hasattr(d["day"], "strftime") else str(d["day"])): d["total"]
        for d in daily_counts
    }

    # Дані про волонтерів
    total_volunteers = Volunteer.objects.count()
    active_volunteers = VolunteerParticipation.objects.values("volunteer").distinct().count()
    total_participations = VolunteerParticipation.objects.count()

    volunteer_stats = {
        "total_volunteers": total_volunteers,
        "active_volunteers": active_volunteers,
        "participations": total_participations,
    }

    context = {
        "status_data": json.dumps(status_data, ensure_ascii=False),
        "region_data": json.dumps(region_data, ensure_ascii=False),
        "weekly_data": json.dumps(weekly_data, ensure_ascii=False),
        "volunteer_stats": volunteer_stats,
    }

    return render(request, "admin_dashboard.html", context)





@staff_member_required
def get_chart_data(request):
    """AJAX-ендпоінт, який повертає JSON із потрібним періодом."""
    period = request.GET.get("period", "week")
    today = now().date()

    # Вибираємо період
    if period == "week":
        start_date = today - timedelta(days=7)
        trunc = TruncWeek
    elif period == "month":
        start_date = today - timedelta(days=30)
        trunc = TruncWeek  
    else:
        start_date = today - timedelta(days=365)
        trunc = TruncMonth

    qs = MissingPerson.objects.filter(created_at__date__gte=start_date)

    status_data = dict(qs.values_list("status").annotate(total=Count("status")))
    region_qs = qs.values("region").annotate(total=Count("region")).order_by("-total")[:7]
    region_data = {r["region"]: r["total"] for r in region_qs}


    # Тренд у часі
    if period == "year":
        date_field = "month"
        time_data = (
            qs.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )
        weekly_data = {
            (d["month"].strftime("%b") if hasattr(d["month"], "strftime") else str(d["month"])): d["total"]
            for d in time_data
        }
    else:
        time_data = (
            qs.annotate(week=trunc("created_at"))
            .values("week")
            .annotate(total=Count("id"))
            .order_by("week")
        )
        weekly_data = {
            (d["week"].strftime("%d.%m") if hasattr(d["week"], "strftime") else str(d["week"])): d["total"]
            for d in time_data
        }

    return JsonResponse({
        "status_data": status_data,
        "region_data": region_data,
        "weekly_data": weekly_data,
    })





def map_view(request):
    category = request.GET.get('category', 'all')

    #  Мапа відповідності між українськими назвами та кодами з моделі
    category_map = {
        "Дитина": "child",
        "Дорослий": "adult",
        "Літня людина": "elderly",
        "Військовий": "military",
        "Людина з інвалідністю": "disabled",
        "Інше": "other",
    }

    # Фільтрація за категорією
    if category == 'all':
        persons = MissingPerson.objects.all()
    else:
        db_value = category_map.get(category)
        if db_value:
            persons = MissingPerson.objects.filter(category=db_value)
        else:
            persons = MissingPerson.objects.none()

    # Формування списку даних для карти
    persons_data = []
    for p in persons:
        if p.latitude and p.longitude:
            persons_data.append({
                "id": p.id,
                "full_name": p.full_name,
                "city": p.city,
                "region": p.region,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "category": dict(MissingPerson.CATEGORY_CHOICES).get(p.category, p.category),  # показує українську
                "status": p.status,
                "photo": p.photo.url if p.photo else None,
            })

    return render(request, "map.html", {
        "persons": persons_data,
        "selected_category": category,
    })






def home_view(request):
    news = [
        {
            "title": "Волонтери об’єдналися для пошуку у Харкові",
            "description": "Більше 40 людей долучились до пошуку у регіоні.",
            "image": "/static/images/news1.jpg",
        },
        {
            "title": "Знайдено 12 людей за минулий тиждень",
            "description": "Завдяки активності користувачів і поліції вдалося відшукати 12 осіб.",
            "image": "/static/images/news2.jpg",
        },
        {
            "title": "Пошукова операція на Донеччині: знайдено двох військових",
            "description": "Волонтери та поліція об’єднали зусилля для пошуку зниклих військових. Обидва чоловіки знайдені живими та передані лікарям.",
            "image": "/static/images/news3.jpg",
        },
    ]

    stats = {
        "total_missing": MissingPerson.objects.count(),
        "found": MissingPerson.objects.filter(status="found").count(),
        "volunteers": 134,
        "active_users": 89,
    }

    context = {
        "news": news,
        "stats": stats,
        "year": date.today().year
    }

    return render(request, "home1.html", context)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_missing_persons_list(request):
    persons = MissingPerson.objects.all().values(
        'id', 'full_name', 'status', 'city', 'region', 'category', 'missing_date'
    )
    return Response({'persons': list(persons)})