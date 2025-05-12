from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def create_payment_method_view(request):
    

    return render(request, 'create_payment_method.html')
