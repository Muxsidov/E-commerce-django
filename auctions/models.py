from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(
        max_length=30, db_index=True, null=True, default="", blank=True
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=30, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="product_creator",
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=200, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="photos/")
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="product",
        null=True,
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    user_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True
    )
    bidded = models.ForeignKey(
        "Bids",
        on_delete=models.SET_NULL,
        related_name="last_bid_for_the_auction",
        blank=True,
        null=True,
    )
    closed = models.BooleanField(default=False)
    bids = models.ManyToManyField(
        "Bids", related_name="bids_in_the_auction", blank=True
    )

    class Meta:
        ordering = ("-created_date",)

    def __str__(self):
        return self.title


class Bids(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_who_make_the_bid"
    )
    auction = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="auction_for_the_bid"
    )
    bid = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True
    )
    item = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user}: {self.item}"


class Comments(models.Model):
    post = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.body}"
