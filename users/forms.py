from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Електронна пошта", required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ця електронна пошта вже використовується.")
        return email
    

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Ім’я користувача або Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введіть ім’я або email"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введіть пароль"})
    )
