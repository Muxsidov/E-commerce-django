from django.contrib import admin
from .models import Product, Bids, Comments, Category, Watchlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    # prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "current_price",
    ]
    # prepopulated_fields = {'slug': ('title',)}


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["name", "body"]


@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = ["auction", "bid"]
