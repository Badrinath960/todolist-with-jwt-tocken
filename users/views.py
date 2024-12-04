from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from tasks.models import Task
from .forms import UserRegisterForm
from .forms import CustomUserChangeForm, ProfileImageForm
from django.contrib.auth.decorators import login_required
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('details')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def details(request):
    # Get all tasks for the current user
    tasks = Task.objects.filter(user=request.user)

    # Count total, completed, and pending tasks
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    pending_tasks = tasks.filter(status='Pending').count()

    # Pass the task statistics to the template
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'show_task_stats': True,  
    }
    return render(request, 'users/home.html', context)

@login_required
def home(request):
    return render(request, 'base.html')

@login_required
def update_profile(request):
    # Ensure that the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect back to the profile page after updating
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileImageForm(instance=profile)

    return render(request, 'users/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def logout_confirm(request):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            logout(request)
            return redirect('login')  # Redirect to the login page after logout
        else:
            return redirect('details')  # Redirect back to the home page if the user cancels
    return render(request, 'users/logout_confirm.html')
