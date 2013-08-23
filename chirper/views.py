from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib import messages
import json

from .forms import (UserCreateForm, UserUpdateForm,
    PasswordResetEmailForm, PasswordResetForm, ChirpForm)
from .models import Chirp

@login_required
def home(request):
    form = ChirpForm(request.POST or None)

    if 'POST' in request.method:
        if form.is_valid():
            chirp = form.save(commit=False)
            chirp.user = request.user
            chirp.save()
            form = ChirpForm()

    return render(request, 'chirps.html', {"form": form,
        "title": "Chirper's Song"})

def chirping(request):
    chirps = Chirp.objects.all().select_related()

    chirp_list = []
    for chirp in chirps:
        chirp_list.append({
            'id': chirp.id,
            'message': chirp.message,
            'name': chirp.user.get_full_name(),
            'admin': chirp.user.is_admin()})

    return HttpResponse(json.dumps(chirp_list),
        mimetype="application/json")


def stormpath_login(request):
    data = request.POST or None
    form = AuthenticationForm(data=data)

    if 'POST' in request.method:
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR,
                "Invalid credentials, please try again.")

    return render(request, 'login.html', {"form": form,
        "title": "Chirper's Door"})

@login_required
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

def send_password_token(request):
    form = PasswordResetEmailForm(request.POST or None)

    if 'POST' in request.method:
        if form.is_valid():
            try:
                form.save()
                success_message = \
                    """If you specified a valid account email address,
                    you should receive Password reset instructions in a few
                    moments. If you don't receive an email soon, please wait and
                    then try again. If you still have problems after that,
                    please contact support."""
                messages.add_message(request, messages.SUCCESS, success_message)
                return redirect('login')
            except ValidationError:
                return render(request, 'signup.html', {"form": form,
                    "title": "Chirper's Amnesia"})

    return render(request, 'password_email.html', {"form": form,
        "title": "Chirper's Amnesia"})

def reset_password(request):
    form = PasswordResetForm(request.POST or request.user)

    if 'POST' in request.method:
        if form.is_valid():
            try:
                form.save(request.GET.get('sptoken'))
                success_message = \
                    """Success! Your password has been successfully changed.
                    You can now log in."""
                messages.add_message(request, messages.SUCCESS, success_message)
                return redirect('login')
            except ValidationError:
                pass

    return render(request, 'password_reset.html', {"form": form,
        "title": "Chirper's Amnesia"})

@login_required
def update_user(request):
    if 'POST' in request.method:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                success_message = \
                    """Your profile has been updated."""
                messages.add_message(request, messages.SUCCESS, success_message)
            except ValidationError:
                pass

    form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {"form": form,
        "title": "Chirper's Pedigree"})
