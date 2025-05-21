from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserPreferenceForm
from .models import UserPreference, CustomUser

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create default preferences for new user
            UserPreference.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Please set your news preferences.')
            return redirect('accounts:preferences')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def preferences(request):
    # Get or create user preferences
    preference, created = UserPreference.objects.get_or_create(
        user=request.user,
        defaults={
            'categories': [],
            'keywords': '',
            'excluded_sources': ''
        }
    )
    
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'News preferences updated successfully!')
            return redirect('news:index')
    else:
        form = UserPreferenceForm(instance=preference)
    
    return render(request, 'accounts/preferences.html', {
        'form': form,
        'categories': UserPreference.CATEGORY_CHOICES
    })

def custom_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('news:index')
