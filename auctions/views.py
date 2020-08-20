from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from auctions.models import Auction, Watchlist, Bid
from .models import User

CATEGORIES = [
    ('antiques', 'Antiques'), 
    ('collectables', 'Collectables'), 
    ('electronics', 'Electronics'), 
    ('entertainment', 'Entertainment'), 
    ('fashion', 'Fashion'), 
    ('health', 'Health & Beauty'), 
    ('home', 'Home & Garden'), 
    ('jewelry', 'Jewelry'), 
    ('office', 'Office'), 
    ('toys', 'Toys')
    ]

class CreateListing(forms.Form):
    title = forms.CharField(empty_value="Listing Title", max_length=255)
    category = forms.ChoiceField(choices=CATEGORIES, widget=forms.Select)
    img = forms.CharField(required=False, label="Listing Photo URL")
    description = forms.CharField(empty_value="Description", widget=forms.Textarea, max_length=2000)
    start = forms.IntegerField(label="Starting Bid", help_text="USD", min_value=1, max_value=1000000)

def index(request):
    return render(request, "auctions/index.html", {
        "objects":Auction.objects.filter(active=True)
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

@login_required
def new_auction(request):
    if request.method == 'POST':
        form = CreateListing(request.POST)
        if form.is_valid():
            seller = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid_starting = form.cleaned_data["start"]
            category = form.cleaned_data["category"]
            bid = Bid(bidder=seller, bid=bid_starting)
            bid.save()
            new = Auction(
                seller=seller,
                title = title,
                description = description,
                bid_starting = bid_starting,
                bid_current = bid,
                category = category,
                active = True
            )          
            if request.POST["img"]:
                img = form.cleaned_data["img"]
                new.img = img
            new.save()
            
            return render(request, "auctions/index.html")
        else:
            return render(request, "auctions/error.html", {
                "message":"Error processing form data."
            })
    else:
        return render(request, "auctions/create.html", {
            "form":CreateListing()
        })

def listing(request, id):
    auction = Auction.objects.get(pk=id)
    if request.method == "POST":
        bid = float(request.POST["bid"])
        if bid > auction.bid_current.bid:
            new = Bid(
                bidder=request.user,
                bid=bid
            )
            new.save()
            auction.bid_current = new
            auction.save()
            return HttpResponseRedirect(reverse("listing", args=[auction.pk]))
        else:
            return render(request, "auctions/error.html", {
                "message":"New bid must be greater than current bid."
            })
        
    else:
        if Watchlist.objects.filter(user=request.user, auction=auction):
            is_watching = True
        else:
            is_watching = False
        return render(request, "auctions/listing.html", {
            "auction":auction,
            "is_watching":is_watching
        })

@login_required
def watch(request, id):
    auction = Auction.objects.get(pk=id)
    watching = Watchlist.objects.filter(user=request.user)
    for row in watching:
        if row.auction == auction:
            row.delete()
            return HttpResponseRedirect(reverse("listing", args=[auction.pk]))
    new = Watchlist(user=request.user, auction=auction)
    new.save()
    return HttpResponseRedirect(reverse("listing",  args=[auction.pk]))

def close(request, id):
    auction = Auction.objects.get(pk=id)
    auction.winner = auction.bid_current.bidder
    auction.active = False
    auction.save()
    return HttpResponseRedirect(reverse("index"))