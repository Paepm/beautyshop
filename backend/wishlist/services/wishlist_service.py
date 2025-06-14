from wishlist.models import Wishlist, WishlistItem
from shop.models import Product


class WishlistService:
    @staticmethod
    def get_or_create_wishlist(user):
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        return wishlist

    @staticmethod
    def add_product(user, product_id):
        wishlist = WishlistService.get_or_create_wishlist(user)
        product = Product.objects.get(id=product_id)
        item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, product=product
        )
        return item

    @staticmethod
    def remove_product(user, product_id):
        wishlist = WishlistService.get_or_create_wishlist(user)
        WishlistItem.objects.filter(wishlist=wishlist, product_id=product_id).delete()

    @staticmethod
    def list_items(user):
        wishlist = WishlistService.get_or_create_wishlist(user)
        return wishlist.items.select_related("product")

    @staticmethod
    def clear_wishlist(user):
        wishlist = WishlistService.get_or_create_wishlist(user)
        wishlist.items.all().delete()
