from django import forms
from .models import MissingPerson

class MissingPersonForm(forms.ModelForm):
    REGION_CHOICES = [
        ("Вінницька область", "Вінницька область"),
        ("Волинська область", "Волинська область"),
        ("Дніпропетровська область", "Дніпропетровська область"),
        ("Донецька область", "Донецька область"),
        ("Житомирська область", "Житомирська область"),
        ("Закарпатська область", "Закарпатська область"),
        ("Запорізька область", "Запорізька область"),
        ("Івано-Франківська область", "Івано-Франківська область"),
        ("Київська область", "Київська область"),
        ("Кіровоградська область", "Кіровоградська область"),
        ("Луганська область", "Луганська область"),
        ("Львівська область", "Львівська область"),
        ("Миколаївська область", "Миколаївська область"),
        ("Одеська область", "Одеська область"),
        ("Полтавська область", "Полтавська область"),
        ("Рівненська область", "Рівненська область"),
        ("Сумська область", "Сумська область"),
        ("Тернопільська область", "Тернопільська область"),
        ("Харківська область", "Харківська область"),
        ("Херсонська область", "Херсонська область"),
        ("Хмельницька область", "Хмельницька область"),
        ("Черкаська область", "Черкаська область"),
        ("Чернівецька область", "Чернівецька область"),
        ("Чернігівська область", "Чернігівська область"),
        ("м. Київ", "м. Київ"),
    ]

    region = forms.ChoiceField(
        choices=REGION_CHOICES,
        label="Область",
        widget=forms.Select(attrs={"class": "form-control rounded-3", "id": "regionSelect"})
    )

    city = forms.CharField(
        label="Місто",
        widget=forms.TextInput(attrs={
            "class": "form-control rounded-3",
            "placeholder": "Введіть або оберіть місто...",
            "list": "cityList",  
            "id": "cityInput"
        })
    )
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
