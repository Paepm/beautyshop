from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def product_list(request):
    # Logic to retrieve and display products
    products = Product.objects.all()
    return render(request, 'shop/index.html', {"products": products})

def about(request):
    # Logic to display the about page
    return render(request, 'shop/about.html')

def contact(request):
    # Logic to display the contact page
    return render(request, 'shop/contact.html')

def privacy(request):
    # Logic to display the imprint page
    return render(request, 'shop/privacy.html')

def agb(request):
    # Logic to display the terms and conditions page
    return render(request, 'shop/agb.html')

def terms_and_conditions(request):
    # Logic to display the terms and conditions page
    return render(request, 'shop/terms_and_conditions.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})