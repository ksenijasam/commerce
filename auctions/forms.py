from django import forms

from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['date', 'active']
        labels = {
            'url': 'Image URL:'
        }
        required = ('title', 'description', 'starting_bid')