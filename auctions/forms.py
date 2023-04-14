from django import forms

from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['date']
        labels = {
            'url': 'Image URL:'
        }