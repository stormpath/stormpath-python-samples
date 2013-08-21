from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib import messages

from .forms import UserCreateForm

@login_required
def home(request):
    return render(request, 'home.html', {"title": "Chirper's Nest"})

def stormpath_login(request):
    data = request.POST or None
    form = AuthenticationForm(data=data)

    if 'POST' in request.method:
        if form.is_valid():
            login(request, form.get_user())
            return render(request, 'home.html')
        else:
            messages.add_message(request, messages.ERROR,
                "Invalid credentials, please try again.")

    return render(request, 'login.html', {"form": form,
        "title": "Chirper's Door"})

def stormpath_logout(request):
    logout(request)
    return redirect('login')

def signup(request):
    data = request.POST or None
    form = UserCreateForm(data=data)

    if 'POST' in request.method:
        if form.is_valid():
            try:
                form.save()
            except ValidationError:
                return render(request, 'signup.html', {"form": form,
                    "title": "Chirper's Egg"})
            success_message = \
                    """Thank you for registering. Check your email for a
                    verification message and follow instructions."""
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('login')

    return render(request, 'signup.html', {"form": form,
    "title": "Chirper's Egg"})
