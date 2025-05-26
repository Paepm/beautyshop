import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beautyshop.settings')
django.setup()

from shop.models import Category, Item

# define categories
categories = {
    'Parfum': Category.objects.get_or_create(name='Parfum', slug='parfum')[0],
    'Creme': Category.objects.get_or_create(name='Creme', slug='creme')[0],
    'Shampoo': Category.objects.get_or_create(name='Shampoo', slug='shampoo')[0],
}

# define products
products = [
    {
        'name': '1million',
        'slug': '1million',
        'category': categories['Parfum'],
        'price': 150,
        'old_price': 200,
        'on_sale': True,
        'available': True,
    },
    {
        'name': '2million',
        'slug': '2million',
        'category': categories['Parfum'],
        'price': 250,
        'old_price': 200,
        'on_sale': True,
        'available': True,
    },
    {
        'name': 'nivea',
        'slug': 'nivea',
        'category': categories['Creme'],
        'price': 10,
        'on_sale': False,
        'available': True,
    },
    {
        'name': 'braun',
        'slug': 'braun',
        'category': categories['Shampoo'],
        'price': 10,
        'old_price': 15,
        'on_sale': True,
        'available': True,
    },
    {
        'name': 'brauner',
        'slug': 'brauner',
        'category': categories['Shampoo'],
        'price': 15,
        'old_price': 10,
        'on_sale': True,
        'available': True,
    },
]

# fill the database with products
for product in products:
    item, created = Item.objects.get_or_create(
        name=product['name'],
        defaults=product
    )
    if created:
        print(f"Added: {item.name}")
    else:
        print(f"Already exists: {item.name}")
