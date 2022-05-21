from django import forms
from .models import UserBookRelation, RATE_CHOICES


class RateForm(forms.ModelForm):
    rate = forms.MultipleChoiceField(choices=RATE_CHOICES, required=False,
                                     widget=forms.RadioSelect)

    class Meta:
        model = UserBookRelation
        fields = ('rate', )
