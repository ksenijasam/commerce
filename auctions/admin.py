from django.contrib import admin

from .models import User, Listing, Bids, Comments, Watchlist

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)

