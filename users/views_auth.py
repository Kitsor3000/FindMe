from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm

def login_view(request):
    error_message = None  # текст помилки для шаблону

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data["username_or_email"].strip()
            password = form.cleaned_data["password"]

            # 🔍 Знайти користувача за email або username
            user_obj = None
            if User.objects.filter(username=username_or_email).exists():
                user_obj = User.objects.get(username=username_or_email)
            elif User.objects.filter(email=username_or_email).exists():
                user_obj = User.objects.get(email=username_or_email)

            if user_obj:
                # 🧠 Авторизуємося тільки через username (не через email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    error_message = "❌ Невірний пароль."
            else:
                error_message = (
                    "❌ Користувача з такими даними не знайдено. "
                    "Будь ласка, <a href='/register/'>зареєструйтесь</a>."
                )
        else:
            error_message = "Будь ласка, заповніть усі поля."
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error_message": error_message})
