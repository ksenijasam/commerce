from django import forms

from .models import Listing, Comments

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['date', 'active', 'user', 'winner_id']
        labels = {
            'url': 'Image URL:'
        }
        required = ('title', 'description', 'starting_bid')

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['user', 'listing']