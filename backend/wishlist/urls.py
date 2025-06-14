from django.urls import path
from wishlist.views.views import WishlistView, WishlistAddRemoveView

app_name = "wishlist"

urlpatterns = [
    path("", WishlistView.as_view(), name="wishlist-detail"),
    path("add/<int:product_id>/", WishlistAddRemoveView.as_view(), name="wishlist-add"),
    path(
        "remove/<int:product_id>/",
        WishlistAddRemoveView.as_view(),
        name="wishlist-remove",
    ),
]
