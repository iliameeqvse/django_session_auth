from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('protected')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'authapp/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('protected')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('protected')
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'authapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def protected_view(request):
    return render(request, 'authapp/protected.html')
