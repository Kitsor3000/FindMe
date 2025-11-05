from django import forms
from .models import Volunteer

class VolunteerApplyForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ["region", "city", "phone_number", "telegram", "viber", "description"]
        widgets = {
            "region": forms.TextInput(attrs={"class": "form-control rounded-3"}),
            "city": forms.TextInput(attrs={"class": "form-control rounded-3"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control rounded-3"}),
            "telegram": forms.TextInput(attrs={"class": "form-control rounded-3"}),
            "viber": forms.TextInput(attrs={"class": "form-control rounded-3"}),
            "description": forms.Textarea(attrs={"class": "form-control rounded-3", "rows": 3}),
        }
