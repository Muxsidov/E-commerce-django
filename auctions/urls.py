from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("item/<int:id>", views.item_view, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path(
        "watchlist/add_to_watchlist/<int:id>",
        views.add_to_watchlist,
        name="user_wishlist",
    ),
    path("bid_to_listing/<str:listing>", views.bid_to_listing, name="bid_to_listing"),
    path("delete_product/<int:id>", views.delete_product, name="delete_product"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
