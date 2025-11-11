from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile
from missing_persons.models import MissingPerson
from user_messages.models import Message

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  
            user.save()
            login(request, user)
            messages.success(request, f'👋 Вітаємо, {user.username}! Ви успішно зареєструвалися.')
            return redirect('home1')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile  
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')

        if username:
            user.username = username
        if email:
            user.email = email
        if phone:
            profile.phone = phone
        if bio:
            profile.bio = bio

        
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        user.save()
        profile.save()

        messages.success(request, "✅ Профіль успішно оновлено!")
        return redirect('profile')

    context = {
        'profile': profile,
        'user': user,
        'total_posts': MissingPerson.objects.filter(user=user).count(),
        'total_messages': Message.objects.filter(receiver=user).count(),
    }
    return render(request, 'profile.html', context)
