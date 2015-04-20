from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import Subscription
from .forms import LoginForm, RegistrationForm, ProfileForm
from .forms import validate_avatar


def index(request):
    login_form = LoginForm(request.POST or None)

    if request.POST and login_form.is_valid():
        user = login_form.login()
        if user:
            login(request, user)
            return HttpResponseRedirect(
                request.POST.get('next') or reverse('index')
            )

    return render(
        request,
        "users/index.html",
        {
            "login_form": login_form,
            'next': request.GET.get('next', ''),
        }
    )


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# Register new user
def register_user(request):
    #make sure user is not already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("index"))

    form = RegistrationForm(request.POST or None)
    login_form = LoginForm()
    if request.POST and form.is_valid():
        new_user = form.save()
        new_user.create_related()

        #send confiermationmail blabla
        return HttpResponseRedirect(reverse('register_success'))

    return render(
        request,
        'users/register.html',
        {
            'form': form,
            'login_form': login_form
        }
    )


def register_succes(request):
    login_form = LoginForm(request.POST or None)
    return render(
        request,
        "users/register_success.html",
        {
            "login_form": login_form
        }
    )


def profile(request):
    user = request.user
    initial = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "country": user.profile.country,
        "timezone": user.profile.timezone,
    }
    if "first_name" in request.POST:
        profile_form = ProfileForm(request.POST, user=user)
    else:
        profile_form = ProfileForm(initial=initial, user=user)

    if request.POST:
        profile_form.save_tags(request.POST)
        if profile_form.is_valid():
            profile_form.save()
        if "character" in request.POST:
            character = validate_avatar(request.POST, user)
            if character:
                user.profile.avatar = character
                user.profile.save()

    subscription = user.subscription_set.get(subscription=Subscription.USER)

    return render(
        request,
        "users/profile.html",
        {
            "profile_form": profile_form,
            "subscription": subscription
        }
    )


def membership(request):

    return render(
        request,
        "users/membership.html",
    )
