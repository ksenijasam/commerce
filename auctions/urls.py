from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist/<int:id>/<str:action>", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("won_listings", views.won_listings, name="won_listings"),
    path("won_listings_details/<int:id>", views.won_listings_details, name="won_listings_details"),
    path("comments/<int:id>", views.comments, name="comments"),
    path("watchlist_list", views.watchlist_list, name="watchlist_list"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category")
]
