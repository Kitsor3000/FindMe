from django import forms
from .models import MissingPerson

class MissingPersonForm(forms.ModelForm):
    class Meta:
        model = MissingPerson
        fields = [
            'full_name',
            'birth_date',
            'missing_date',
            'region',
            'city',
            'description',
            'photo',
            'category',
            'status',
            'location',
            'latitude',
            'longitude',
        ]

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': "Наприклад: Іваненко Іван Іванович"
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control rounded-3'
            }),
            'missing_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control rounded-3'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': "Наприклад: Київська область"
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': "Наприклад: Київ"
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 3,
                'placeholder': "Короткий опис зовнішності, обставини зникнення..."
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': "Наприклад: вул. Соборна, 10"
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control rounded-3'})
    )
