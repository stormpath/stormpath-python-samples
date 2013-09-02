from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import json

from django_stormpath.forms import (UserUpdateForm,
    PasswordResetEmailForm, PasswordResetForm)

from .forms import ChirpForm, ChirperCreateForm
from .models import Chirp


@login_required
def home(request):
    form = ChirpForm(request.POST or None)

    user_is_admin = request.user.is_admin()
    user_is_premium = request.user.is_premium()

    if form.is_valid():
        chirp = form.save(commit=False)
        chirp.user = request.user
        chirp.owner_is_admin = user_is_admin
        chirp.owner_is_premium = user_is_premium
        chirp.save()
        form = ChirpForm()

    if user_is_admin:
        acc_type = 'Admin'
    elif user_is_premium:
        acc_type = 'Premium'
    else:
        acc_type = 'Basic'

    return render(request, 'chirps.html', {"form": form,
        "title": "Chirper's Song",
        "acc_type": acc_type})


@login_required
def chirping(request):
    chirps = Chirp.objects.all().select_related()
    rendered = render_to_string("message.html", {
        'chirps': chirps,
        'user': request.user,
        'is_admin': request.user.is_superuser})

    return HttpResponse(json.dumps([{'chirps': rendered}]),
        mimetype="application/json")


@login_required
def delete_chirp(request, id):
    if request.user.is_admin():
        Chirp.objects.get(pk=id).delete()
    else:
        messages.add_message(request, messages.ERROR,
            "You are not the admin and cannot delete a Chirp! Sorry.")

    return redirect('home')


def stormpath_login(request):
    form = AuthenticationForm(data=(request.POST or None))

    if form.is_valid():
        user = form.get_user()
        user.is_superuser = user.is_admin()
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'login.html', {"form": form,
        "title": "Chirper's Door"})


@login_required
def stormpath_logout(request):
    logout(request)
    return redirect('login')


def signup(request):
    form = ChirperCreateForm(request.POST or None)

    if form.is_valid():
        try:
            form.save()
            success_message = """Thank you for registering. Check your email
                                for a verification message and follow
                                instructions."""
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('login')
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

    return render(request, 'signup.html', {"form": form,
        "title": "Chirper's Egg"})


def send_password_token(request):
    form = PasswordResetEmailForm(request.POST or None)

    if form.is_valid():
        try:
            form.save()
            success_message = \
                """If you specified a valid account email address,
                you should receive Password reset instructions in a few
                moments. If you don't receive an email soon, please
                wait and then try again. If you still have problems
                after that, please contact support."""
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('login')
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

    return render(request, 'password_email.html', {"form": form,
        "title": "Chirper's Amnesia"})


def reset_password(request):
    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        try:
            form.save(request.GET.get('sptoken'))
            success_message = \
                """Success! Your password has been successfully changed.
                You can now log in."""
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('login')
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

    return render(request, 'password_reset.html', {"form": form,
        "title": "Chirper's Amnesia"})


@login_required
def update_user(request):
    form = UserUpdateForm(request.POST or None, instance=request.user)
    if form.is_valid():
        try:
            form.save()
            success_message = "Your profile has been successfully updated."
            messages.add_message(request, messages.SUCCESS, success_message)
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

    return render(request, 'profile.html', {"form": form,
        "title": "Chirper's Pedigree"})
