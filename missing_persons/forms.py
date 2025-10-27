from django import forms
from .models import MissingPerson

class MissingPersonForm(forms.ModelForm):
    class Meta:
        model = MissingPerson
        fields = ['full_name', 'birth_date', 'missing_date', 'region', 'city', 'description', 'photo']
        photo = forms.ImageField(required=False)
