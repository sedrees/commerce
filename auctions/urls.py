from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_auction", views.new_auction, name="new_auction"),
    path("auctions/<str:id>", views.listing, name="listing"),
    path("watch/<str:id>", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close/<str:id>", views.close, name="close"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.category, name="category")
]
