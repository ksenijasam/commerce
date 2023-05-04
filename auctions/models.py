from django.contrib.auth.models import AbstractUser
from django.db import models

    
class User(AbstractUser):
    pass

class Listing(models.Model):
    FASHION = 'FSHN'
    TOYS = 'TYS'
    ELECTRONICS = 'LCTRNCS'
    HOME = 'HME'
    BOOKS = 'BKS'
    STATIONARY = 'STTNRY'
    OTHER = 'THR'
    CATEGORY_CHOICES = [
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home'),
        (BOOKS, 'Books'),
        (STATIONARY, 'Stationary'),
        (OTHER, 'Other')
    ]
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.FloatField()
    url = models.URLField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, null=True, blank=True, max_length=15)
    date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_listing')
    winner_id = models.IntegerField(null=True, blank=True)

class Bids(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = 'listing_bids')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_bids')

class Comments(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = 'listing_comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_comments')

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = 'listing')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user')

