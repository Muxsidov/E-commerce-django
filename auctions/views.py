from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Product, Bids, Comments, Category, Watchlist
from .forms import ProductForm, CommentForm


def index(request):
    activelistings = Product.objects.filter(closed=False)

    return render(request, "auctions/index.html", {"listings": activelistings})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    # Form for listings
    listing_form = ProductForm(request.POST, request.FILES)

    if request.method == "POST":
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.created_by = request.user
            if Product.objects.filter(category__name=category).exists():
                listing.category.add(category)

            listing.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {"listing_form": listing_form})


# Add to watchlist button (check whether the user logged in)
@login_required(login_url="login")
def add_to_watchlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
    else:
        product.user_wishlist.add(request.user)
    return HttpResponseRedirect("/watchlist")


# Show the watchlist
def watchlist(request):
    listing = Product.objects.filter(user_wishlist=request.user)

    return render(request, "auctions/index.html", {"listings": listing})


def categories(request):
    categories = Category.objects.all()
    if categories:
        return render(request, "auctions/categories.html", {"categories": categories})
    else:
        return HttpResponse("Categories are empty!")


def category(request, category):
    categories = Product.objects.filter(category__name=category)

    if categories:
        return render(request, "auctions/index.html", {"listings": categories})
    else:
        return HttpResponse("Categories are empty!")


# Display all listings
def item_view(request, id):

    item = Product.objects.get(id=id)
    comment_form = CommentForm(request.POST)
    comment = Comments()

    if request.method == "POST":
        if comment_form.is_valid():
            comment.name = comment_form.cleaned_data["name"]
            comment.body = comment_form.cleaned_data["body"]
            comment.post = item
            comment.save()

    if item:
        return render(
            request,
            "auctions/listing.html",
            {"listing": item, "comment_form": comment_form},
        )
    else:
        raise Http404("No listing is provided")


def bid_to_listing(request, listing):

    comment_form = CommentForm(request.POST)

    if request.method == "POST":
        auction_to_add = Product.objects.get(id=listing)
        total_bid = int(request.POST["totalBid"])
        if (total_bid < int(auction_to_add.current_price)) or (
            auction_to_add.bidded is not None
            and total_bid < int(auction_to_add.bidded.bid)
        ):
            return render(
                request,
                "auctions/listing.html",
                {
                    "message": "Bid must be more than current price",
                    "listing": auction_to_add,
                    "comment_form": comment_form,
                },
            )
        bid = Bids.objects.create(
            user=request.user, auction=auction_to_add, bid=total_bid
        )
        auction_to_add.bids.add(bid)
        auction_to_add.bidded = bid
        auction_to_add.save()

        return HttpResponseRedirect(reverse("index"))


def delete_product(request, id):
    if request.method == "GET":
        product = Product.objects.get(id=id)
        if product.created_by == request.user:
            try:
                product.delete()
                return HttpResponseRedirect(reverse("index"))
            except ProtectedError:
                return HttpResponse("You cannot remove this item!")


def close_listing(request, id):
    if request.method == "GET":
        product_object = Product.objects.get(id=id)
        product_object.closed = True
        product_object.save()

        return HttpResponseRedirect(reverse("index"))
