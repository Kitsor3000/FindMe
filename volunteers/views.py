from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from missing_persons.models import MissingPerson
from .models import Volunteer, VolunteerParticipation
from .forms import VolunteerApplyForm


@login_required
def become_volunteer(request):
    """Форма подачі заявки на волонтера"""
    if hasattr(request.user, "volunteer_profile"):
        return redirect("volunteer_dashboard")

    if request.method == "POST":
        form = VolunteerApplyForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.user = request.user
            volunteer.save()
            messages.success(request, "✅ Ви стали волонтером FindMe!")
            return redirect("volunteer_dashboard")
    else:
        form = VolunteerApplyForm()

    return render(request, "volunteer_apply.html", {"form": form})


@login_required
def volunteer_dashboard(request):
    """Кабінет волонтера — показує зниклих у його регіоні (без знайдених)"""
    volunteer = request.user
    if not hasattr(volunteer, "volunteer_profile"):
        return redirect("become_volunteer")

    region = volunteer.volunteer_profile.region

    # ❗ Показуємо лише зниклих ("missing")
    persons = MissingPerson.objects.filter(
        region__icontains=region,
        status="missing"
    ).order_by("-created_at")

    joined_person_ids = VolunteerParticipation.objects.filter(
        volunteer=volunteer
    ).values_list('person_id', flat=True)

    # Дані для карти
    persons_data = [
        {
            "id": p.id,
            "full_name": p.full_name,
            "city": p.city,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "photo": p.photo.url if p.photo else None,
        }
        for p in persons if p.latitude and p.longitude
    ]

    return render(request, "volunteer_dashboard.html", {
        "persons": persons,
        "joined_person_ids": joined_person_ids,
        "persons_data": persons_data,
        "region": region
    })


@login_required
def join_search(request, person_id):
    """Приєднання волонтера до пошуку конкретної людини"""
    person = get_object_or_404(MissingPerson, id=person_id)
    participation, created = VolunteerParticipation.objects.get_or_create(
        volunteer=request.user,
        person=person
    )

    if created:
        messages.success(request, f"Ви приєднались до пошуку {person.full_name} ✅")
    else:
        messages.info(request, f"Ви вже берете участь у пошуку {person.full_name}")

    return redirect("volunteer_dashboard")
