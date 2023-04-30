from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm, CommentsForm
from .models import Listing
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import User, Watchlist, User, Bids, Comments


def index(request):
    listings = Listing.objects.all().filter(active=True)
    if(listings is None):
        return render(request, "auctions/index.html", {
            'no_listings': 'Currently there are no available listings. Be free to join community and create your own listing!'
        })

    return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        user = User.objects.get(pk = request.user.pk)

        if form.is_valid():
            form.instance.user = user
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            'form': form
        })

def listing(request, id):
    if id is not None:
        listing = Listing.objects.get(pk = id)
        bids = Bids.objects.all().filter(listing = listing)

        comments = Comments.objects.all().filter(listing = listing)

        comment_form = CommentsForm()

        its_creator = False

        if request.user == listing.user:
            its_creator = True

        if Watchlist.objects.filter(listing = listing).exists():
            return render(request, "auctions/listing.html", {
            'listing': listing,
            'on_watchlist': True,
            'bids': bids,
            'its_creator': its_creator,
            'comment_form': comment_form,
            'comments': comments
        })


        return render(request, "auctions/listing.html", {
            'listing': listing,
            'on_watchlist': False,
            'bids': bids,
            'its_creator': its_creator,
            'comment_form': comment_form,
            'comments': comments
        })

def watchlist(request, id, action):
    if id is not None:
        watchlist = Watchlist()
        listing = Listing.objects.get(pk = id)
        bids = Bids.objects.all().filter(listing = listing)
        user = User.objects.get(pk = request.user.pk)
        if action == 'add':
            watchlist.user = user
            watchlist.listing = listing
            watchlist.save()
            return render(request, "auctions/listing.html", {
                'listing': listing,
                'added_to_watchlist': True,
                'bids': bids,
                'comment_form': CommentsForm()
            })
        
        # Watchlist.objects.filter(listing = listing, user = user).delete()
        return render(request, "auctions/listing.html", {
            'listing': listing,
            'added_to_watchlist': False,
            'bids': bids,
            'comment_form': CommentsForm()
        })

@login_required
def bid(request, id):
    if request.method == 'POST' and id is not None:
        listing = Listing.objects.get(pk = id)
        bids = Bids.objects.all().filter(listing = listing)
        user = User.objects.get(pk = request.user.pk)
        bid = request.POST.get('bid')

        comment_form = CommentsForm()

        for item in bids:
            if float(item.bid) >= float(bid):
                return render(request, "auctions/listing.html", {
                'listing': listing,
                'error_other_user': True,
                'bids': bids,
                'comment_form': comment_form
            })
                
        if float(listing.starting_bid) >= float(bid):
            return render(request, "auctions/listing.html", {
                'listing': listing,
                'error_owner': True,
                'bids': bids,
                'comment_form': comment_form
            })

        bids = Bids()
        bids.bid = float(bid)
        bids.listing = listing
        bids.user = user
        bids.save()

        bids = Bids.objects.all().filter(listing = listing)

        return render(request, "auctions/listing.html", {
            'listing': listing,
            'bids': bids,
            'comment_form': comment_form
        })

@login_required
def close_listing(request, id):
    if id is not None:
        listing = Listing.objects.get(pk = id)
        bids = Bids.objects.all().filter(listing = listing)

        max_bid = bids.aggregate(Max('bid'))['bid__max']
        
        winning_bid = bids.get(bid = max_bid)
        winning_user = winning_bid.user
        winner = User.objects.get(pk = winning_user.pk)

        listing.winner_id = winner.pk
        listing.active = False
        listing.save()

        return render(request, "auctions/listing.html", {
            'listing': listing,
            'added_to_watchlist': False, #not good, watchlist should be removed altogether if
            'bids': bids,                #item is closed                    
            'its_creator': False
        })

@login_required
def won_listings(request):
    won_listing = Listing.objects.all().filter(winner_id = request.user.pk)
    
    return render(request, "auctions/won_listings.html", {
        'won_listing': won_listing
    })

@login_required
def won_listings_details(request, id):
    won_listings_details = Listing.objects.get(pk = id)
    
    return render(request, "auctions/won_listing_details.html", {
        'won_listings_details': won_listings_details
    })

@login_required
def comments(request, id):
    if request.method == 'POST':
        user = User.objects.get(pk = request.user.pk)
        listing = Listing.objects.get(pk = id)
        comments = Comments.objects.all().filter(listing = listing)

        comment_form = CommentsForm(request.POST)

        if comment_form.is_valid():
            comment_form.instance.listing = listing
            comment_form.instance.user = user
            comment_form.save()

        return render(request, "auctions/listing.html", {
            'listing': listing,
            'comment_form': CommentsForm(),
            'comments': comments
        })


@login_required
def watchlist_list(request):
    watchlist_list = Watchlist.objects.all().filter(user = request.user.pk)
    print(watchlist_list[0].listing.title)
    return render(request, "auctions/watchlist.html", {
        'watchlist_list': watchlist_list
    })



