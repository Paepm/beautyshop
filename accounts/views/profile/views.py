from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from devtools import debug
from django.contrib import messages

from ...forms import ProfileEditForm

@login_required
def profile_view(request):
    """Display the profile page."""
    # debug(request.user)

    return render(request, 'profile/profile_detail.html', {
        'login_required': request.user.is_authenticated,
        'user': request.user,
    })

@login_required
def edit_profile_view(request):
    """Display the edit profile page."""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'profile/profile_edit.html', {
        'form': form,
    })